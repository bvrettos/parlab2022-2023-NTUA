import sys
import numpy as np
import matplotlib

import matplotlib.pyplot as plt

mode = "speedup"
threads = ['1','2','4','8','16','32','64']

tSerial = 15.3023

fp = open("kmeansData/kmeans_naive_affinity.out")
line = fp.readline()

kmeansTime = []


while line:
    if line.strip(" ").startswith("nloops"):
        time = float(line.split()[5].strip("s)"))
        kmeansTime.append(time)

    line = fp.readline()

fp.close()

kmeansSpeedup = [tSerial / x for x in kmeansTime]

if mode == "time":

    path = "kmeansNaivePlots/kmeans_naive_gomp_cpu_affinity.png"
    title = "K-means - Naive - GOMP_CPU_AFFINITY - Time - Size:256MB, Coords:16, Clusters:16"

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))


    plt.bar(X_axis, kmeansTime, 0.3, color="red",  edgecolor='black')

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Time (in seconds)")
    plt.title(title)
    plt.savefig(path)

elif mode == "speedup":
    path = "kmeansNaivePlots/kmeans_naive_gomp_cpu_affinity_speedup.png"
    title = "K-means - Naive - GOMP_CPU_AFFINITY - Speedup - Size:256MB, Coords:16, Clusters:16"

    f= plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    plt.plot(X_axis, kmeansSpeedup, color="red", marker='o')

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup")
    plt.title(title)
    plt.legend()
    plt.savefig(path)