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
    workloadTitle = ""

    filename = f"{type}_{size}_{workload}.out"

    fp = open(filename)
    line = fp.readline()

    while line:
        if (line.strip(" ").startswith("Nthreads:") and line.split()[5] == workload):
            print("hi")
            throughput = float(line.split()[7])
            throughputList.append(throughput)
            
        line = fp.readline()

    fp.close()
    
    return throughputList



def parser() -> str:
    pass

def plotThroughput(outFilePath:str, title:str, workload:str):
    threads = ['1', '2', '4', '8', '16', '32', '64', '128']
    

def main():
    list = logger("cgl",'100/0/0',1024)
    print(list)

if __name__ == "__main__":
    main()