import random
# random.seed(42)

def solve(N: int, K: int, c: 'list[list]') -> list:
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


    # random.shuffle(cands)
    # route = [0]
    # for pickup_loc in cands:
    #     route.append(pickup_loc)
    #     route.append(pickup_loc + N)

    route.append(2*N + 1)
    # random.shuffle(cands)

    MAX_ITER = 100
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

    return route[1:-1]