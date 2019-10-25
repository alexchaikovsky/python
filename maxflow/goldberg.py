import time

def MaxFlow(C, s, t):
    n = len(C)
    F = [[0] * n for i in range(n)]
    height = [0] * n
    excess = [0] * n
    excess[s] = sum(C[s])
    seen = [0] * n
    nodelist = [i for i in range(n) if i != s and i != t]


    def push(u, v):
        send = min(excess[u], C[u][v] - F[u][v])
        F[u][v] += send
        F[v][u] -= send
        excess[u] -= send
        excess[v] += send

    def relabel(u):
        min_height = float('inf')
        for v in range(n):
            if C[u][v] - F[u][v] > 0:
                min_height = min(min_height, height[v])
                height[u] = min_height + 1

    def discharge(u):
        while excess[u] > 0:
            if seen[u] < n:
                v = seen[u]
                if C[u][v] - F[u][v] > 0 and height[u] > height[v]:
                    push(u, v)
                else:
                    seen[u] += 1
            else:
                relabel(u)
                seen[u] = 0

    height[s] = n

    for v in range(n):
        push(s, v)
    disttime = 0
    stime = time.time()
    p = 0
    while p < len(nodelist):
        u = nodelist[p]
        old_height = height[u]
        distart = time.time()
        discharge(u)
        disttime += time.time() - distart
        if height[u] > old_height:
            #lstart = time.time()
            nodelist.insert(0, nodelist.pop(p))
            #listtime += time.time() - lstart
            p = 0
        else:
            p += 1
    #print(disttime)
    endtime = time.time() - stime
    return sum(F[s]), endtime

