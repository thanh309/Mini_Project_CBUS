def solve(N: int, K: int, c: 'list[list]') -> list:

    load = 0
    unvisited = list(range(1, 2*N + 1))
    route = [0]
    load_list = [0]

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
                load_list.append(load)
            else:
                load -= 1
                load_list.append(load)
            continue

        else:

            cand = filter(lambda x: (x - N in route[1:]), unvisited)
            nearest_loc, nearest_dist = -1, float('inf')

            for loc in cand:
                if c[route[-1]][loc] < nearest_dist:
                    nearest_loc = loc
                    nearest_dist = c[route[-1]][loc]
            route.append(nearest_loc)
            unvisited.remove(nearest_loc)
            load -= 1
            load_list.append(load)
            continue


    # cands = list(range(1, N + 1))
    # random.shuffle(cands)
    # route = [0]
    # for pickup_loc in cands:
    #     route.append(pickup_loc)
    #     route.append(pickup_loc + N)
    #     load_list.extend([1, 0])

    route.append(0)
    load_list.append(0)


    route_index = dict()
    for i, v in enumerate(route):
        route_index[v] = i

    def precedence_violated(i: int, i_prime: int) -> bool:
        if route[i] <= N:
            return i_prime > route_index[route[i] + N]
        return i_prime < route_index[route[i] - N]


    def capacity_violated(i: int, j: int) -> bool:
        i, j = sorted((i, j))
        x_i, x_j = route[i], route[j]
        if (x_i <= N and x_j <= N) or (x_i > N and x_j > N):
            return False

        if x_i <= N:
            for loc in range(i, j):
                if load_list[loc] - 2 < 0:
                    return True
        else:
            for loc in range(i, j):
                if load_list[loc] + 2 > K:
                    return True
        return False


    def delta_objective(i: int , i_prime: int) -> int:
        '''Change of objective value when swapping location index `i` with 
        location index `i_prime` in the route.'''

        if precedence_violated(i, i_prime) or capacity_violated(i, i_prime):
            return 0

        if abs(i-i_prime) == 1:
            i, i_prime = sorted((i, i_prime))
            return c[route[i-1]][route[i_prime]] + c[route[i]][route[i_prime+1]] - c[route[i-1]][route[i]] - c[route[i_prime]][route[i_prime+1]]
    
        return c[route[i-1]][route[i_prime]] + c[route[i_prime]][route[i+1]] + c[route[i_prime-1]][route[i]] + c[route[i]][route[i_prime+1]]\
            - c[route[i-1]][route[i]] - c[route[i]][route[i+1]] - c[route[i_prime-1]][route[i_prime]] - c[route[i_prime]][route[i_prime+1]]
    
    def update_load_list(i: int, j: int) -> None:
        i, j = sorted((i, j))
        x_i, x_j = route[i], route[j]
        if (x_i <= N and x_j <= N) or (x_i > N and x_j > N):
            return

        if x_i <= N:
            for loc in range(i, j):
                load_list[loc] = load_list[loc] - 2
            return

        for loc in range(i, j):
            load_list[loc] = load_list[loc] + 2
        return

    for _ in range(100):
        improved = False
        for pickup in range(1, N + 1):

            index_pickup = route_index[pickup]
            index_delivery = route_index[pickup + N]

            best = 0
            index_swap = -1

            for index_cand in range(1, index_delivery):
                if index_pickup == index_cand:
                    continue
                delta = delta_objective(index_cand, index_pickup)
                if delta < best:
                    best = delta
                    index_swap = index_cand
                    improved = True

            if index_swap == -1:
                continue

            swap = route[index_swap]
            route_index[swap], route_index[pickup] = index_pickup, index_swap
            update_load_list(index_swap, index_pickup)
            route[index_pickup], route[index_swap] = route[index_swap], route[index_pickup]



        for delivery in range(N + 1, 2*N + 1):

            index_delivery = route_index[delivery]
            index_pickup = route_index[delivery - N]

            best = 0
            index_swap = -1

            for index_cand in range(index_pickup + 1, 2*N + 1):
                if index_delivery == index_cand:
                    continue
                delta = delta_objective(index_cand, index_delivery)
                if delta < best:
                    best = delta
                    index_swap = index_cand
                    improved = True
            
            if index_swap == -1:
                continue

            swap = route[index_swap]
            route_index[swap], route_index[delivery] = index_delivery, index_swap
            update_load_list(index_swap, index_delivery)
            route[index_delivery], route[index_swap] = route[index_swap], route[index_delivery]

        if not improved:
            break
    return route[1:-1]