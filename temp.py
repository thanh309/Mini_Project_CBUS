from time import perf_counter as t
from cProfile import run
def main():

    with open('data/example5.txt', 'r') as f:
        N, K = tuple(map(int, f.readline().split()))
        c = []

        for i in range(2*N + 1):
            c.append(list(map(int, f.readline().split())))

    a = t()

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

    route.append(0)
    load_list.append(0)


    route_index = dict()
    for i, v in enumerate(route):
        route_index[v] = i
    


    # Evaluation function
    def route_cost(route) -> int:
        result = 0
        
        for i in range(2*N - 1):
            from_loc = route[i]
            to_loc = route[i + 1]
            result += c[from_loc][to_loc]

        result += c[route[-1]][0]
        result += c[0][route[0]]
        return result


    def precedence_violated(i_cand: int, i_swap: int) -> bool:
        if route[i_cand] <= N:
            return i_swap > route_index[route[i_cand] + N]
        return i_swap < route_index[route[i_cand] - N]


    def capacity_violated(i: int, j: int) -> bool:
        i, j = sorted((i, j))
        i_val, j_val = route[i], route[j]
        if (i_val <= N and j_val <= N) or (i_val > N and j_val > N):
            return False

        if i_val <= N:
            for loc in range(i, j):
                if load_list[loc] - 2 < 0:
                    return True

        for loc in range(i, j):
            if load_list[loc] + 2 > K:
                return True
        return False


    def delta_objective(i_cand: int , i_swap: int) -> int:
        '''Change of objective value when swapping location index `i_cand` with 
        location index `i_swap` in the route.'''

        if precedence_violated(i_cand, i_swap) or capacity_violated(i_cand, i_swap):
            return 0

        if abs(i_cand-i_swap) == 1:
            i_cand, i_swap = sorted((i_cand, i_swap))
            return c[route[i_cand-1]][route[i_swap]] + c[route[i_cand]][route[i_swap+1]] - c[route[i_cand-1]][route[i_cand]] - c[route[i_swap]][route[i_swap+1]]
    
        return c[route[i_cand-1]][route[i_swap]] + c[route[i_swap]][route[i_cand+1]] + c[route[i_swap-1]][route[i_cand]] + c[route[i_cand]][route[i_swap+1]]\
            - c[route[i_cand-1]][route[i_cand]] - c[route[i_cand]][route[i_cand+1]] - c[route[i_swap-1]][route[i_swap]] - c[route[i_swap]][route[i_swap+1]]
    
    def update_load_list(i: int, j: int) -> None:
        i, j = sorted((i, j))
        i_val, j_val = route[i], route[j]
        if (i_val <= N and j_val <= N) or (i_val > N and j_val > N):
            return

        if i_val <= N:
            for loc in range(i, j):
                load_list[loc] = load_list[loc] - 2
            return

        for loc in range(i, j):
            load_list[loc] = load_list[loc] + 2
        return

    for ITER in range(5):

        for pickup in range(1, N + 1):

            index_pickup = route_index[pickup]
            index_dropoff = route_index[pickup + N]

            best = 0
            index_swap = -1

            for index_cand in range(1, index_dropoff):
                if index_pickup == index_cand:
                    continue
                delta = delta_objective(index_cand, index_pickup)
                if delta < best:
                    best = delta
                    index_swap = index_cand

            if index_swap == -1:
                continue

            swap = route[index_swap]
            route_index[swap], route_index[pickup] = index_pickup, index_swap
            update_load_list(index_swap, index_pickup)
            route[index_pickup], route[index_swap] = route[index_swap], route[index_pickup]



        for dropoff in range(N + 1, 2*N + 1):

            index_dropoff = route_index[dropoff]
            index_pickup = route_index[dropoff - N]

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

            swap = route[index_swap]
            route_index[swap], route_index[dropoff] = index_dropoff, index_swap
            update_load_list(index_swap, index_dropoff)
            route[index_dropoff], route[index_swap] = route[index_swap], route[index_dropoff]



    print(N)
    print(*route[1:-1])
    print(t() - a)
    print(route_cost(route[1:-1]))


if __name__ == '__main__':
    # run('main()')
    main()