import random
MAX_BLOCK_LENGTH = 4

def main():
    
    N, K = tuple(map(int, input().split()))
    c = []

    for i in range(2*N + 1):
        c.append(list(map(int, input().split())))
        c[i].append(c[i][0])
    c.append(c[0])

    route = [0]
    load_list = [0]

    load = 0
    unvisited = list(range(1, 2*N + 1))

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


    def delta_cost(s: int, e: int, insert_pos: int, removing_delta: int) -> int:
        return removing_delta - c[route[insert_pos-1]][route[insert_pos]]\
            + c[route[insert_pos-1]][route[s]] + c[route[e]][route[insert_pos]]

    def check_cap(x: int) -> bool:
        return x <= K

    def capacity_violated(s: int, e: int, insert_pos: int) -> bool:
        if insert_pos > e:
            return capacity_violated(e + 1, insert_pos - 1, s)
        delta_load_inside = load_list[insert_pos - 1] - load_list[s - 1]
        delta_load_outside = 0
        for pos_inside in range(s, e + 1):
            if not check_cap(load_list[pos_inside] + delta_load_inside):
                return True
            if route[pos_inside] > N:
                delta_load_outside -= 1
            else:
                delta_load_outside += 1
        if not check_cap(max(load_list[insert_pos:s]) + delta_load_outside):
            return True
        return False

    def route_update(s: int, e: int, insert_pos: int) -> None:
        if insert_pos > e:
            route_update(e + 1, insert_pos - 1, s)
            return
        
        temp_load_list = {}
        delta_load_inside = load_list[insert_pos - 1] - load_list[s - 1]
        delta_load_outside = 0
        for pos_inside in range(s, e + 1):
            load_list[pos_inside] += delta_load_inside
            temp_load_list[pos_inside] = load_list[pos_inside]
            if route[pos_inside] > N:
                delta_load_outside -= 1
            else:
                delta_load_outside += 1
        for pos_outside in range(insert_pos, s):
            load_list[pos_outside] += delta_load_outside
            temp_load_list[pos_outside] = load_list[pos_outside]
        
        changed_node = []
        for pos in range(insert_pos, s):
            route_index[route[pos]] += e - s + 1
            load_list[route_index[route[pos]]] = temp_load_list[pos]
            changed_node.append(route[pos])
        for pos in range(s, e + 1):
            route_index[route[pos]] -= s - insert_pos
            load_list[route_index[route[pos]]] = temp_load_list[pos]
            changed_node.append(route[pos])
        
        for node in changed_node:
            route[route_index[node]] = node
        return
        

    cands = list(range(1, 2*N + 1))

    for _ in range(4):
        random.shuffle(cands)
        for cand in cands:

            # s, e: start and end of a block (index)
            s = route_index[cand]
            e_range = range(s, min(2*N, s + MAX_BLOCK_LENGTH - 1))
            move = tuple()
            for e in e_range:
                best_delta_cost = 0
                removing_delta = c[route[s-1]][route[e+1]] - c[route[s-1]][route[s]] - c[route[e]][route[e+1]]

                # insert_pos: insert block before index
                for insert_pos in range(s-1, 0, -1):

                    checking_node = route[insert_pos]
                    if checking_node <= N:
                        if route_index[checking_node + N] >= s and route_index[checking_node + N] <= e:
                            break
                    if capacity_violated(s, e, insert_pos):
                        continue

                    d_cost = delta_cost(s, e, insert_pos, removing_delta)
                    if best_delta_cost > d_cost:
                        best_delta_cost = d_cost
                        move = (s, e, insert_pos)
                    
                    
                for insert_pos in range(e + 2, 2*N + 2):

                    checking_node = route[insert_pos - 1]
                    if checking_node > N:
                        if route_index[checking_node - N] >= s and route_index[checking_node - N] <= e:
                            break
                    if capacity_violated(s, e, insert_pos):
                        continue
                    
                    d_cost = delta_cost(s, e, insert_pos, removing_delta)
                    if best_delta_cost > d_cost:
                        best_delta_cost = d_cost
                        move = (s, e, insert_pos)
                
                if best_delta_cost < 0:
                    break

            if move:
                route_update(move[0], move[1], move[2])
                # print(route_cost(route[1:-1]))

    print(N)
    print(*route[1:-1])

if __name__ == '__main__':
    main()