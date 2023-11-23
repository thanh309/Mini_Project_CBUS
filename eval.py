class result():

    def __init__(self, N, K, cost_matrix, route) -> None:
        self.cost_matrix = cost_matrix
        if isinstance(route, str):
            self.route = tuple(map(int, route.strip().split()))
        else:
            self.route = route
        self.N = N
        self.K = K


    def route_cost(self) -> int:
        result = 0
        
        for i in range(2*self.N - 1):
            from_loc = self.route[i]
            to_loc = self.route[i + 1]
            result += self.cost_matrix[from_loc][to_loc]

        result += self.cost_matrix[self.route[-1]][0]
        result += self.cost_matrix[0][self.route[0]]
        return result
    

    def precedence_test(self) -> str:
        for loc in self.route:
            if loc <= self.N:
                if self.route.index(loc) > self.route.index(loc + self.N):
                    return 'FAIL'
            else:
                if self.route.index(loc) < self.route.index(loc - self.N):
                    return 'FAIL'
        return 'PASS'
    

    def capacity_test(self) -> str:
        load = 0
        for loc in self.route:
            if loc <= self.N:
                load += 1
                if load > self.K:
                    return 'FAIL'
            else:
                load -= 1
        return 'PASS'