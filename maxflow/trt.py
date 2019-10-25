from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np


f = open("uff2.txt", "r")
#nodesNum = int(input())
testN = 500
goldbergTime = []
edkarpTime = []
numberOfNodes = []
densityC = 200
step = 10
#density = [0 for i in range(testN*10 - 5)]
density = []

for line in f:
    lineAr = line.split(";")
    numberOfNodes.append(int(lineAr[1]))
    density.append((int(lineAr[0])))
    goldbergTime.append(float(lineAr[2])/10)
    #lineAr[3] = line[3][:-1]
    print(lineAr)
    edkarpTime.append(float(lineAr[3]))

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.plot_trisurf(numberOfNodes,density,goldbergTime)
ax.set_xlabel('Количество вершин, V')
ax.set_ylabel('Количество ребер, E')
ax.set_zlabel('Время выполнения, t')
zpos = [0 for i in range(int((testN - 10) / step) * int(densityC / 5))]
dx = np.ones((int((testN - 10) / step)) * int(densityC / 5))
dy = np.ones((int((testN - 10) / step)) * int(densityC / 5))
#dz = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
#ax.bar3d(numberOfNodes, density, zpos, dx, dy, goldbergTime, color='#00ceaa')
ax.bar3d(numberOfNodes, density, zpos, dx, dy, edkarpTime, color='#00ceaa')
plt.show()