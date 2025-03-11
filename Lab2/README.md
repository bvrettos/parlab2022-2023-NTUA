# Lab 2 - Shared-Memory Programming Model - K-means

The purpose of the exercise was to parallelize an implementation of K-means for shared memory architectures. We follow the shared address space programming model using OpenMP. We need to identify the parts that can be parallelized in the algorithm and be careful of potential race conditions.

The first implementation is the Naive one, which is the "first thought" someone would have when trying to parallelize the problem. We maintain a shared array of the problem that all executing threads have access to. By thinking a bit further, we can come up with ways to improve the performance of the problem with NUMA-aware optimization techniques.



