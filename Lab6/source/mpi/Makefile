CC=mpicc
CFLAGS=-O3 -lm -Wall
# RES=-DPRINT_RESULTS
CONV=-DTEST_CONV

all: jacobi seidelsor redblacksor

jacobi: Jacobi_mpi.c utils.c
	$(CC) $(CFLAGS) $(RES) $(CONV) Jacobi_mpi.c utils.c -o jacobi_mpi

seidelsor: GaussSeidelSOR_mpi.c utils.c
	$(CC) $(CFLAGS) $(RES) $(CONV) GaussSeidelSOR_mpi.c -lm utils.c -o seidelsor_mpi

redblacksor: RedBlackSOR_mpi.c utils.c 
	$(CC) $(CFLAGS) $(RES) $(CONV) RedBlackSOR_mpi.c -lm utils.c -o redblacksor_mpi

clean:
	rm jacobi_mpi seidelsor_mpi redblacksor_mpi

