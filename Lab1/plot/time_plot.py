import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

x_Axis = [1,2,4,6,8]
size_64_time = []
size_1024_time  = []
size_4096_time  = []


fp = open("results.out")
line = fp.readline()

while line:
    tokens = line.split()
    if (int(tokens[2]) == 64):
        size_64_time.append(float(tokens[6]))
        
    elif (int(tokens[2]) == 1024):
        size_1024_time.append(float(tokens[6]))

    elif (int(tokens[2]) == 4096):
        size_4096_time.append(float(tokens[6]))
        
    print(tokens[2])

    line = fp.readline()

fp.close()

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Number of Threads")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(size_64_time) - 0.05 * min(size_64_time), max(size_64_time) + 0.05 * max(size_64_time))
ax1.set_ylabel("Time (in seconds)")
line1 = ax1.plot(size_64_time, label="Time (in seconds)", color="red", marker='o')


plt.title(f"Conway's Game of Life - 1000 Steps - 64 x 64 Array")
plt.savefig("64.png", bbox_inches="tight")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(size_1024_time) - 0.20 * min(size_1024_time), max(size_1024_time) + 0.05 * max(size_1024_time))
ax1.set_ylabel("Time (in seconds)")
line1 = ax1.plot(size_1024_time, label="Time (in seconds)", color="red", marker='o')

plt.title(f"Conway's Game of Life - 1000 Steps - 1024 x 1024 Array")
plt.savefig("1024.png", bbox_inches="tight")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(size_4096_time) - 0.20 * min(size_4096_time), max(size_4096_time) + 0.05 * max(size_4096_time))
ax1.set_ylabel("Time (in seconds)")
line1 = ax1.plot(size_4096_time, label="Time (in seconds)", color="red", marker='o')

plt.title(f"Conway's Game of Life - 1000 Steps - 4096 x 4096 Array")
plt.savefig("4096.png", bbox_inches="tight")