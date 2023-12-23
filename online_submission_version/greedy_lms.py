# Greedy 2

def main():

    N, K = tuple(map(int, input().split()))
    c = []

    for _ in range(2*N + 1):
        c.append(list(map(int, input().split())))

    load = 0
    unvisited = list(range(1, 2*N + 1))
    route = [0]

    while unvisited:

        if load < K:

            cand = list(filter(lambda x: (x <= N or x - N in route[1:]), unvisited))
            nearest_loc, nearest_dist = -1, float('inf')

            for loc in cand:
                if c[route[-1]][loc] < nearest_dist:
                    nearest_loc = loc
                    nearest_dist = c[route[-1]][loc]
            route.append(nearest_loc)
            unvisited.remove(nearest_loc)
            if nearest_loc <= N:
                load += 1
            else:
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


if __name__ == '__main__':
    main()