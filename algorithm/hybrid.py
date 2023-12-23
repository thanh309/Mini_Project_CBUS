import random
# random.seed(42)
MAX_BLOCK_LENGTH = 5
MAX_ITER = 5
TIME_LIMIT = 300

def solve(N: int, K: int, c: 'list[list]') -> list:


    route = [0]
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
            else:
                load -= 1
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
            continue



    # cands = list(range(1, N + 1))
    # random.shuffle(cands)
    # for pickup_loc in cands:
    #     route.append(pickup_loc)
    #     route.append(pickup_loc + N)
    #     load_list.extend([1, 0])



    route.append(0)

    def delta_cost(s: int, e: int, insert_pos: int, removing_delta: int) -> int:
        return removing_delta - c[route[insert_pos-1]][route[insert_pos]]\
            + c[route[insert_pos-1]][route[s]] + c[route[e]][route[insert_pos]]


    def capacity_violated(s: int, e: int, insert_pos: int) -> bool:
        if insert_pos > e:
            return capacity_violated(e + 1, insert_pos - 1, s)
        delta_load_inside = load_list[insert_pos - 1] - load_list[s - 1]
        delta_load_outside = 0
        for pos_inside in range(s, e + 1):
            if load_list[pos_inside] + delta_load_inside > K:
                return True
            if route[pos_inside] > N:
                delta_load_outside -= 1
            else:
                delta_load_outside += 1
        if max(load_list[insert_pos:s]) + delta_load_outside > K:
            return True
        return False
        # for pos_outside in range(insert_pos, s):
        #     if not check_cap(load_list[pos_outside] + delta_load_outside):
        #         return True
        # return False


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
    
    def max_capacity() -> tuple:
        '''Calculate the maximum capacity of the route.

        Returns:
            tuple[max_cap, ids]: max capacity of the route, at one of the indices in `ids`.
        '''
        cur_cap = 0
        max_cap = 0
        for i in range(1, len(route)):
            if route[i] <= N:
                cur_cap += 1
                if cur_cap > max_cap:
                    ids = [i]
                    max_cap = cur_cap
                elif cur_cap == max_cap:
                    ids.append(i)
            else:
                cur_cap -= 1
        ids.append(999999)
        return (max_cap, ids)

    cands = list(range(1, N + 1))
    for iter in range(MAX_ITER):
        random.shuffle(cands)
        for cand in cands:
            # i, i': the old and new index of the pick-up point (cand)
            # j, j': the old and new index of the drop-off point (cand + N)
            # d: delta
            i, j = route.index(cand), route.index(cand + N)
            if j - i == 1:
                d_removal = c[route[i-1]][route[j+1]] - c[route[i-1]][cand] - c[cand][cand+N]- c[cand+N][route[j+1]]
            else:
                d_removal = c[route[i-1]][route[i+1]] - c[route[i-1]][cand] - c[cand][route[i+1]] + c[route[j-1]][route[j+1]] - c[route[j-1]][cand+N] - c[cand+N][route[j+1]]
            route.pop(j)
            route.pop(i)

            route_max_cap, max_cap_ids = max_capacity()
            min_d_insertion = - d_removal
            action = (i - 1, j - 2)
            changed = False

            # Consecutive insertion
            # Try to insert the pair after index i_prime of the new route
            # i_prime in [0, 2N - 2]
            p = 0
            for i_prime in range(2*N - 1):
                if (i_prime == max_cap_ids[p]) and (route_max_cap + 1 > K):
                    p += 1
                    continue
                d_insertion = c[route[i_prime]][cand] + c[cand][cand+N] + c[cand+N][route[i_prime+1]] - c[route[i_prime]][route[i_prime+1]]
                if d_insertion < min_d_insertion:
                    min_d_insertion = d_insertion
                    action = (i_prime, i_prime)
                    changed = True


            # Non-consecutive insertion
            p = 0
            for i_prime in range(2*N - 2):
                if route_max_cap < K:
                    for j_prime in range(i_prime + 1, 2*N - 1):
                        d_insertion = c[route[i_prime]][cand] + c[cand][route[i_prime+1]] - c[route[i_prime]][route[i_prime+1]]\
                            + c[route[j_prime]][cand+N] + c[cand+N][route[j_prime+1]] - c[route[j_prime]][route[j_prime+1]]
                        if d_insertion < min_d_insertion:
                            min_d_insertion = d_insertion
                            action = (i_prime, j_prime)
                            changed = True

                else:
                    if i_prime == max_cap_ids[p]:
                        p += 1
                        continue
                    for j_prime in range(i_prime + 1, min(2*N - 1, max_cap_ids[p])):
                        d_insertion = c[route[i_prime]][cand] + c[cand][route[i_prime+1]] - c[route[i_prime]][route[i_prime+1]]\
                            + c[route[j_prime]][cand+N] + c[cand+N][route[j_prime+1]] - c[route[j_prime]][route[j_prime+1]]
                        if d_insertion < min_d_insertion:
                            min_d_insertion = d_insertion
                            action = (i_prime, j_prime)
                            changed = True


            route.insert(action[1] + 1, cand + N)
            route.insert(action[0] + 1, cand)
        if not changed:
            break

    load_list = []
    for node in route:
        if node == 0:
            load_list.append(0)
        else:
            if node > N:
                load_list.append(load_list[-1] - 1)
            else:
                load_list.append(load_list[-1] + 1)
    route[-1] = 2*N + 1
    route_index = dict()
    for i, v in enumerate(route):
        route_index[v] = i


    cands = list(range(1, 2*N + 1))
    for i in range(MAX_ITER):
        random.shuffle(cands)
        for cand in cands:

            # s, e: start and end of a block (index)
            s = route_index[cand]
            e_range = range(s, min(2*N + 1, s + MAX_BLOCK_LENGTH))
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

    

    return route[1:-1]
