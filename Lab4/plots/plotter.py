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
    speedupList = []

    if size == 1024:
        if workload == "100/0/0":
            serialThroughput = 1566.15
        elif workload == "80/10/10":
            serialThroughput = 1897.13
        elif workload == "20/40/40":
            serialThroughput = 1612.85
        elif workload == "0/50/50":
            serialThroughput = 1410.06
    elif size == 8192:
        if workload == "100/0/0":
            serialThroughput = 151.82
        elif workload == "80/10/10":
            serialThroughput = 69.55
        elif workload == "20/40/40":
            serialThroughput = 81.33
        elif workload == "0/50/50":
            serialThroughput = 65.60
    
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
    
    speedupList = [x / serialThroughput for x in throughputList]
    return throughputList, speedupList

def plotThroughput(outFilePath:str, title:str, dataList, mode, speedup=False):
    threads = ['1', '2', '4', '8', '16', '32', '64', '128']

    if speedup is True:
        ylabel = 'Speedup'
    elif speedup is False:
        ylabel = "Throughput(Kops/sec)"

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
    plt.ylabel(ylabel)
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

            allJpgPath = f"outFiles/plots/concurrent_data_structs_all_{size}_{total}_{add}_{remove}.png"
            lowJpgPath = f"outFiles/plots/concurrent_data_structs_low_{size}_{total}_{add}_{remove}.png"
            highJpgPath = f"outFiles/plots/concurrent_data_structs_high_{size}_{total}_{add}_{remove}.png"

            allSpeedupJpgPath = f"outFiles/plots/concurrent_data_structs_all_speedup_{size}_{total}_{add}_{remove}.png"
            lowSpeedupJpgPath = f"outFiles/plots/concurrent_data_structs_low_speedup_{size}_{total}_{add}_{remove}.png"
            highSpeedupJpgPath = f"outFiles/plots/concurrent_data_structs_high_speedup_{size}_{total}_{add}_{remove}.png"

            allTitle = f"Concurrent Linked List - Size: {size} - Workload: {workload}"
            lowTitle = f"Concurrent Linked List - Low Performers - Size: {size} - Workload: {workload}"
            highTitle = f"Concurrent Linked List - High Performers - Size: {size} - Workload: {workload}"

            allSpeedupTitle = f"Concurrent Linked List - Speedup - Size: {size} - Workload: {workload}"
            lowSpeedupTitle = f"Concurrent Linked List - Speedup - Low Performers - Size: {size} - Workload: {workload}"
            highSpeedupTitle = f"Concurrent Linked List - Speedup - High Performers - Size: {size} - Workload: {workload}"

            allDataList = []
            lowPerformersList = []
            highPerformersList = []

            allSpeedup = []
            lowPerformersSpeedup = []
            highPerformersSpeedup = []            

            for type in allTypes:
                data, speedup = logger(type, workload, size)
                allDataList.append(data)
                allSpeedup.append(speedup)

            for type in lowPerformers:
                data, speedup = logger(type, workload, size)
                lowPerformersList.append(data)
                lowPerformersSpeedup.append(speedup)

            for type in highPerformers:
                data, speedup = logger(type, workload, size)
                highPerformersList.append(data)
                highPerformersSpeedup.append(speedup)

            plotThroughput(outFilePath = allJpgPath, title = allTitle, dataList=allDataList, mode='all')
            plotThroughput(outFilePath = lowJpgPath, title = lowTitle, dataList=lowPerformersList, mode='low')
            plotThroughput(outFilePath = highJpgPath, title = highTitle, dataList=highPerformersList, mode='high')

            plotThroughput(outFilePath = allSpeedupJpgPath, title = allSpeedupTitle, dataList = allSpeedup, mode = 'all', speedup=True)
            plotThroughput(outFilePath = lowSpeedupJpgPath, title = lowSpeedupTitle, dataList = lowPerformersSpeedup, mode = 'low', speedup=True)
            plotThroughput(outFilePath = highSpeedupJpgPath, title = highSpeedupTitle, dataList = highPerformersSpeedup, mode = 'high', speedup=True)

            allSpeedup = []
            lowPerformersSpeedup = []
            highPerformersSpeedup = []            
            
            allDataList = []
            lowPerformersList = []
            highPerformersList = []

if __name__ == "__main__":
    main()