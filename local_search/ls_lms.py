def main():

    N, K = tuple(map(int, input().split()))
    c = []

    for i in range(2*N + 1):
        c.append(list(map(int, input().split())))


    load = 0
    unvisited = list(range(1, 2*N + 1))
    route = [0]

    while unvisited:

        if load < K:

            cand = filter(lambda x: (x <= N or x - N in route[1:]), unvisited)
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

    route.append(0)


    # Evaluation function
    # def route_cost(route) -> int:
    #     result = 0
        
    #     for i in range(2*N - 1):
    #         from_loc = route[i]
    #         to_loc = route[i + 1]
    #         result += c[from_loc][to_loc]

    #     result += c[route[-1]][0]
    #     result += c[0][route[0]]
    #     return result


    def constraint_violated() -> bool:
        cur_load = 0
        for i_loc in range(1, 2*N + 1):
            if route[i_loc] <= N:
                cur_load += 1
                if cur_load > K:
                    return True
            else:
                if route[i_loc] - N not in route[1:i_loc]:
                    return True
                cur_load -= 1
        return False


    def delta_objective(i: int , j: int) -> int:
        '''Change of objective value when swapping location index `i` with 
        location index `j` in the route.'''

        route[i], route[j] = route[j], route[i]
        if constraint_violated():
            route[i], route[j] = route[j], route[i]
            return 0
        route[i], route[j] = route[j], route[i]
        
        if abs(i-j) == 1:
            i, j = sorted((i, j))
            return c[route[i-1]][route[j]] + c[route[i]][route[j+1]] - c[route[i-1]][route[i]] - c[route[j]][route[j+1]]
    
        return c[route[i-1]][route[j]] + c[route[j]][route[i+1]] + c[route[j-1]][route[i]] + c[route[i]][route[j+1]]\
            - c[route[i-1]][route[i]] - c[route[i]][route[i+1]] - c[route[j-1]][route[j]] - c[route[j]][route[j+1]]


    for ITER in range(1):

        for pickup in range(1, N + 1):

            index_pickup = route.index(pickup)
            index_dropoff = route.index(pickup + N)

            best = 0
            index_swap = -1

            for index_cand in range(1, index_dropoff):
                if index_pickup == index_cand:
                    continue
                delta = delta_objective(index_cand, index_pickup)
                if delta < best:
                    best = delta
                    index_swap = index_cand
                    break
            
            if index_swap == -1:
                continue
            route[index_pickup], route[index_swap] = route[index_swap], route[index_pickup]

        for dropoff in range(N + 1, 2*N + 1):

            index_dropoff = route.index(dropoff)
            index_pickup = route.index(dropoff - N)

            best = 0
            index_swap = -1

            for index_cand in range(index_pickup + 1, 2*N + 1):
                if index_dropoff == index_cand:
                    continue
                delta = delta_objective(index_cand, index_dropoff)
                if delta < best:
                    best = delta
                    index_swap = index_cand
            
            if index_swap == -1:
                continue
            route[index_dropoff], route[index_swap] = route[index_swap], route[index_dropoff]


    print(N)
    print(*route[1:-1])

if __name__ == '__main__':
    main()