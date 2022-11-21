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
    parser.add_argument('--locktype', help = 'Select Locktype', type = str, choices = ['no_lock', 'mutex', 'spinlock', 'tas', 'ttas', 'array', 'clh', 'all'], required=True)
    parser.add_argument('--outfile', help = 'Kmeans outfile path (relative to script)', type = str, required=True)
    namespace = parser.parse_args()

    return namespace

def timePlotter(outFilePath:str, plotTitle:str, timeList, color:str):
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
    plt.title(plotTitle)
    plt.savefig(outFilePath)
    
def speedupPlotter(outFilePath:str, plotTitle:str, speedupList, color:str):
    threads = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    plt.bar(X_axis, speedupList, 0.3, color=color)

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup")
    plt.title(plotTitle)
    plt.savefig(outFilePath)

def main():
    # Parse arguments
    namespace = parser()
    lock = namespace.locktype

    # Switch-Case (Python gamiesai)
    if lock == 'no_lock':
        color = "red"
        timeTitle = "test"
        speedupTitle = "test2"
        timePlotPath = "path"
        speedupPlotPath = "test2"
    elif lock == 'mutex':
        pass
    elif lock == 'spinlock':
        pass
    elif lock == 'tas':
        pass
    elif lock == 'ttas':
        pass
    elif lock == 'array':
        pass
    elif lock == 'clh':
        pass
    elif lock == 'all':
        pass
    
    # Log Data from Outfiles
    timeList, speedupList = logger(namespace.outfile)

    # Plot and Save
    timePlotter(outFilePath=timePlotPath, title=timeTitle, timeList=timeList, color=color)
    speedupPlotter(outFilePath=speedupPlotPath, title=speedupTitle, speedupList=speedupList, color=color)


if __name__ == "__main__":
    main()

    
