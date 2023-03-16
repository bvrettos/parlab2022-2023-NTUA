import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path

def CSVLogger(type:str, size:int, numCoords:int, clusters:int):
    measurementArray = []
    speedupArray = []
    sumList = []

    filename = f"outFiles/Sz-{size}_Coo-{numCoords}_Cl-{clusters}.csv"

    if numCoords == 2:
        serialTime = 18446.200132
    elif numCoords == 16:
        serialTime = 5484.833002
    
    fp = open(filename)
    line = fp.readline()

    while line:
        if(line.startswith(type)):
            line = line.split(',')
            measurement = (int(line[1]), float(line[5]), float(line[6]), float(line[7]))
            measurementArray.append(measurement)

        line = fp.readline()

    fp.close()

    for i in measurementArray:
        Sum = sum(i[1:])
        sumList.append(Sum)
    
    speedupArray = [serialTime / x for x in sumList]
    # print(measurementArray, speedupArray)
    return measurementArray, speedupArray, sumList

def timePlotter(outFilePath:str, title:str, timeList, color:str):
    blockSize = ['32','64','128','256','512','1024']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(blockSize))

    plt.bar(X_axis, timeList, 0.3, color=color, edgecolor='black')

    plt.xticks(X_axis, blockSize)
    plt.xlabel("Block Size")
    plt.ylabel("Time (in milliseconds)")
    plt.title(title)
    plt.savefig(outFilePath)

def speedupPlotter(outFilePath:str, title:str, speedupList, color:str):
    blockSize = ['32','64','128','256','512','1024']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(blockSize))

    plt.bar(X_axis, speedupList, 0.3, color=color, edgecolor='black')

    plt.xticks(X_axis, blockSize)
    plt.xlabel("Block Size")
    plt.ylabel("Speedup")
    plt.title(title)
    plt.savefig(outFilePath)

def singularPlot(type:str, numCoords:int, size:int, clusters:int, color:str):
    _, speedupList, sumList = CSVLogger(type,size,numCoords, clusters)
    
    outFilePath = f"outFiles/plots/kmeans_gpu_{type}_{numCoords}_"
    title = f"K-Means - CUDA Version - Size:{size}MB, Coords:{numCoords}, Clusters:{clusters}"

    timePath = outFilePath + "time.png"
    speedupPath = outFilePath + "speedup.png"

    timeTitle = title + f" - {type}"
    speedupTitle = title + " - Speedup" + f" - {type}"

    timePlotter(timePath, timeTitle, sumList, color)
    speedupPlotter(speedupPath, speedupTitle, speedupList, color)

def plotAll(types, coordsList, colors):
    for type,color in zip(types,colors):
        for numCoords in coordsList:
            singularPlot(type, numCoords, 256, 16, color)

def commonFigurePlotter(types, coordsList, colors, legends):
    blockSize = ['32','64','128','256','512','1024']
    modes = ['Time', 'Speedup']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(6)
    f.tight_layout() 

    X_axis = np.arange(len(blockSize))
    for mode in modes:
        for numCoords in coordsList:
            title = f"K-Means - CUDA Version - Size:256MB, Coords:{numCoords}, Clusters:16"
            outFilePath = f"outFiles/plots/kmeans_gpu_common_figure_{numCoords}_"
            cnt = 0.1
            if mode == 'Speedup':
                title += " - Speedup"
                outFilePath += "speedup.png"
                for type,color,legend in zip(types,colors,legends):
                    _, speedupList, sumList = CSVLogger(type,256,numCoords, 16)
                    
                    plt.bar(X_axis+cnt, speedupList, 0.2, color=color,label=legend, edgecolor='black')
                    cnt += 0.2
            elif mode == 'Time':
                outFilePath += "time.png"
                for type,color,legend in zip(types,colors,legends):
                    _, speedupList, sumList = CSVLogger(type,256,numCoords, 16)
                    
                    plt.bar(X_axis+cnt, sumList, 0.2, color=color,label=legend, edgecolor='black')
                    cnt += 0.2
            plt.xticks(X_axis, blockSize)
            plt.xlabel("Block Size")
            plt.ylabel("Time (in milliseconds)")
            plt.title(title)
            plt.legend()
            plt.savefig(outFilePath)
            plt.close()
            f = plt.figure()
            f.set_figwidth(8)
            f.set_figheight(6)
            f.tight_layout()
        
