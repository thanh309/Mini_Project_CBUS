from time import perf_counter as t
from data.data_generator import datagen
from os.path import exists


def cost_matrix_init(example: int, N: int = None, K: int = None) -> 'list[list]':
    c = []
    if example:
        with open(f'data/example{example}.txt', 'r') as f:
            N, K = tuple(map(int, f.readline().split()))
            for i in range(2*N + 1):
                c.append(list(map(int, f.readline().split())))
                c[i].append(c[i][0])
            c.append(c[0])
    else:
        if not exists(f'data/{N}_{K}.txt'):
            datagen(N, K)
        with open(f'data/{N}_{K}.txt', 'r') as f:
            _ = f.readline()
            for i in range(2*N + 1):
                c.append(list(map(int, f.readline().split())))
                c[i].append(c[i][0])
            c.append(c[0])
    return c


class cbus_solution:

    def __init__(self, N: int, K: int, cost_matrix: 'list[list]', route: 'list | None') -> None:
        self.cost_matrix = cost_matrix
        if isinstance(route, str):
            self.route = tuple(map(int, route.strip().split()))
        else:
            self.route = route
        self.N = N
        self.K = K
        self.__time__ = -1
        self.__solved__ = False

    def sol_time(self) -> float:
        return self.__time__

    def route_cost(self) -> int:
        result = 0
        
        for i in range(2*self.N - 1):
            from_loc = self.route[i]
            to_loc = self.route[i + 1]
            result += self.cost_matrix[from_loc][to_loc]

        result += self.cost_matrix[self.route[-1]][0]
        result += self.cost_matrix[0][self.route[0]]
        return result


    def print_sol(self) -> None:
        print(*self.route)
    

    def precedence_test(self) -> bool:
        for loc in self.route:
            if loc <= self.N:
                if self.route.index(loc) > self.route.index(loc + self.N):
                    print(f'precedence_test FAIL: pair ({loc}, {loc + self.N}) violated')
                    self.print_sol()
                    return False
            else:
                if self.route.index(loc) < self.route.index(loc - self.N):
                    print(f'precedence_test FAIL: pair ({loc - self.N}, {loc}) violated')
                    self.print_sol()
                    return False
        print(f'precedence_test PASS')
        return True
    

    def capacity_test(self) -> bool:
        load = 0
        for loc in self.route:
            if loc <= self.N:
                load += 1
                if load > self.K:
                    print(f'capacity_test FAIL: node ({loc}) exceeded max capacity')
                    self.print_sol()
                    return False
            else:
                load -= 1
        print('capacity_test PASS')
        return True


    def solve(self, solve_f: 'function') -> None:
        t0 = t()
        self.route = solve_f(self.N, self.K, self.cost_matrix)
        self.__time__ = t() - t0
        self.__solved__ = True

    def info(self, print_route: bool = True) -> None:
        print('*'*50)
        if not self.__solved__:
            print('Problem has not been solved')
        else:
            if self.capacity_test() and self.precedence_test():
                print()
                print('Route cost:', self.route_cost())
                if print_route:
                    print('Route: ', end='')
                    self.print_sol()
                print('Time taken:', self.sol_time(), 'seconds')
        print('*'*50)