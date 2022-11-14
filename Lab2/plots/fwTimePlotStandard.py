import sys
import numpy as np
import matplotlib

import matplotlib.pyplot as plt

threads = ['1','2','4','8','16','32','64']
standard1024Values = []
standard2048Values = []
standard4096Values = []

fp = open("fwData/fw_standard_sandman.out")
line = fp.readline()

while line:
    tokens = line.split(",")

    tokens[2].replace("\n", "")

    if (int(tokens[1]) == 1024):
        standard1024Values.append(float(tokens[2]))
    elif (int(tokens[1]) == 2048):
        standard2048Values.append(float(tokens[2]))
    elif (int(tokens[1]) == 4096):
        standard4096Values.append(float(tokens[2]))
    line = fp.readline()

print(standard1024Values)
print(standard2048Values)
print(standard4096Values)

fp.close()

tSerial1024 = standard1024Values[0]
tSerial2048 = standard2048Values[0]
tSerial4096 = standard4096Values[0]

speedup1024 = []
speedup2048 = []
speedup4096 = []

for i in range(len(standard1024Values)):
    speedup1024.append(tSerial1024/standard1024Values[i])
    speedup2048.append(tSerial2048/standard2048Values[i])
    speedup4096.append(tSerial4096/standard4096Values[i])

print(speedup1024)
print(speedup2048)
print(speedup4096)

# fig = plt.figure(figsize = (9,5))

# # Standard - 1024 
# plt.bar(threads, standard1024Values, color= 'blue', width=0.4)

# plt.xlabel("Number of Threads")
# plt.ylabel("Time (in seconds)")
# plt.title("Floyd-Warshall Standard - 1024")
# plt.savefig("fw_standard_1024.png", bbox_inches="tight")

# # Standard - 2048 
# plt.bar(threads, standard2048Values, color= 'red', width=0.4)

# plt.xlabel("Number of Threads")
# plt.ylabel("Time (in seconds)")
# plt.title("Floyd-Warshall Standard - 2048")
# plt.savefig("fw_standard_2048.png", bbox_inches="tight")

# # Standard - 4096 
# plt.bar(threads, standard4096Values, color= 'purple', width=0.4)

# plt.xlabel("Number of Threads")
# plt.ylabel("Time (in seconds)")
# plt.title("Floyd-Warshall Standard - 4096")
# plt.savefig("fw_standard_4096.png", bbox_inches="tight")

fig, ax1 = plt.subplots()
ax1.grid(True)
ax1.set_xlabel("Number of Threads")

xAx = np.arange(len(threads))
ax1.xaxis.set_ticks(np.arange(0, len(threads), 1))
ax1.set_xticklabels(threads, rotation=45)
ax1.set_xlim(-0.5, len(threads) - 0.5)
ax1.set_ylim(min(speedup1024) - 0.05 * min(speedup1024), max(speedup1024) + 0.05 * max(speedup1024))
ax1.set_ylabel("Speedup")
line1 = ax1.plot(speedup1024, label="Speedup", color="blue", marker='o')


plt.title(f"Floyd-Warshall Standard - 1024 - Speedup")
plt.savefig("fw_speedup1024.png", bbox_inches="tight")

# fig, ax1 = plt.subplots()
# ax1.grid(True)
# ax1.set_xlabel("Number of Threads")

# xAx = np.arange(len(threads))
# ax1.xaxis.set_ticks(np.arange(0, len(threads), 1))
# ax1.set_xticklabels(threads, rotation=45)
# ax1.set_xlim(-0.5, len(threads) - 0.5)
# ax1.set_ylim(min(speedup2048) - 0.05 * min(speedup2048), max(speedup2048) + 0.05 * max(speedup2048))
# ax1.set_ylabel("Speedup")
# line1 = ax1.plot(speedup2048, label="Speedup", color="red", marker='o')


# plt.title(f"Floyd-Warshall Standard - 2048 - Speedup")
# plt.savefig("fw_speedup2048.png", bbox_inches="tight")

# fig, ax1 = plt.subplots()
# ax1.grid(True)
# ax1.set_xlabel("Number of Threads")

# xAx = np.arange(len(threads))
# ax1.xaxis.set_ticks(np.arange(0, len(threads), 1))
# ax1.set_xticklabels(threads, rotation=45)
# ax1.set_xlim(-0.5, len(threads) - 0.5)
# ax1.set_ylim(min(speedup4096) - 0.05 * min(speedup4096), max(speedup4096) + 0.05 * max(speedup4096))
# ax1.set_ylabel("Speedup")
# line1 = ax1.plot(speedup4096, label="Speedup", color="purple", marker='o')


# plt.title(f"Floyd-Warshall Standard - 4096 - Speedup")
# plt.savefig("fw_speedup4096.png", bbox_inches="tight")