def piePlot(type:str, numCoords:int, legend:str):
    measurementArray, _, _ = CSVLogger(type, 256, numCoords, 16)
    breakLists = list(zip(*measurementArray))

    outFilePath = f"outFiles/plots/kmeans_gpu_{type}_{numCoords}_bottleneck_analysis.png"
    title = f"K-Means - Bottleneck Analysis - {legend} - Size:256MB, Coords:{numCoords}, Clusters:16"

    labels = ['CPU Time', 'CPU-GPU Transfers Time', 'GPU Time']
    cpuTime = sum(breakLists[1])/len(breakLists[1])
    transferTime = sum(breakLists[2])/len(breakLists[2])
    gpuTime = sum(breakLists[3])/len(breakLists[3])
    
    explode = (0,0,0)
    
    pieArray = [cpuTime, transferTime, gpuTime]

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(6)
    f.tight_layout() 
    plt.pie(pieArray, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True)
    plt.axis('equal')
    plt.title(title)
    plt.savefig(outFilePath)

def bottleneckAnalysisPlot(numCoords:int):
    naiveArray, _, _ = CSVLogger("Naive", 256, numCoords, 16)
    transposeArray, _, _ = CSVLogger("Transpose", 256, numCoords, 16)
    sharedArray, _, _ = CSVLogger("Shmem", 256, numCoords, 16)

    outFilePath = f"outFiles/plots/kmeans_gpu_{numCoords}_bottleneck_analysis.png"
    title = f"K-Means - Bottleneck Analysis - Size:256MB, Coords:{numCoords}, Clusters:16"
    blockSize = ['32','64','128','256','512','1024']

    X_axis = np.arange(len(blockSize))

    f = plt.figure()
    f.set_figwidth(10)
    f.set_figheight(8)
    f.tight_layout()

    offset = -0.3
    for idx, naiveTuple in enumerate(naiveArray):
        if idx == 0:
            cpuLabel = "Naive CPU"
            transLabel = "Naive CPU-GPU Transfers"
            gpuLabel = "Naive GPU"
        else:
            cpuLabel = transLabel = gpuLabel = ""
        (_, cpuPart, transferPart, gpuPart) = naiveTuple
        plt.bar(x=X_axis[idx]+offset, width = 0.25, height=gpuPart+transferPart+cpuPart, color="#FF2500", label=gpuLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=transferPart+cpuPart, color="#00FF25", label=transLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=cpuPart, color="#2500FF", label=cpuLabel, edgecolor="black")

    offset += 0.3

    for idx, naiveTuple in enumerate(transposeArray):
        if idx == 0:
            cpuLabel = "Transpose CPU"
            transLabel = "Transpose CPU-GPU Transfers"
            gpuLabel = "Transpose GPU"
        else:
            cpuLabel = transLabel = gpuLabel = ""
        (_, cpuPart, transferPart, gpuPart) = naiveTuple
        plt.bar(x=X_axis[idx]+offset, width = 0.25, height=gpuPart+transferPart+cpuPart, color="#FFC100", label=gpuLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=transferPart+cpuPart, color="#00FFC1", label=transLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=cpuPart, color="#C100FF", label=cpuLabel, edgecolor="black")

    offset += 0.3

    for idx, naiveTuple in enumerate(sharedArray):
        if idx == 0:
            cpuLabel = "Shared Memory CPU"
            transLabel = "Shared Memory CPU-GPU Transfers"
            gpuLabel = "Shared Memory GPU"
        else:
            cpuLabel = transLabel = gpuLabel = ""
        (_, cpuPart, transferPart, gpuPart) = naiveTuple
        plt.bar(x=X_axis[idx]+offset, width = 0.25, height=gpuPart+transferPart+cpuPart, color="#FF008B", label=gpuLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=transferPart+cpuPart, color="#8BFF00", label=transLabel, edgecolor="black")
        plt.bar(x=X_axis[idx]+offset,  width = 0.25, height=cpuPart, color="#008BFF", label=cpuLabel, edgecolor="black")

    plt.xticks(X_axis, blockSize)
    plt.xlabel("Block Size")
    plt.ylabel("Time (in milliseconds)")
    plt.title(title)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()
    
def piePlotAll(types, coordsList,legends):
    for type,legend in zip(types,legends):
        for numCoords in coordsList:
            piePlot(type, numCoords,legend)

    
def runAllPlots():
    types = ["Naive", "Transpose", "Shmem"]
    legend = ["Naive", "Transpose", "Shared Memory"]
    coordsList = [2,16]
    colors = ["darkblue", "darkgreen", "darkred"]

    commonFigurePlotter(types, coordsList, colors, legend)
    plotAll(types, coordsList, colors)
    bottleneckAnalysisPlot(2)
    bottleneckAnalysisPlot(16)

def main():
    runAllPlots()

if __name__ == "__main__":
    main()