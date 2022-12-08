import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

def logger(type:str, workload:str, size:int) -> list[float]:
    throughputList = []
    completeList = []
    
    total = workload.split('/')[0]
    add = workload.split('/')[1]
    remove = workload.split('/')[2]

    filename = f"outFiles/{type}_{size}_{total}_{add}_{remove}.out"

    fp = open(filename)
    line = fp.readline()

    while line:
        if (line.strip(" ").startswith("Nthreads:") and line.split()[5] == workload):
            throughput = float(line.split()[7])
            throughputList.append(throughput)
            
        line = fp.readline()

    fp.close()
    
    return throughputList

def plotThroughput(outFilePath:str, title:str, dataList, mode):
    threads = ['1', '2', '4', '8', '16', '32', '64', '128']

    if mode == 'all':
        legend = ["Coarse-Grain Locking", "Fine-Grain Locking", "Optimistic Syncrhonization", "Lazy Syncrhonization", "Non-Block Synchronization"]
    elif mode == 'low':
        legend = ["Coarse-Grain Locking", "Fine-Grain Locking", "Optimistic Syncrhonization"]
    elif mode == 'high':
        legend = ["Lazy Syncrhonization", "Non-Block Synchronization"]

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(threads))

    for idx, dataArray in enumerate(dataList):
        print(dataArray)
        plt.plot(X_axis, dataArray, label=legend[idx],  marker = 'x')

    plt.xticks(X_axis, threads)
    plt.xlabel("Number of Threads")
    plt.ylabel("Throughput(Kops/sec)")
    plt.title(title)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()
    
def main():
    workloads = ["100/0/0", "80/10/10", "20/40/40", "0/50/50"]
    lowPerformers = ["cgl", "fgl", "opt"]
    highPerformers = ['lazy', 'nb']
    allTypes = ["cgl", "fgl", "opt", 'lazy', 'nb']
    colors = ['green', 'purple', 'darkred', 'blue', 'orange']

    sizes = [1024,8192]

    for size in sizes:
        for workload in workloads:
            total = workload.split('/')[0]
            add = workload.split('/')[1]
            remove = workload.split('/')[2]

            allJpgPath = f"outFiles/plots/concurrent_data_structs_all_{size}_{total}_{add}_{remove}.jpg"
            lowJpgPath = f"outFiles/plots/concurrent_data_structs_low_{size}_{total}_{add}_{remove}.jpg"
            highJpgPath = f"outFiles/plots/concurrent_data_structs_high_{size}_{total}_{add}_{remove}.jpg"

            allTitle = f"Concurrent Linked List - Size: {size} - Workload: {workload}"
            lowTitle = f"Concurrent Linked List - Low Performers - Size: {size} - Workload: {workload}"
            highTitle = f"Concurrent Linked List - High Performers - Size: {size} - Workload: {workload}"

            allDataList = []
            lowPerformersList = []
            highPerformersList = []            

            for type in allTypes:
                data = logger(type, workload, size)
                allDataList.append(data)

            for type in lowPerformers:
                data = logger(type, workload, size)
                lowPerformersList.append(data)

            for type in highPerformers:
                data = logger(type, workload, size)
                highPerformersList.append(data)

            plotThroughput(outFilePath = allJpgPath, title = allTitle, dataList=allDataList, mode='all')
            plotThroughput(outFilePath = lowJpgPath, title = lowTitle, dataList=lowPerformersList, mode='low')
            plotThroughput(outFilePath = highJpgPath, title = highTitle, dataList=highPerformersList, mode='high')
            
            allDataList = []
            lowPerformersList = []
            highPerformersList = []

if __name__ == "__main__":
    main()