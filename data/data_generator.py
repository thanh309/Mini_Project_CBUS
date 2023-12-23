import random
from os.path import exists
random.seed(20220066)  # for consistency

# ------------------------------- #
# Number of passengers
N = 750
# Capacity of the bus
K = 40
# The range of the cost between two locations
COST_RANGE = range(1, 3*N + 1)
# ------------------------------- #


def datagen(N: int, K: int, COST_RANGE: range = None) -> None:
    if COST_RANGE == None:
        COST_RANGE = range(1, 3*N + 1)

    cost_matrix = [['0' for _ in range(2*N + 1)] for _ in range(2*N + 1)]

    for i in range(2*N):
        for j in range(i + 1, 2*N + 1):
            cost_matrix[i][j] = cost_matrix[j][i] = str(
                random.choice(COST_RANGE))

    with open(f'data/{N}_{K}.txt', 'w') as f:
        f.write(f'{N} {K}\n')
        f.write('\n'.join(tuple(map(' '.join, cost_matrix))))


if __name__ == '__main__':
    datagen(N, K, COST_RANGE)