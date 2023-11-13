import random
random.seed(42)  # for consistency

# ------------------------------- #
# Number of passengers; should be in (5, 10, 20, 50, 100, 200, 500, 1000)
N = 100
# Capacity of the bus
K = 20
# The range of the cost between two locations
COST_RANGE = range(1, 3*N)
# ------------------------------- #


def main():

    cost_matrix = [['0' for _ in range(2*N + 1)] for _ in range(2*N + 1)]


    for i in range(2*N):
        for j in range(i + 1, 2*N + 1):
            cost_matrix[i][j] = cost_matrix[j][i] = str(
                random.choice(COST_RANGE))

    

    with open(f'data/CBUS_{N}_{K}.txt', 'w') as f:
        f.write(f'{N} {K}\n')
        f.write('\n'.join(tuple(map(' '.join, cost_matrix))))


if __name__ == '__main__':
    main()