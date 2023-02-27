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
    outFilePath = f"outFiles/plots/{algoName}_{size}.png"

    procs = ['8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(procs))

    commTime, compTime, convTime, totalTime = zip(*timeArray[3:])

    plt.bar(x=X_axis, height=totalTime, width=0.2, color="blue", bottom=0, label="Total Time", edgecolor='black')
    plt.bar(x=X_axis, height=commTime, width=0.2, color="red", bottom=0, label="Communication Time", edgecolor='black')
    
    plt.xticks(X_axis, procs)
    plt.xlabel("MPI Processes")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()

def plotCommunicationPercentage(jacobiTime, seidelTime, redBlackTime, size):
    plotTitle = f"Communication Percentage (over total time) - Size: {size} - Iterations: 256"
    outFilePath = f"outFiles/plots/extras/heat_transfer_communication_analysis_{size}.png"

    procs = ['8','16','32','64']

    X_axis = np.arange(len(procs))

    jacobiComm, _ ,_, jacobiTotal = zip(*jacobiTime[3:])
    seidelComm, _ ,_, seidelTotal = zip(*seidelTime[3:])
    redBlackComm, _ ,_, redBlackTotal = zip(*redBlackTime[3:])

    jacobiCommPerc = []
    redBlackCommPerc = []
    seidelCommPerc = []
    for i in range(len(jacobiComm)):
        jacobiCommPerc.append(jacobiComm[i]/jacobiTotal[i])
        seidelCommPerc.append(seidelComm[i]/seidelTotal[i])
        redBlackCommPerc.append(redBlackComm[i]/redBlackTotal[i])

    offset = -0.22
    plt.bar(x=X_axis+offset, height=jacobiCommPerc, width=0.2, color="blue", bottom=0, label="Jacobi", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=seidelCommPerc, width=0.2, color="green", bottom=0, label="Gauss-Seidel SOR", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=redBlackCommPerc, width=0.2, color="red", bottom=0, label="Red-Black SOR", edgecolor='black')

    plt.xticks(X_axis, procs)
    plt.xlabel("MPI Processes")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()


def plotCommonTimeAnalysis(jacobiTime, seidelTime, redBlackTime, size):
    plotTitle = f"Computation Comparisson - Size: {size} - Iterations: 256"
    outFilePath = f"outFiles/plots/extras/heat_transfer_computation_analysis_{size}.png"

    procs = ['8','16','32','64']

    f = plt.figure()
    f.set_figwidth(8)
    f.set_figheight(5)
    f.tight_layout()


    X_axis = np.arange(len(procs))

    jacobiComm, jacobiComp ,_, jacobiTotal = zip(*jacobiTime[3:])
    seidelComm, seidelComp ,_, seidelTotal = zip(*seidelTime[3:])
    redBlackComm, redBlackComp ,_, redBlackTotal = zip(*redBlackTime[3:])

    offset = -0.22
    plt.bar(x=X_axis+offset, height=jacobiTotal, width=0.2, color="#1100FF", bottom=0, label="Jacobi Total", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=seidelTotal, width=0.2, color="#00D91B", bottom=0, label="Gauss-Seidel SOR Total", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=redBlackTotal, width=0.2, color="#FF0003", bottom=0, label="Red-Black SOR Total", edgecolor='black')

    offset = -0.22
    plt.bar(x=X_axis+offset, height=jacobiComp, width=0.2, color="#9000FF", bottom=0, label="Jacobi Computation", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=seidelComp, width=0.2, color="#00D987", bottom=0, label="Gauss-Seidel SOR Computation", edgecolor='black')
    offset += 0.22
    plt.bar(x=X_axis+offset, height=redBlackComp, width=0.2, color="#FF7C00", bottom=0, label="Red-Black SOR Computation", edgecolor='black')

    plt.xticks(X_axis, procs)
    plt.xlabel("MPI Processes")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()


def plotSpeedup(jacobiSpeedup, seidelSpeedup, redBlackSpeedup, size):
    plotTitle = f"Heat Trasnfer Methods Speedup - Size: {size} - Iterations: 256"
    outFilePath = f"outFiles/plots/speedup/heat_transfer_{size}_speedup.png"

    procs = ['1','2','4','8','16','32','64']

    f = plt.figure()
    f.set_figwidth(6.5)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(procs))

    plt.plot(X_axis, jacobiSpeedup, color="blue", marker='o', label="Jacobi")
    plt.plot(X_axis, seidelSpeedup, color="green", marker='o', label="Gauss-Seidel SOR")
    plt.plot(X_axis, redBlackSpeedup, color="red", marker='o', label="Red-Black SOR")

    plt.xticks(X_axis, procs)
    plt.xlabel("MPI Processes")
    plt.ylabel("Speedup")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()

