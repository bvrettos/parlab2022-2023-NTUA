#!/bin/bash

for nsize in 1024 2048 4096
do
	for blocksize in 32 64 128 256 512	
	do	
		for threads in 1 2 4 8
		do
			export OMP_NUM_THREADS=$threads
			./fw_tiled $nsize $blocksize
		done
	done
done
