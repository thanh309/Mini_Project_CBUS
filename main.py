from eval import result


def main():
    # Read data
    with open('data/example2.txt', 'r') as f:
        N ,K = tuple(map(int, f.readline().split()))
        cost_matrix = []
        for _ in range(2*N + 1):
            cost_matrix.append(tuple(map(int, f.readline().split())))

    # Test
    route = '6 4 3 9 7 19 2 8 18 1 13 12 5 11 14 15 16 10 17 20'
    print(result(N, K, cost_matrix, route).route_cost())


if __name__ == '__main__':
    main()