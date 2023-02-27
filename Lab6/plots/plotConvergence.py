import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path


def Logger(filename, algorithm):
    timeList = []

    fp = open(filename)
    line = fp.readline()

    while line:
        tokens = line.split(' ')
        algorithmToken = tokens[0]

        px = int(tokens[6])
        py = int(tokens[8])

        communicationTime = float(tokens[12])
        computationTime = float(tokens[14])
        converganceTime = float(tokens[16])
        totalTime = float(tokens[18])

        timeTuple = (communicationTime, computationTime, converganceTime, totalTime)

        if (algorithmToken == algorithm):
            timeList.append(timeTuple)
                
        line = fp.readline()

    fp.close()
    return timeList

def medianTimeList(algorithm):
    timeList1 = Logger(f"outFiles/run_mpi_convergence1.out", algorithm)
    timeList2 = Logger(f"outFiles/run_mpi_convergence2.out", algorithm)
    timeList3 = Logger(f"outFiles/run_mpi_convergence3.out", algorithm)

    medianList = []

    for i,j,k in zip(timeList1, timeList2, timeList3):
        medianTemp = tuple(map(sum, zip(i,j,k)))
        medianTemp = tuple(map(lambda x: x/3, medianTemp))
        medianList.append(medianTemp)

    return medianList
       

def plotConvergence(timeList, algoName):
    
    plotTitle = f"{algoName} Convergence Analysis - Size: 1024 - MPI Processes: 64"
    outFilePath = f"outFiles/plots/convergence/{algoName}_convergence_1024.png"

    blockSize = ["8x8", "4x16", "16x4"]

    f = plt.figure()
    f.set_figwidth(6.5)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(blockSize))

    for idx, timeArray in enumerate(timeList):
        (commTime, compTime, convTime, totalTime) = timeArray
        print(commTime, compTime, convTime)
        if idx == 0:
            plt.bar(x=X_axis[idx], height=commTime, width=0.2, color="red", bottom=0, label="Communication Time", edgecolor='black')
            plt.bar(x=X_axis[idx], height=compTime, width=0.2, color="blue", bottom=commTime, label="Computation Time", edgecolor='black')
            plt.bar(x=X_axis[idx], height=convTime, width=0.2, color="green", bottom=compTime+commTime, label="Convergence Time", edgecolor='black')
        else:
            plt.bar(x=X_axis[idx], height=commTime, width=0.2, color="red", bottom=0, edgecolor='black')
            plt.bar(x=X_axis[idx], height=compTime, width=0.2, color="blue", bottom=commTime, edgecolor='black')
            plt.bar(x=X_axis[idx], height=convTime, width=0.2, color="green", bottom=compTime+commTime, edgecolor='black') 

    
    plt.xticks(X_axis, blockSize)
    plt.xlabel("Grid Dimensions")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()
    

def main():
    jacobiList = medianTimeList("Jacobi")
    seidelList = medianTimeList("GaussSeidelSOR")
    redBlackList = medianTimeList("RedBlackSOR")

    plotConvergence(timeList=jacobiList, algoName="Jacobi")
    plotConvergence(timeList=seidelList, algoName="Gauss-Seidel SOR")
    plotConvergence(timeList=redBlackList, algoName="Red-Black SOR")
    
if __name__ == "__main__":
    main()
