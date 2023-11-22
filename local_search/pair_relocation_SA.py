import random
import math
from time import time
# random.seed(42)


with open('data/example3.txt', 'r') as f:
    N, K = tuple(map(int, f.readline().split()))
    c = []

    for i in range(2*N + 1):
        c.append(list(map(int, f.readline().split())))
        c[i].append(c[i][0])
    c.append(c[0])

a = time()
def binary_search(arr: list, key: int) -> int:
    low = 0
    high = len(arr) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2

        if arr[mid] > key:
            result = mid
            high = mid - 1
        else:
            low = mid + 1

    return result


def P(s:int, s_prime: int, T: float) -> float:
    if s > s_prime:
        return 1
    return math.exp((s - s_prime)/T)

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
    return (max_cap, ids)


def route_cost() -> int:
    result = 0
    for i in range(2*N + 1):
        from_loc = route[i]
        to_loc = route[i + 1]
        result += c[from_loc][to_loc]
    return result


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

greedy_res = route_cost()

# random.shuffle(cands)

MAX_ITER = round(10 + 10000/(N - 4))
# MAX_ITER = 10000
T0 = 0.25
for iter in range(MAX_ITER):
    T = T0 * (1 - (iter + 0.999)/MAX_ITER)
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

        # Consecutive insertion
        # Try to insert the pair after index i_prime of the new route
        # i_prime in [0, 2N - 2]
        for i_prime in range(2*N - 1):
            if (i_prime <= max_cap_ids[-1]) and (route_max_cap + 1 > K):
                continue
            d_insertion = c[route[i_prime]][cand] + c[cand][cand+N] + c[cand+N][route[i_prime+1]] - c[route[i_prime]][route[i_prime+1]]
            if P(min_d_insertion, d_insertion, T) > random.random():
                min_d_insertion = d_insertion
                action = (i_prime, i_prime)


        # Non-consecutive insertion
        # min_d_jp: dict, min_d_jp[i'] = the minimum change of the drop-off point insertion
        # when j' goes from i' + 1 to 2N - 2; along with index of j'

        min_d_jp = dict()
        # When pickup point is inserted after index 2N - 3 in the new route, only 1 possible
        # place exists to insert drop-off point
        min_d_jp[2*N - 3] = (c[route[2*N - 2]][cand+N] + c[cand+N][0] - c[route[2*N - 2]][0], 2*N - 2)
        for i_prime in range(2*N - 4, -1, -1):
            d = c[route[i_prime+1]][cand+N] + c[cand+N][route[i_prime+2]] - c[route[i_prime+1]][route[i_prime+2]]
            if d < min_d_jp[i_prime + 1][0]:
                min_d_jp[i_prime] = (d, i_prime + 1)
            else:
                min_d_jp[i_prime] = min_d_jp[i_prime + 1]


        for i_prime in range(2*N - 2):
            if (i_prime <= max_cap_ids[-1]) and (route_max_cap + 1 > K):
                continue
            j_prime = min_d_jp[i_prime][1]

            feasible = None
            result = binary_search(max_cap_ids, i_prime)
            if (result != -1 and j_prime < max_cap_ids[result]) or route_max_cap + 1 <= K:
                    d_insertion = c[route[i_prime]][cand] + c[cand][route[i_prime+1]] - c[route[i_prime]][route[i_prime+1]] + min_d_jp[i_prime][0]
                    if P(min_d_insertion, d_insertion, T) > random.random():
                        min_d_insertion = d_insertion
                        action = (i_prime, j_prime)






        route.insert(action[1] + 1, cand + N)
        route.insert(action[0] + 1, cand)
        # print(route_cost())

res2 = route_cost()
# print(route)
# print(max_capacity()[0])
print('time:', time()-a)
print(res2/greedy_res)