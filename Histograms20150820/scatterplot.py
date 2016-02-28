"""
Simple scatter plot.
"""
import sys
import numpy as np
import matplotlib.pyplot as plt

xCoords = []
yCoords = []
#theFile = open('zoutwed101zorks.txt')
theFile = open('zoutwed102zorks.txt')
for line in theFile:
    if 'BAG' not in line: continue
    lineSplit = line.split()
    xCoords.append(lineSplit[1])
    yCoords.append(lineSplit[2])

plt.scatter(xCoords, yCoords)
plt.show()
