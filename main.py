from eval import result


def main():
    # Read data
    with open('data/example.txt', 'r') as f:
        N ,K = tuple(map(int, f.readline().split()))
        cost_matrix = []
        for _ in range(2*N + 1):
            cost_matrix.append(tuple(map(int, f.readline().split())))

    # Test
    # route = '1 2 6 7 5 10 3 4 8 9'
    route = [0, 1, 5, 6, 4, 9, 2, 3, 7, 8]
    print(result(N, K, cost_matrix, route).route_cost())


if __name__ == '__main__':
    main()