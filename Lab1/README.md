# Lab 1 - Conway's Game of Life

Simple exercise with the main purpose of familiarizing ourselves with the tools/machines of the lab. Use of OpenMP for parallelizing the Game of Life algorithm.

The algorithm is provided and we simply add the appropriate #pragma directive so that the algorithm is parallelized correctly without performance losses due to poor management of shared/copied variables.

## Time
<p align="center">
    <img src="plot/time_plots/time_64.png" width="40%" height="40%">
    <img src="plot/time_plots/time_1024.png" width="40%" height="40%">
    <img src="plot/time_plots/time_4096.png" width="40%" height="40%">
</p>


## Speedup
<p align="center">
    <img src="plot/speedup_plots/speedup_64.png" width="40%" height="40%">
    <img src="plot/speedup_plots/speedup_1024.png" width="40%" height="40%">
    <img src="plot/speedup_plots/speedup_4096.png" width="40%" height="40%">
</p>