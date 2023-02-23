#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <sys/time.h>
#include <mpi.h>
#include "utils.h"

int main(int argc, char **argv)
{
    int rank, size;
    int global[2], local[2];                 // global matrix dimensions and local matrix dimensions (2D-domain, 2D-subdomain)
    int global_padded[2];                    // padded global matrix dimensions (if padding is not needed, global_padded=global)
    int grid[2];                             // processor grid dimensions
    int i, j, t;                             // Indexes for computation
    int global_converged = 0, converged = 0; // flags for convergence, global and per process
    MPI_Datatype dummy;                      // dummy datatype used to align user-defined datatypes in memory
    double omega;                            // relaxation factor - useless for Jacobi
    double *U_start;                         // Need to keep track of Global array starting point in order to scatter/gather from the root process

    struct timeval tts, ttf, tcs, tcf, tconvs, tconvf, tcomms, tcommf; // Timers: total-> tts,ttf, computation -> tcs,tcf, communication -> tcomms,tcommf, convergance -> tconvs,tconvf
    double ttotal = 0, tcomp = 0, tconv = 0, tcomm = 0, total_time, comp_time, conv_time, comm_time;

    double **U, **u_current, **u_previous, **swap; // Global matrix, local current and previous matrices, pointer to swap between current and previous

    MPI_Init(&argc, &argv);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);

    //----Read 2D-domain dimensions and process grid dimensions from stdin----//

    if (argc != 5)
    {
        fprintf(stderr, "Usage: mpirun .... ./exec X Y Px Py");
        exit(-1);
    }
    else
    {
        global[0] = atoi(argv[1]);
        global[1] = atoi(argv[2]);
        grid[0] = atoi(argv[3]);
        grid[1] = atoi(argv[4]);
    }

    //----Create 2D-cartesian communicator----//
    //----Usage of the cartesian communicator is optional----//

    MPI_Comm CART_COMM;      // CART_COMM: the new 2D-cartesian communicator
    int periods[2] = {0, 0}; // periods={0,0}: the 2D-grid is non-periodic
    int rank_grid[2];        // rank_grid: the position of each process on the new communicator

    MPI_Cart_create(MPI_COMM_WORLD, 2, grid, periods, 0, &CART_COMM); // communicator creation
    MPI_Cart_coords(CART_COMM, rank, 2, rank_grid);                   // rank mapping on the new communicator

    //----Compute local 2D-subdomain dimensions----//
    //----Test if the 2D-domain can be equally distributed to all processes----//
    //----If not, pad 2D-domain----//

    for (i = 0; i < 2; i++)
    {
        if (global[i] % grid[i] == 0)
        {
            local[i] = global[i] / grid[i];
            global_padded[i] = global[i];
        }
        else
        {
            local[i] = (global[i] / grid[i]) + 1;
            global_padded[i] = local[i] * grid[i];
        }
    }

    // Initialization of omega
    omega = 2.0 / (1 + sin(3.14 / global[0]));

    //----Allocate global 2D-domain and initialize boundary values----//
    //----Rank 0 holds the global 2D-domain----//
    if (rank == 0)
    {
        U = allocate2d(global_padded[0], global_padded[1]);
        init2d(U, global[0], global[1]);
    }

    //----Allocate local 2D-subdomains u_current, u_previous----//
    //----Add a row/column on each size for ghost cells----//

    u_previous = allocate2d(local[0] + 2, local[1] + 2);
    u_current = allocate2d(local[0] + 2, local[1] + 2);

    //----Distribute global 2D-domain from rank 0 to all processes----//

    //----Appropriate datatypes are defined here----//
    /*****The usage of datatypes is optional*****/

    //----Datatype definition for the 2D-subdomain on the global matrix----//

    MPI_Datatype global_block;
    MPI_Type_vector(local[0], local[1], global_padded[1], MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &global_block);
    MPI_Type_commit(&global_block);

    //----Datatype definition for the 2D-subdomain on the local matrix----//

    MPI_Datatype local_block;
    MPI_Type_vector(local[0], local[1], local[1] + 2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &local_block);
    MPI_Type_commit(&local_block);

    //----Rank 0 defines positions and counts of local blocks (2D-subdomains) on global matrix----//
    int *scatteroffset, *scattercounts;

    if (rank == 0)
    {
        // Keep the starting point of send_buffer from the root in order to scatter later
        // Scatter functions needs to be outside of only-root scope (outside of if rank == 0))
        U_start = &(U[0][0]);
        scatteroffset = (int *)malloc(size * sizeof(int));
        scattercounts = (int *)malloc(size * sizeof(int));
        for (i = 0; i < grid[0]; i++)
            for (j = 0; j < grid[1]; j++)
            {
                scattercounts[i * grid[1] + j] = 1;
                scatteroffset[i * grid[1] + j] = (local[0] * local[1] * grid[1] * i + local[1] * j);
            }
    }

    //----Rank 0 scatters the global matrix----//
    MPI_Scatterv(U_start, scattercounts, scatteroffset, global_block, &(u_previous[1][1]), 1, local_block, 0, MPI_COMM_WORLD);
    MPI_Scatterv(U_start, scattercounts, scatteroffset, global_block, &(u_current[1][1]), 1, local_block, 0, MPI_COMM_WORLD);

    if (rank == 0)
        free2d(U);

    //----Define datatypes or allocate buffers for message passing----//

    // Create Lists of Requests/Statues for the non-blocking communication necessary for the Gauss-Seidel Algorithm.
    // These lists are local and of specific size. The first list is needed by the processes that need to receive data that exist in the u_current array
    // The second list is needed by the processes that do not need any u_current data, but need to wait in order for the root process to gather the results safely

    MPI_Request before_computation_requests[6];
    MPI_Request after_computation_requests[2];

    MPI_Status before_computation_statuses[6];
    MPI_Status after_computation_statuses[2];

    int before_computation_request_index = 0, after_computation_request_index = 0;

    MPI_Datatype mpi_column;
    MPI_Type_vector(local[0], 1, local[1] + 2, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &mpi_column);
    MPI_Type_commit(&mpi_column);

    // Will not use in the end. We wanted to try this method even though it is completely unnecessary, because we thought it could make the
    // Communcation time a bit smaller. In the end, it made the communication time 4 times worse, so we will not use it.
    MPI_Datatype mpi_row;
    MPI_Type_vector(local[0], local[0], 0, MPI_DOUBLE, &dummy);
    MPI_Type_create_resized(dummy, 0, sizeof(double), &mpi_row);
    MPI_Type_commit(&mpi_row);

    //----Find the 4 neighbors with which a process exchanges messages----//

    int north, south, east, west;
    MPI_Cart_shift(CART_COMM, 0, 1, &north, &south);
    MPI_Cart_shift(CART_COMM, 1, 1, &west, &east);

    //---Define the iteration ranges per process-----//

    int i_min, i_max, j_min, j_max;

    /*Three types of ranges:
        -internal processes
        // Internal Processes should run from i = 1 to i = local[0] + 1 and j = 1 to local[1] + 1
        -boundary processes
        // Boundary processes without padded global array should run from i = 2 to local[0] (we do not calculate the outer wall)
        -boundary processes and padded global array
        // Boundary processes from padded global array should only run from i = 2 to the difference between the padded and the normal dimensions of the 2D-array
    */

    // Internal Processes
    i_min = 1;
    i_max = local[0] + 1;

    // Boundary Processes
    if (north == MPI_PROC_NULL)
        i_min = 2;

    if (south == MPI_PROC_NULL)
        i_max -= global_padded[0] - global[0] + 1;

    // Internal Processes
    j_min = 1;
    j_max = local[1] + 1;

    // Boundary Processes
    if (west == MPI_PROC_NULL)
        j_min = 2;

    if (east == MPI_PROC_NULL)
        j_max -= global_padded[1] - global[1] + 1;

    //----Computational core----//
    gettimeofday(&tts, NULL);
