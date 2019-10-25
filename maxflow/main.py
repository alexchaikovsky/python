import edmondskarp
import goldberg
import time
import matplotlib.pyplot as plt
from random import randrange
from mpl_toolkits import mplot3d
#from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import timeit

def GenerateCapacityMatrix(nodesNum, density):
    M = []
    nodeInput = [0 for i in range(nodesNum)]
    emptyNum = 0
    constZ = int(nodesNum / 2)
    for i in range(nodesNum - 1):
        line = []
        emptyNum += 1
        for j in range(nodesNum - 1):
            v = randrange((-1) * density,10)
            if v > 0:
                r = randrange(1,50)
            else:
                r = 0
            if (j < i):
                if (M[j][i] != 0):
                    r = 0
            else:
                nodeInput[j] += r
            line.append(r)
        for j in range(emptyNum):
            line[j] = 0
        line[0] = 0
        line[i] = 0
        last = randrange((-1) * nodesNum * 5, nodesNum * 5)
        if last > 0:
            line.append(last)
        else:
            line.append(0)
        if emptyNum < nodesNum/2:
            constZ += 1
        else:
            constZ -= 2
        for j in range(constZ + emptyNum, nodesNum):
            line[j] = 0
        M.append(line)
    lastLine = [0 for i in range(nodesNum)]
    M.append(lastLine)
    if (sum(M[i][nodesNum-1]) for i in range(nodesNum)) == 0:
        for j in range(nodesNum):
            if sum(M[j]) > 0:
                M[j][nodesNum-1] = range(1, nodesNum * 5)

    #for str in M:
    #    print(str)
    edgesCount = 0
    for i in range(nodesNum):
        for j in range(nodesNum):
            if M[i][j] != 0:
                edgesCount += 1
    print(edgesCount)
    return M, edgesCount


def GenerateRMatrix(nodesNum, d):
    M = []
    emptyNum = 0
    nodeInput = [0 for i in range(nodesNum)]
    for i in range(nodesNum - 1):
        line = []
        emptyNum += 1
        line.append(0)
        for j in range(1,nodesNum):
            r = randrange((-1) * 50 * int(d/10), 50)
            if (r < 0):
                r = 0
            else:
                r = randrange(1, 50)
            nodeInput[j] += r
            line.append(r)
        if (nodeInput[i] > 0 and sum(line) == 0 and emptyNum < nodesNum - 1):
            line[nodesNum-1] = randrange(1, 50)
            #print("ff")
        line[0] = 0

        M.append(line)
        for j in range(0,emptyNum):
            M[i][j] = 0
    #print(nodeInput)
    #if (nodeInput[nodesNum - 1] == 0):
    #    for i in range(nodesNum - 1, 0):
    #        if nodeInput[i] > 0:
    #            M[i][nodesNum-1] = randrange(1,50)
    #            break
    if sum(M[0]) == 0:
        M[0][nodesNum-1] = randrange(1,50)
    lastLine = [0 for i in range(nodesNum)]
    M.append(lastLine)
    #for str in M:
    #   print(str)
    edgesCount = 0
    for i in range(nodesNum):
        for j in range(nodesNum):
            if M[i][j] != 0:
                edgesCount += 1
    print(edgesCount)
    return M, edgesCount

f = open("uff44.txt", "w")
#nodesNum = int(input())
testN = 250
goldbergTime = []
edkarpTime = []
numberOfNodes = []
densityC = 500
step = 10
densityStep = 5
#density = [0 for i in range(testN*10 - 5)]
density = []
for nodesNum in range(10,testN, step):
    print(nodesNum)
    #C = GenerateCapacityMatrix(nodesNum)
#C = GenCapM(nodesNum)
    print("------------")
    G = GenerateRMatrix(nodesNum, 200)
    source = 0
    sink = nodesNum - 1
    #numberOfNodes.append(nodesNum)
    for densityCoef in range(0,densityC,densityStep):
        #G, edgesCount = GenerateRMatrix(nodesNum, densityCoef)
        G, edgesCount = GenerateCapacityMatrix(nodesNum,densityCoef)
        #density.append(densityCoef)
        numberOfNodes.append(nodesNum)
        start_time = time.time()
        gFlow, gTime = goldberg.MaxFlow(G, source, sink)
        end_time = time.time()
        #gTime = end_time - start_time
        density.append(edgesCount)
        #print(rTime, max_flow_value)
        goldbergTime.append(gTime)

        start_time = time.time()
        edFlow = edmondskarp.max_flow(G, source, sink)
        end_time = time.time()
        rTime = end_time - start_time
        #print(rTime, max_flow_value)
        edkarpTime.append(rTime)
        print(gFlow, edFlow,gTime, rTime)

        f.write(str(edgesCount) + ";" + str(nodesNum) + ";" + str(gTime) + ";" + str(rTime) + "\n")



f.close()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.plot_trisurf(numberOfNodes,density,goldbergTime)
ax.set_xlabel('Количество вершин, V')
ax.set_ylabel('Количество ребер, E')
ax.set_zlabel('Время выполнения, t')
zpos = [0 for i in range(int((testN - 10) / step) * int(densityC / densityStep))]
dx = np.ones((int((testN - 10) / step)) * int(densityC/densityStep))
dy = np.ones((int((testN - 10) / step)) * int(densityC / densityStep))
#dz = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
ax.bar3d(numberOfNodes, density, zpos, dx, dy, goldbergTime, color='#00ceaa')
plt.show()


a = int(input())


start_time = time.time()
max_flow_value = goldberg.MaxFlow(C, source, sink)
end_time = time.time() - start_time
print("Алгоритм Голдберга. Плотный граф. Время выполнения:", end_time)
print("Максимальный поток: ", max_flow_value)

start_time = time.time()
max_flow_value = edmondskarp.max_flow(C, source, sink)
print("Алгоритм Эдмондса-Карпа. Плотный граф. Время выполнения:", time.time() - start_time)
print("Максимальный поток: ", max_flow_value)

print("---------------------------------------------")

start_time = time.time()
max_flow_value = goldberg.MaxFlow(G, source, sink)
print("Алгоритм Голдберга. Разреженный граф. Время выполнения:", time.time() - start_time)
print("Максимальный поток: ", max_flow_value)

start_time = time.time()
max_flow_value = edmondskarp.max_flow(G, source, sink)
print("Алгоритм Эдмондса-Карпа. Разреженный граф. Время выполнения:", time.time() - start_time)
print("Максимальный поток: ", max_flow_value)

