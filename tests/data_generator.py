import random
random.seed(420)  # for consistency

# ------------------------------- #
# Number of passengers; should be in (5, 10, 20, 50, 100, 200, 500, 1000)
N = 5
# Capacity of the bus
K = 3
# To indicate if the cost matrix is balanced or not (c[i, j] == c[j, i])
# Should be in (B, I)
IS_BALANCED = 'B'
# The range of the cost between two locations
COST_RANGE = range(1, 3*N)
# ------------------------------- #


def main():

    cost_matrix = [['0' for _ in range(2*N + 1)] for _ in range(2*N + 1)]

    if IS_BALANCED == 'B':
        for i in range(2*N):
            for j in range(i + 1, 2*N + 1):
                cost_matrix[i][j] = cost_matrix[j][i] = str(
                    random.choice(COST_RANGE))

    else:
        for i in range(2*N + 1):
            for j in range(2*N + 1):
                if i != j:
                    cost_matrix[i][j] = str(random.choice(COST_RANGE))

    with open(f'tests/CBUS_{N}_{K}_{IS_BALANCED}.txt', 'w') as f:
        f.write(f'{N} {K}\n')
        f.write('\n'.join(tuple(map(' '.join, cost_matrix))))


if __name__ == '__main__':
    main()