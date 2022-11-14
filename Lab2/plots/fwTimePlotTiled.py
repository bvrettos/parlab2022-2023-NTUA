import sys
import numpy as np
import matplotlib

import matplotlib.pyplot as plt

mode = "speedup"

threads = ['1','2','4','8','16','32','64']

tile1024_32 = []
tile1024_64 = []
tile1024_128 = []
tile1024_256 = []
tile1024_512 = []

tile2048_32 = []
tile2048_64 = []
tile2048_128 = []
tile2048_256 = []
tile2048_512 = []

tile4096_32 = []
tile4096_64 = []
tile4096_128 = []
tile4096_256 = []
tile4096_512 = []

fp = open("fwData/fw_tiled_collapse_all.out")
line = fp.readline()

while line:
    tokens = line.split(",")

    size = int(tokens[1])
    blocksize = int(tokens[2])
    time = float(tokens[3])

    if size == 1024:
        if blocksize == 32:
            tile1024_32.append(time)
        elif blocksize == 64:
            tile1024_64.append(time)
        elif blocksize == 128:
            tile1024_128.append(time)
        elif blocksize == 256:
            tile1024_256.append(time)
        elif blocksize == 512:
            tile1024_512.append(time)

    if size == 2048:
        if blocksize == 32:
            tile2048_32.append(time)
        elif blocksize == 64:
            tile2048_64.append(time)
        elif blocksize == 128:
            tile2048_128.append(time)
        elif blocksize == 256:
            tile2048_256.append(time)
        elif blocksize == 512:
            tile2048_512.append(time)

    if size == 4096:
        if blocksize == 32:
            tile4096_32.append(time)
        elif blocksize == 64:
            tile4096_64.append(time)
        elif blocksize == 128:
            tile4096_128.append(time)
        elif blocksize == 256:
            tile4096_256.append(time)
        elif blocksize == 512:
            tile4096_512.append(time)

    line = fp.readline()

fp.close()

speedup1024_32 = [tile1024_32[0] / x for x in tile1024_32]
speedup1024_64 = [tile1024_64[0] / x  for x in tile1024_64]
speedup1024_128 = [tile1024_128[0] / x for x in tile1024_128]
speedup1024_256 = [tile1024_256[0] / x for x in tile1024_256]
speedup1024_512 = [tile1024_512[0] / x for x in tile1024_512]

speedup2048_32 = [tile2048_32[0] / x for x in tile2048_32]
speedup2048_64 = [tile2048_64[0] / x for x in tile2048_64]
speedup2048_128 = [tile2048_128[0] / x for x in tile2048_128]
speedup2048_256 = [tile2048_256[0] / x for x in tile2048_256]
speedup2048_512 = [tile2048_512[0] / x for x in tile2048_512]

speedup4096_32 = [tile4096_32[0] / x for x in tile4096_32]
speedup4096_64 = [tile4096_64[0] / x for x in tile4096_64]
speedup4096_128 = [tile4096_128[0] / x for x in tile4096_128]
speedup4096_256 = [tile4096_256[0] / x for x in tile4096_256]
speedup4096_512 = [tile4096_512[0] / x for x in tile4096_512]

if mode == "time":
    for j in [1024, 2048, 4096]:
        path = f"fw_tiles_{j}.png"
        title = f"Floyd-Warshall - tile Implementation - Time - Size:{j}"
        legend = ['Block Size=32', 'Block Size=64', 'Block Size=128', 'Block Size=256', 'Block Size=512']

        if j == 1024:
            range = [tile1024_32, tile1024_64, tile1024_128, tile1024_256, tile1024_512]
        elif j == 2048:
            range = [tile2048_32, tile2048_64, tile2048_128, tile2048_256, tile2048_512]
        elif j == 4096:
            range = [tile4096_32, tile4096_64, tile4096_128, tile4096_256, tile4096_512]

        f= plt.figure()
        f.set_figwidth(8)
        f.set_figheight(6.5)
        f.tight_layout()

        X_axis = np.arange(len(threads))

        cnt= 0.05
        for idx, i in enumerate(range):
            plt.bar(X_axis + cnt , i, 0.1, align='edge', label=legend[idx])
            cnt+=0.1

        plt.xticks(X_axis + 0.3, threads)
        plt.xlabel("Number of Threads")
        plt.ylabel("Time (in seconds)")
        plt.title(title)
        plt.legend()
        plt.savefig(path)

elif mode == "speedup":
    for j in [1024, 2048, 4096]:
        path = f"fw_tiles_speedup_{j}.png"
        title = f"Floyd-Warshall - Tiled Implementation - Speedup - Size:{j}"
        legend = ['Block Size=32', 'Block Size=64', 'Block Size=128', 'Block Size=256', 'Block Size=512']

        if j == 1024:
            range = [speedup1024_32, speedup1024_64, speedup1024_128, speedup1024_256, speedup1024_512]
        elif j == 2048:
            range = [speedup2048_32, speedup2048_64, speedup2048_128, speedup2048_256, speedup2048_512]
        elif j == 4096:
            range = [speedup4096_32, speedup4096_64, speedup4096_128, speedup4096_256, speedup4096_512]

        f= plt.figure()
        f.set_figwidth(8)
        f.set_figheight(6.5)
        f.tight_layout()

        X_axis = np.arange(len(threads))

        cnt= 0.05
        for idx, i in enumerate(range):
            plt.plot(X_axis + cnt , i, label=legend[idx], marker='o')

        plt.xticks(X_axis + 0.3, threads)
        plt.xlabel("Number of Threads")
        plt.ylabel("Speedup")
        plt.title(title)
        plt.legend()
        plt.savefig(path)
    