#ifdef TEST_CONV
    for (t = 0; t < T && !global_converged; t++)
    {
#endif
#ifndef TEST_CONV
#undef T
#define T 256
        for (t = 0; t < T; t++)
        {
#endif
            swap = u_previous;
            u_previous = u_current;
            u_current = swap;

            gettimeofday(&tcomms, NULL);

            if (west != MPI_PROC_NULL)
            {
                MPI_Isend(&u_previous[1][1], 1, mpi_column, west, 420, MPI_COMM_WORLD, &before_computation_requests[before_computation_request_index]);
                MPI_Irecv(&u_current[1][0], 1, mpi_column, west, 420, MPI_COMM_WORLD, &before_computation_requests[++before_computation_request_index]);
                before_computation_request_index++;
            }

            if (east != MPI_PROC_NULL)
                MPI_Irecv(&u_previous[1][local[1] + 1], 1, mpi_column, east, 420, MPI_COMM_WORLD, &before_computation_requests[before_computation_request_index++]);

            if (north != MPI_PROC_NULL)
            {
                MPI_Isend(&u_previous[1][1], local[1], MPI_DOUBLE, north, 420, MPI_COMM_WORLD, &before_computation_requests[before_computation_request_index]);
                MPI_Irecv(&u_current[0][1], local[1], MPI_DOUBLE, north, 420, MPI_COMM_WORLD, &before_computation_requests[++before_computation_request_index]);
                before_computation_request_index++;
            }

            if (south != MPI_PROC_NULL)
                MPI_Irecv(&u_previous[local[0] + 1][1], local[1], MPI_DOUBLE, south, 420, MPI_COMM_WORLD, &before_computation_requests[before_computation_request_index++]);

            MPI_Waitall(before_computation_request_index, before_computation_requests, before_computation_statuses);

            gettimeofday(&tcommf, NULL);

            tcomm += (tcommf.tv_sec - tcomms.tv_sec) + (tcommf.tv_usec - tcomms.tv_usec) * 0.000001;

            gettimeofday(&tcs, NULL);

            for (i = i_min; i < i_max; i++)
                for (j = j_min; j < j_max; j++)
                    u_current[i][j] = u_previous[i][j] + omega * (u_current[i - 1][j] + u_previous[i + 1][j] + u_current[i][j - 1] + u_previous[i][j + 1] - 4.0 * u_previous[i][j]) / 4.0;

            gettimeofday(&tcf, NULL);

            gettimeofday(&tcomms, NULL);

            if (east != MPI_PROC_NULL)
                MPI_Isend(&u_current[1][local[1]], 1, mpi_column, east, 420, MPI_COMM_WORLD, &after_computation_requests[after_computation_request_index++]);

            if (south != MPI_PROC_NULL)
                MPI_Isend(&u_current[local[0]][1], local[1], MPI_DOUBLE, south, 420, MPI_COMM_WORLD, &after_computation_requests[after_computation_request_index++]);

            MPI_Waitall(after_computation_request_index, after_computation_requests, after_computation_statuses);

            gettimeofday(&tcommf, NULL);

            tcomm += (tcommf.tv_sec - tcomms.tv_sec) + (tcommf.tv_usec - tcomms.tv_usec) * 0.000001;

            tcomp += (tcf.tv_sec - tcs.tv_sec) + (tcf.tv_usec - tcs.tv_usec) * 0.000001;

            // Reset indexes so as to not overflow by mistake
            before_computation_request_index = 0;
            after_computation_request_index = 0;

#ifdef TEST_CONV
            if (t % C == 0)
            {
                gettimeofday(&tconvs, NULL);

                converged = converge(u_previous, u_current, i_min, i_max, j_min, j_max);
                MPI_Allreduce(&converged, &global_converged, 1, MPI_INT, MPI_MIN, MPI_COMM_WORLD);

                gettimeofday(&tconvf, NULL);
                tconv += (tconvf.tv_sec - tconvs.tv_sec) + (tconvf.tv_usec - tconvs.tv_usec) * 0.000001;
            }
#endif

            //************************************//
        }
        gettimeofday(&ttf, NULL);

        ttotal = (ttf.tv_sec - tts.tv_sec) + (ttf.tv_usec - tts.tv_usec) * 0.000001;

        MPI_Reduce(&ttotal, &total_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        MPI_Reduce(&tcomp, &comp_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        MPI_Reduce(&tconv, &conv_time, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD);
        MPI_Reduce(&tcomm, &comm_time, 1, MPI_DOUBLE, MPI_SUM, 0, MPI_COMM_WORLD);

        comm_time /= grid[0] * grid[1];

        //----Rank 0 gathers local matrices back to the global matrix----//
        if (rank == 0)
        {
            U = allocate2d(global_padded[0], global_padded[1]);
            U_start = &(U[0][0]);
        }
        MPI_Gatherv(&(u_previous[1][1]), 1, local_block, U_start, scattercounts, scatteroffset, global_block, 0, MPI_COMM_WORLD);

        //----Printing results----//
        if (rank == 0)
        {
            printf("GaussSeidelSOR X %d Y %d Px %d Py %d Iter %d CommunicationTime(Median) %lf ComputationTime(Max) %lf ConverganceTime(Max) %lf TotalTime %lf midpoint %lf\n", global[0], global[1], grid[0], grid[1], t - 1, comm_time, comp_time, conv_time, total_time, U[global[0] / 2][global[1] / 2]);

#ifdef PRINT_RESULTS
            char *s = malloc(50 * sizeof(char));
            sprintf(s, "resGaussSeidelSORMPI_%dx%d_%dx%d", global[0], global[1], grid[0], grid[1]);
            fprint2d(s, U, global[0], global[1]);
            free(s);
#endif
        }
        MPI_Finalize();
        return 0;
    }