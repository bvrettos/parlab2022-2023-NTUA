#!/bin/bash
mkdir -p outFiles

for threads in 1 2 4 8
do
    for lock_type in "nosync" "pthread_mutex" "pthread_spin" "tas" "ttas" "array" "clh"
    do  
        export OMP_NUM_THREADS=$threads
        ./"kmeans_omp_${lock_type}_lock" -s 16 -n 16 -c 16 -l 10 >> "outFiles/sandman_kmeans_${lock_type}.out"
    done
done