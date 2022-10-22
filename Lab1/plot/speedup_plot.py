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

Tserial_64 = size_64_time[0]
Tserial_1024 = size_1024_time[0]
Tserial_4096 = size_4096_time[0]

speedup_64 = []
speedup_1024 = []
speedup_4096 = []

for i in range(len(size_64_time)):
    speedup_64.append(Tserial_64/size_64_time[i])
    speedup_1024.append(Tserial_1024/size_1024_time[i])
    speedup_4096.append(Tserial_4096/size_4096_time[i])
    
fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Number of Threads")

xAx = np.arange(len(x_Axis))
ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
ax1.set_xticklabels(x_Axis, rotation=45)
ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
ax1.set_ylim(min(speedup_64) - 0.05 * min(speedup_64), max(speedup_64) + 0.05 * max(speedup_64))
ax1.set_ylabel("Speedup")
line1 = ax1.plot(speedup_64, label="Speedup", color="red", marker='o')


plt.title(f"Conway's Game of Life - 1000 Steps - 64 x 64 Array")
plt.savefig("speedup_64.png", bbox_inches="tight")

# xAx = np.arange(len(x_Axis))
# ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
# ax1.set_xticklabels(x_Axis, rotation=45)
# ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
# ax1.set_ylim(min(speedup_1024) - 0.20 * min(speedup_1024), max(speedup_1024) + 0.05 * max(speedup_1024))
# ax1.set_ylabel("Speedup")
# line1 = ax1.plot(speedup_1024, label="Speedup", color="red", marker='o')

# plt.title(f"Conway's Game of Life - 1000 Steps - 1024 x 1024 Array")
# plt.savefig("speedup_1024.png", bbox_inches="tight")

# xAx = np.arange(len(x_Axis))
# ax1.xaxis.set_ticks(np.arange(0, len(x_Axis), 1))
# ax1.set_xticklabels(x_Axis, rotation=45)
# ax1.set_xlim(-0.5, len(x_Axis) - 0.5)
# ax1.set_ylim(min(speedup_4096) - 0.20 * min(speedup_4096), max(speedup_4096) + 0.05 * max(speedup_4096))
# ax1.set_ylabel("Speedup")
# line1 = ax1.plot(speedup_4096, label="Speedup", color="red", marker='o')

# plt.title(f"Conway's Game of Life - 1000 Steps - 4096 x 4096 Array")
# plt.savefig("speedup_4096.png", bbox_inches="tight")