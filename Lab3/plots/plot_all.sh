#!/bin/bash

for folder in "outFiles" "outFilesAffinityMouliko" "outFilesCores" "outFilesCoresClose"
do
    python3 ./kmeansLockPlotter.py --locktype all --folder $folder
done

