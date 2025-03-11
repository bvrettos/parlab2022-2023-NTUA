# Lab 6 - MPI Programming Model - Heat Transfer Equation

Moving on from the K-means algorithm, we transition important numerical analysis algorithms from shared memory to distributed memory using the Message Passing Interface (MPI), the de facto standard for programming distributed systems. Specifically, we focus on implementing and optimizing the Jacobi, Gauss-Seidel, and Red-Black algorithms for solving the heat equation in a 2D space.

The main conclusion is that transforming a shared-memory program to run in distributed environments needs heavy code refactoring and heavy attention to data distributions and cache management, in order to achieve high performance and scalability.