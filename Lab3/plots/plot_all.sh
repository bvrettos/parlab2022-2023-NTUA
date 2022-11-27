#!/bin/bash

# for affinity_type in "affinitymouliko" "cores" "coresclose" ""
# do
#     mkdir -p "plots${affinity_type}"
#     for lock_type in "nosync" "mutex" "spinlock" "tas" "ttas" "array" "clh"
#     do
#         python3 kmeansLockPlotter.py --locktype ${lock_type} --outfile outFiles${affinity_type}/sandman_kmeans_${lock_type}.out
#     done
# done