def plotScalingComparisson(jacobiTime, seidelTime, redBlackTime, size, numberOfProcs):
    plotTitle = f"Heat Transfer Methods Comparisson - Size: {size} - Iterations: 256\nMPI Processes: {numberOfProcs}"
    outFilePath = f"outFiles/plots/scaling/heat_transfer_comparisson_{numberOfProcs}_{size}.png"

    algorithms = ["Jacobi", "Gauss-Seidel SOR", "Red-Black SOR"]

    f = plt.figure()
    f.set_figwidth(6.5)
    f.set_figheight(5)
    f.tight_layout()

    X_axis = np.arange(len(algorithms))

    (jacobiComm, jacobiComp, _, jacobiTotal) = jacobiTime
    (seidelComm, seidelComp, _, seidelTotal) = seidelTime
    (redBlackComm, redBlackComp, _, redBlackTotal) = redBlackTime

    plt.bar(x=X_axis[0], height=jacobiTime, width=0.2, color="#1100FF", bottom=0, label="Jacobi Total", edgecolor='black')
    plt.bar(x=X_axis[1], height=seidelTime, width=0.2, color="#00D91B", bottom=0, label="Gauss-Seidel SOR Total", edgecolor='black')
    plt.bar(x=X_axis[2], height=redBlackTime, width=0.2, color="#FF0003", bottom=0, label="Red-Black SOR Total", edgecolor='black')

    plt.bar(x=X_axis[0], height=jacobiComp, width=0.2, color="#9000FF", bottom=0, label="Jacobi Computation", edgecolor='black')
    plt.bar(x=X_axis[1], height=seidelComp, width=0.2, color="#00D987", bottom=0, label="Gauss-Seidel SOR Computation", edgecolor='black')
    plt.bar(x=X_axis[2], height=redBlackComp, width=0.2, color="#FF7C00", bottom=0, label="Red-Black SOR Computation", edgecolor='black')


    plt.xticks(X_axis, algorithms)
    plt.xlabel("Algorithm")
    plt.ylabel("Time (in seconds)")
    plt.title(plotTitle)
    plt.legend()
    plt.savefig(outFilePath)
    plt.close()

def main():
    jacobiTime2048, jacobiTime4096, jacobiTime6144, jacobiSpeedup2048, jacobiSpeedup4096, jacobiSpeedup6144 = returnAlgorithmResults("Jacobi")
    seidelTime2048, seidelTime4096, seidelTime6144, seidelSpeedup2048, seidelSpeedup4096, seidelSpeedup6144 = returnAlgorithmResults("GaussSeidelSOR")
    redBlackTime2048, redBlackTime4096, redBlackTime6144, redBlackSpeedup2048, redBlackSpeedup4096, redBlackSpeedup6144 = returnAlgorithmResults("RedBlackSOR")
    # plotTimeAnalysis(timeArray=jacobiTime2048, algoName="Jacobi", size=2048)
    # plotTimeAnalysis(timeArray=jacobiTime4096, algoName="Jacobi", size=4096)
    # plotTimeAnalysis(timeArray=jacobiTime6144, algoName="Jacobi", size=6144)

    # plotTimeAnalysis(timeArray=seidelTime2048, algoName="Gauss-Seidel SOR", size=2048)
    # plotTimeAnalysis(timeArray=seidelTime4096, algoName="Gauss-Seidel SOR", size=4096)
    # plotTimeAnalysis(timeArray=seidelTime6144, algoName="Gauss-Seidel SOR", size=6144)

    # plotTimeAnalysis(timeArray=redBlackTime2048, algoName="Red-Black SOR", size=2048)
    # plotTimeAnalysis(timeArray=redBlackTime4096, algoName="Red-Black SOR", size=4096)
    # plotTimeAnalysis(timeArray=redBlackTime6144, algoName="Red-Black SOR", size=6144)

    plotCommunicationPercentage(jacobiTime=jacobiTime2048, seidelTime=seidelTime2048, redBlackTime=redBlackTime2048, size=2048)
    plotCommunicationPercentage(jacobiTime=jacobiTime4096, seidelTime=seidelTime4096, redBlackTime=redBlackTime4096, size=4096)
    plotCommunicationPercentage(jacobiTime=jacobiTime6144, seidelTime=seidelTime6144, redBlackTime=redBlackTime6144, size=6144)

    plotCommonTimeAnalysis(jacobiTime=jacobiTime2048, seidelTime=seidelTime2048, redBlackTime=redBlackTime2048, size=2048)
    plotCommonTimeAnalysis(jacobiTime=jacobiTime4096, seidelTime=seidelTime4096, redBlackTime=redBlackTime4096, size=4096)
    plotCommonTimeAnalysis(jacobiTime=jacobiTime6144, seidelTime=seidelTime6144, redBlackTime=redBlackTime6144, size=6144)

    plotSpeedup(jacobiSpeedup=jacobiSpeedup2048, seidelSpeedup=seidelSpeedup2048, redBlackSpeedup=redBlackSpeedup2048, size=2048)
    plotSpeedup(jacobiSpeedup=jacobiSpeedup4096, seidelSpeedup=seidelSpeedup4096, redBlackSpeedup=redBlackSpeedup4096, size=4096)
    plotSpeedup(jacobiSpeedup=jacobiSpeedup6144, seidelSpeedup=seidelSpeedup6144, redBlackSpeedup=redBlackSpeedup6144, size=6144)

    for i,j,k,procs in zip(jacobiTime2048[3:], seidelTime2048[3:], redBlackTime2048[3:], [8,16,32,64]):
        plotScalingComparisson(i, j, k, 2048, procs)

    for i,j,k,procs in zip(jacobiTime4096[3:], seidelTime4096[3:], redBlackTime4096[3:], [8,16,32,64]):
        plotScalingComparisson(i, j, k, 4096, procs)

    for i,j,k,procs in zip(jacobiTime6144[3:], seidelTime6144[3:], redBlackTime6144[3:], [8,16,32,64]):
        plotScalingComparisson(i, j, k, 6144, procs)

    
if __name__ == "__main__":
    main()