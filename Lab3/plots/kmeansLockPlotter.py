import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

def logger(filename:str):
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
    # tSerial = 0.8780
    tSerial = kmeansTime[0]
    kmeansSpeedup = [tSerial / x for x in kmeansTime]

    return kmeansTime, kmeansSpeedup

def parser() -> str:
    parser = argparse.ArgumentParser(description = "Kmeans Lock Plotter")
    parser.add_argument('--locktype', help = 'Select Locktype', type = str, choices = ['nosync', 'pthread_mutex', 'pthread_spin', 'tas', 'ttas', 'array', 'clh', 'all', 'critical', 'atomic'], required=True)
    parser.add_argument('--folder', type = str, default="outFiles")
    namespace = parser.parse_args()

    return namespace

def plotMultiple(outFilePath:str, title:str, inputList, color, yTitle:str, mode:str):
    threads = ['1','2','4','8','16','32','64']
    legend = ['No Sync', 'PThread-Mutex', 'PThread-Spinlock', 'TAS', 'TTAS', 'Array', 'CLH', 'OMP Critical', 'OMP Atomic']

    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(6)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    if mode == 'Time':
        cnt = -0.1
        for idx, i in enumerate(inputList):
            plt.bar(X_axis + cnt, i, 0.1, align='edge', label=legend[idx], color=color[idx],  edgecolor='black')
            cnt += 0.1
        plt.xticks(X_axis + 0.3, threads)
        plt.xlabel("Number of Threads")
        plt.ylabel(yTitle)
        plt.title(title)
        plt.legend()
        plt.savefig(outFilePath)
    elif mode == 'Speedup':
        for idx, i in enumerate(inputList):
            plt.plot(X_axis, i, marker='o', label=legend[idx], color=color[idx])
        plt.xticks(X_axis + 0.3, threads)
        plt.xlabel("Number of Threads")
        plt.ylabel(yTitle)
        plt.title(title)
        plt.legend()
        plt.savefig(outFilePath)


def timePlotter(outFilePath:str, title:str, timeList, color:str):
    threads = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(6.5)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    plt.bar(X_axis, timeList, 0.3, color=color, edgecolor='black')

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

    plt.plot(X_axis, speedupList, color=color, marker='o')

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Speedup")
    plt.title(title)
    plt.savefig(outFilePath)

def main():
    # Parse arguments
    namespace = parser()
    lock = namespace.locktype
    outFolder = namespace.folder
    plotFolder = f"{outFolder}/plots"
    Path(plotFolder).mkdir(parents=True, exist_ok=True)

    # Choice Arrays
    locks = ['No Lock', 'Mutex', 'Spinlock', 'TAS', 'TTAS', 'Array', 'CLH', 'OMP Critical', 'OMP Atomic']
    colors = ['red', 'green', 'purple', 'darkred', 'blue', 'orange', 'darkblue', 'black', 'darkgreen']
    lockFiles = ['nosync', 'pthread_mutex', 'pthread_spin', 'tas', 'ttas', 'array', 'clh', 'critical', 'atomic']
    

    
    if lock == "all":
        index = 0
        allTimeList = []
        allSpeedupList = []
        allTimeTitle = "K-Means - Time - Size:16MB, Coords:16, Clusters:16"
        allSpeedupTitle = "K-Means - Speedup - Size:16MB, Coords:16, Clusters:16"
        for i in locks:
            timeList, speedupList = logger(f"{outFolder}/sandman_kmeans_{lockFiles[index]}.out")
            allTimeList.append(timeList)
            allSpeedupList.append(speedupList)

            timeTitle = f"K-Means - {i} - Size:16MB, Coords:16, Clusters:16"
            speedupTitle = f"K-Means - {i} - Speedup - Size:16MB, Coords:16, Clusters:16"

            timePlotPath = f"{plotFolder}/kmeans_locks_{lockFiles[index]}.jpg"
            speedupPlotPath = f"{plotFolder}/kmeans_locks_{lockFiles[index]}_speedup.jpg"
            color = colors[index]

            index += 1 
            print (timeList, speedupList)
            speedupPlotter(outFilePath=speedupPlotPath, title=speedupTitle, speedupList=speedupList, color=color)
            timePlotter(outFilePath=timePlotPath, title=timeTitle, timeList=timeList, color=color)
        plotMultiple(f"{plotFolder}/kmeans_locks_all.jpg", allTimeTitle, allTimeList, colors, "Time (in seconds)", mode='Time')
        plotMultiple(f"{plotFolder}/kmeans_locks_all_speedup.jpg", allSpeedupTitle, allSpeedupList, colors, "Speedup", mode='Speedup')
    

    else:
        lockIndex = lockFiles.index(lock)
        ## Get info for Plots
        # Data
        timeList, speedupList = logger(f"{outFolder}/sandman_kmeans_{lock}.out")
        # Plot result path
        timePlotPath = f"{plotFolder}/kmeans_locks_{lock}.jpg"
        speedupPlotPath = f"{plotFolder}/kmeans_locks_{lock}_speedup.jpg"
        # Titles for Plots
        if ((lock == 'critical') or (lock == 'atomic')):
            color = 'black'
            timeTitle = f"K-Means - OMP {lock} - Size:16MB, Coords:16, Clusters:16"
            speedupTitle = f"K-Means - OMP {lock} - Speedup - Size:16MB, Coords:16, Clusters:16"
        else:
            timeTitle = f"K-Means - {locks[lockIndex]} Lock - Size:16MB, Coords:16, Clusters:16"
            speedupTitle = f"K-Means - {lock[lockIndex]} Lock - Speedup - Size:16MB, Coords:16, Clusters:16"
        # Color
            color = colors[lockIndex]
        print(timeList, speedupList)

        speedupPlotter(outFilePath=speedupPlotPath, title=speedupTitle, speedupList=speedupList, color=color)
        timePlotter(outFilePath=timePlotPath, title=timeTitle, timeList=timeList, color=color)

if __name__ == "__main__":
    main()

    
