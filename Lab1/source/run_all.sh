#!/bin/bash

##Job Name
#PBS -N run_all_game_of_life

##Outfiles
#PBS -o run_all.out
#PBS -e run_all.err

##Number of machines
#PBS -l nodes=1:ppn=8

##Run-time
#PBS -l walltime=00:20:00

module load openmp
cd /home/parallel/parlab06/lab1


for array_size in 64 1024 4096
do
	for threads in 1 2 4 6 8
	do	
		export OMP_NUM_THREADS=$threads
		./Game_Of_Life $array_size 1000
	done
done
