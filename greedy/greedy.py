# Greedy

with open('data/example3.txt', 'r') as f:
    N, K = tuple(map(int, f.readline().split()))
    c = []

    for i in range(2*N + 1):
        c.append(list(map(int, f.readline().split())))
        # Modify the cost matrix: add the auxiliary point 2N + 1,
        # which has the same geographical location as point 0
        c[i].append(c[i][0])

    c.append(c[0])


load = 0
unvisited = list(range(1, 2*N + 1))
route = [0]

while unvisited:


    if load < K:

        cand = list(filter(lambda x: (x <= N), unvisited))
        nearest_loc, nearest_dist = -1, float('inf')
        

        if cand:
            for loc in cand:
                if c[route[-1]][loc] < nearest_dist:
                    nearest_loc = loc
                    nearest_dist = c[route[-1]][loc]
            route.append(nearest_loc)
            unvisited.remove(nearest_loc)
            load += 1
            continue


        else:
            for loc in unvisited:
                if c[route[-1]][loc] < nearest_dist:
                    nearest_loc = loc
                    nearest_dist = c[route[-1]][loc]
            route.append(nearest_loc)
            unvisited.remove(nearest_loc)
            load -= 1
            continue


    else:

        cand = list(filter(lambda x: (x - N in route[1:]), unvisited))
        nearest_loc, nearest_dist = -1, float('inf')

        for loc in cand:
            if c[route[-1]][loc] < nearest_dist:
                nearest_loc = loc
                nearest_dist = c[route[-1]][loc]
        route.append(nearest_loc)
        unvisited.remove(nearest_loc)
        load -= 1
        continue

result = route[1:]
print(N)
print(*result)