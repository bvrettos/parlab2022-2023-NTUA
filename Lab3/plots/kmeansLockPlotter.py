import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def logger(filename:str) -> list:
    kmeansTime = []
    kmeansSpeedup = []
    
    fp = open(filename)
    line = fp.readline()

    while line:
        if line.strip(" ").startswith("nloops"):
            time = float(line.split()[5].strip("s)"))
            kmeansTime.append(time)
        line = fp.readline()

    fp.close()
    tSerial = kmeansTime[0]
    kmeansSpeedup = [tSerial / x for x in kmeansTime]

    return kmeansTime, kmeansSpeedup

def parser() -> str:
    parser = argparse.ArgumentParser(description = "Kmeans Lock Plotter")
    parser.add_argument('--locktype', help = 'Select Locktype', type = str, choices = ['nosync', 'mutex', 'spinlock', 'tas', 'ttas', 'array', 'clh', 'all', 'critical', 'atomic'], required=True)
    parser.add_argument('--outfile', help = 'Kmeans outfile path (relative to script)', type = str, required=True)
    parser.add_argument('--affinity', type = str, default="")
    namespace = parser.parse_args()

    return namespace

def timePlotter(outFilePath:str, title:str, timeList, color:str):
    threads = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    plt.bar(X_axis, timeList, 0.3, color=color)

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Time (in seconds)")
    plt.title(title)
    plt.savefig(outFilePath)
    
def speedupPlotter(outFilePath:str, title:str, speedupList, color:str):
    threads = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    plt.plot(X_axis, speedupList, 0.3, color=color, marker='o')

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup")
    plt.title(title)
    plt.savefig(outFilePath)

def main():
    # Parse arguments
    namespace = parser()
    lock = namespace.locktype
    affinity = namespace.affinity

    # Switch-Case (Python gamiesai)
    folder = f"plots{affinity}"
    timePlotPath = f"{folder}/kmeans_locks_{lock}.jpg"
    speedupPlotPath = f"{folder}/kmeans_locks_{lock}_speedup.jpg"
    
    if ((lock == 'critical') or (lock == 'atomic')):
        timeTitle = f"K-Means - OMP {lock} - Size:16MB, Coords:16, Clusters:16"
        speedupTitle = f"K-Means - OMP {lock} - Speedup - Size:16MB, Coords:16, Clusters:16"

    timeTitle = f"K-Means - {lock} Lock - Size:16MB, Coords:16, Clusters:16"
    speedupTitle = f"K-Means - {lock} Lock - Speedup - Size:16MB, Coords:16, Clusters:16"

    color = "red"
    # Log Data from Outfiles
    timeList, speedupList = logger(namespace.outfile)

    # Plot and Save
    print(timeList, speedupList)
    speedupPlotter(outFilePath=speedupPlotPath, title=speedupTitle, speedupList=speedupList, color=color)

    timePlotter(outFilePath=timePlotPath, title=timeTitle, timeList=timeList, color=color)


if __name__ == "__main__":
    main()

    
