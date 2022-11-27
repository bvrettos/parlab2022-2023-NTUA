#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans

## Output and error files
#PBS -o run_kmeans.out
#PBS -e run_kmeans.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

module load openmp
cd /home/parallel/parlab06/lab3



for threads in 1 2 4 8 16 32 64
do
    for lock_type in "nosync" "pthread_mutex" "pthread_spin" "tas" "ttas" "array" "clh"
    do  
        export OMP_NUM_THREADS=$threads
        ./"kmeans_omp_${lock_type}_lock" -s 16 -n 16 -c 16 -l 10 >> "outFiles/sandman_kmeans_${lock_type}.out"
    done
done
