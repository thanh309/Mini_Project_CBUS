from solution import *
from algorithm import cp, greedy, node_swap, or_opt, pair_relocation, hybrid
# from cProfile import run

MAGIC_COLOR = ["\033[107m\033[30m", "\033[47m\033[97m", "\033[0m", "\033[47m\033[30m\033[1m"]

solver = {
    1: cp.solve,
    2: greedy.solve,
    3: node_swap.solve,
    4: or_opt.solve,
    5: pair_relocation.solve,
    6: hybrid.solve
}

example_size = [(), (5, 3), (10, 6), (100, 40), (500, 40), (1000, 40)]

def main(N: int, K: int, example: int, solver_id: int, data: dict) -> None:
    if example:
        N, K = example_size[example]
        key = f'e{example}'
    else:
        key = f'{N}_{K}'
    c = cost_matrix_init(example, N, K)
    route = []
    sol = cbus_solution(N, K, c, route)
    sol.solve(solver[solver_id])

    # Use the following line of code to show the info after each solve
    # sol.info(print_route=False)

    if key not in data:
        data[key] = [[0, [], []] for _ in range(6)]
    data[key][solver_id - 1][0] += 1
    data[key][solver_id - 1][1].append(sol.route_cost())
    data[key][solver_id - 1][2].append(sol.__time__)


if __name__ == '__main__':
    print("Input N, K, example number (0 to use randomized input), solver's id, number of iterations; separated by space")
    print("solver's id: 1: cp; 2: greedy; 3: node swapping; 4: or-opt; 5: pair relocation; 6: hybrid")
    print("'stat' to show statistics")
    print("'clear' to reset data")
    print("'exit' to exit")
    data = {}
    while True:
        inp = input('>>> ').strip()
        if inp == 'exit':
            exit()
        elif inp == 'clear':
            data = {}
            continue
        elif inp == 'stat':
            for k, v in data.items():
                print('-' * 90)
                print(k, end=':\n')
                print(MAGIC_COLOR[3] + 'id'.ljust(15), 'min_c'.ljust(15), 'max_c'.ljust(15), 'avg_c'.ljust(15), 'avg_t'.ljust(25) + MAGIC_COLOR[2])
                for i in range(6):
                    try:
                        print(MAGIC_COLOR[i%2] + f'{i + 1}'.ljust(15), f'{min(v[i][1])}'.ljust(15), f'{max(v[i][1])}'.ljust(15), f'{sum(v[i][1])/v[i][0]}'.ljust(15), f'{sum(v[i][2])/v[i][0]}'.ljust(25) + MAGIC_COLOR[2])
                    except ValueError:
                        print(MAGIC_COLOR[i%2] + f'{i + 1}'.ljust(15), 'N/A'.ljust(15), 'N/A'.ljust(15), 'N/A'.ljust(15), 'N/A'.ljust(25) + MAGIC_COLOR[2])
                print('-' * 90)
                print()
        else:   
            N, K, example, solver_id, iters = tuple(map(int, inp.split()))
            for _ in range(iters):
                main(N, K, example, solver_id, data)
                # run('main(N, K, example, solver_id)')