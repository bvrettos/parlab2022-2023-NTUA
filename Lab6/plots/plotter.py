import argparse
import os
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pathlib import Path


def Logger(filename, algorithm, size):
    timeList = []

    fp = open(filename)
    line = fp.readline()

    while line:
        tokens = line.split(' ')
        algorithmToken = tokens[0]
        sizeToken = int(tokens[2])

        px = int(tokens[6])
        py = int(tokens[8])

        communicationTime = float(tokens[12])
        computationTime = float(tokens[14])
        converganceTime = float(tokens[16])
        totalTime = float(tokens[18])

        timeTuple = (communicationTime, computationTime, converganceTime, totalTime)

        if (algorithmToken == algorithm) and (sizeToken == size):
            timeList.append(timeTuple)
                
        line = fp.readline()

    fp.close()
    return timeList

def medianTimeList(algorithm, size):
    timeList1 = Logger(f"outFiles/run_mpi_scaling1.out", algorithm, size)
    timeList2 = Logger(f"outFiles/run_mpi_scaling2.out", algorithm, size)
    timeList3 = Logger(f"outFiles/run_mpi_scaling3.out", algorithm, size)

    medianList = []

    for i,j,k in zip(timeList1, timeList2, timeList3):
        medianTemp = tuple(map(sum, zip(i,j,k)))
        medianTemp = tuple(map(lambda x: x/3, medianTemp))
        medianList.append(medianTemp)

    return medianList
       
def returnAlgorithmResults(algorithm):
    # SerialTimeList = [tSerial2048, tSerial4096, tSerial6144]
    timeList2048 = medianTimeList(algorithm, 2048)
    timeList4096 = medianTimeList(algorithm, 4096)
    timeList6144 = medianTimeList(algorithm, 6144)

    speedupList2048 = [timeList2048[0][3] / x[3] for x in timeList2048]
    speedupList4096 = [timeList4096[0][3] / x[3] for x in timeList4096]
    speedupList6144 = [timeList6144[0][3] / x[3] for x in timeList6144]

    return timeList2048, timeList4096, timeList6144, speedupList2048, speedupList4096, speedupList6144

def plotTimeAnalysis(timeArray, algoName, size):
    
    plotTitle = f"{algoName} Time Analysis - Size: {size} - Iterations: 256"
    outFilePath = f"outFiles/plots/{algoName}_{size}_time_analysis.png"

    procs = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(procs))

    commTime, compTime, convTime, totalTime = zip(*timeArray)

    plt.bar(x=X_axis, height=commTime, width=0.2, color="red", bottom=0, label="Comm Time")
    plt.bar(x=X_axis, height=compTime, width=0.2, color="blue", bottom=commTime, label="Comp Time")
    plt.bar(x=X_axis, height=convTime, width=0.2, color="green", bottom=compTime, label="Conv Time")
    

    plt.xticks(X_axis, procs)
    plt.xlabel("No. Processes")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()
    

def main():
    jacobiTime2048, jacobiTime4096, jacobiTime6144, jacobiSpeedup2048, jacobiSpeedup4096, jacobiSpeedup6144 = returnAlgorithmResults("Jacobi")
    seidelTime2048, seidelTime4096, seidelTime6144, seidelSpeedup2048, seidelSpeedup4096, seidelSpeedup6144 = returnAlgorithmResults("GaussSeidelSOR")
    redBlackTime2048, redBlackTime4096, redBlackTime6144, redBlackSpeedup2048, redBlackSpeedup4096, redBlackSpeedup6144 = returnAlgorithmResults("RedBlackSOR")

    timeArray2048 = [jacobiTime2048, seidelTime2048, redBlackTime2048]
    timeArray4096 = [jacobiTime4096, seidelTime4096, redBlackTime4096]
    timeArray6144 = [jacobiTime6144, seidelTime6144, redBlackTime6144]

    plotTimeAnalysis(timeArray=jacobiTime2048, algoName="Jacobi", size=2048)
    plotTimeAnalysis(timeArray=jacobiTime4096, algoName="Jacobi", size=4096)
    plotTimeAnalysis(timeArray=jacobiTime6144, algoName="Jacobi", size=6144)
    
if __name__ == "__main__":
    main()
