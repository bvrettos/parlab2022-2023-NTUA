/*
 * Tiled version of the Floyd-Warshall algorithm.
 * command-line arguments: N, B
 * N = size of graph
 * B = size of tile
 * works only when N is a multiple of B
 */
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "util.h"

inline int min(int a, int b);
inline void FW(int **A, int K, int I, int J, int N);

int main(int argc, char **argv)
{
	int **A;
	int i,j,k;
	struct timeval t1, t2;
	double time;
	int B=64;
	int N=1024;

	char *numThreadsChar;
	int numThreads = 0;

	if ((numThreadsChar = getenv("OMP_NUM_THREADS")) != NULL)
		numThreads = atoi(numThreadsChar);

	if (argc != 3){
		fprintf(stdout, "Usage %s N B\n", argv[0]);
		exit(0);
	}

	N=atoi(argv[1]);
	B=atoi(argv[2]);

	A=(int **)malloc(N*sizeof(int *));
	for(i=0; i<N; i++)A[i]=(int *)malloc(N*sizeof(int));

	graph_init_random(A,-1,N,128*N);

	gettimeofday(&t1,0);


	for(k=0;k<N;k+=B){
		// Compute the Akk tile
		FW(A,k,k,k,B);

		#pragma omp parallel
		{
			#pragma omp single
			{
				for(i=0; i<k; i+=B)
					#pragma omp task
						FW(A,k,i,k,B);

				for(i=k+B; i<N; i+=B)
					#pragma omp task
						FW(A,k,i,k,B);

				for(j=0; j<k; j+=B)
					#pragma omp task
						FW(A,k,k,j,B);

				for(j=k+B; j<N; j+=B)
					#pragma omp task
						FW(A,k,k,j,B);
			}
		}


		#pragma omp parallel
		{
			#pragma omp single
			{
				for(i=0; i<k; i+=B)
					for(j=0; j<k; j+=B)
						#pragma omp task
							FW(A,k,i,j,B);

				for(i=0; i<k; i+=B)
					for(j=k+B; j<N; j+=B)
						#pragma omp task
							FW(A,k,i,j,B);

				for(i=k+B; i<N; i+=B)
					for(j=0; j<k; j+=B)
						#pragma omp task
							FW(A,k,i,j,B);

				for(i=k+B; i<N; i+=B)
					for(j=k+B; j<N; j+=B)
						#pragma omp task
							FW(A,k,i,j,B);
			}
		}
	}
	gettimeofday(&t2,0);

	time=(double)((t2.tv_sec-t1.tv_sec)*1000000+t2.tv_usec-t1.tv_usec)/1000000;
	printf("FW_TILED_TASK,%d,%d,%.4f,Threads = %d\n", N,B,time,numThreads);

	/*
	   for(i=0; i<N; i++)
	   for(j=0; j<N; j++) fprintf(stdout,"%d\n", A[i][j]);
	 */

	return 0;
}

inline int min(int a, int b)
{
	if(a<=b)return a;
	else return b;
}

inline void FW(int **A, int K, int I, int J, int N)
{
	int i,j,k;

	for(k=K; k<K+N; k++)
		#pragma omp parallel for private(i,j,A) shared(N,k)
		for(i=I; i<I+N; i++)
			for(j=J; j<J+N; j++)
				A[i][j]=min(A[i][j], A[i][k]+A[k][j]);

}
