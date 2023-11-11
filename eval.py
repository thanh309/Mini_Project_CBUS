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
            from_loc = self.route[i] - 1
            to_loc = self.route[i + 1] - 1
            result += self.cost_matrix[from_loc][to_loc]
        result += self.cost_matrix[self.route[-1] - 1][self.route[0] - 1]
        return result