from ortools.linear_solver import pywraplp
import numpy as np


def main():


    ########## Read the input ##########
    
    N, K = tuple(map(int, input().split()))
    c = []

    for i in range(2*N + 1):
        c.append(list(map(int, input().split())))
        # Modify the cost matrix: add the auxiliary point 2N + 1,
        # which has the same geographical location as point 0
        c[i].append(c[i][0])

    c.append(c[0])
    c = np.array(c)

    NUM_NODES = 2*N + 2
    solver = pywraplp.Solver.CreateSolver('SCIP')
    # solver = pywraplp.Solver('', pywraplp.Solver.GLPK_MIXED_INTEGER_PROGRAMMING)



    ########## Add the flow variables and their constraints ##########

    x = np.array([[solver.BoolVar(f'x[{i}, {j}]') for j in range(
        NUM_NODES)] for i in range(NUM_NODES)])
    

    # 1. Each location (except the origin and destination of the bus) is visited exactly once
    # (has 1 way in and 1 way out)
    for i in range(1, NUM_NODES - 1):
        solver.Add(solver.Sum(x[i, 1:NUM_NODES]) == 1)
        solver.Add(solver.Sum(x[0:NUM_NODES-1, i]) == 1)

    # 2. The next location from the origin must be one of the passenger pick-up points,
    # and the destination of the bus must be accessed through one of the drop-off points
    solver.Add(solver.Sum(x[0, 1:N+1]) == 1)
    solver.Add(solver.Sum(x[N+1:NUM_NODES-1, NUM_NODES-1]) == 1)



    ########## Add the time variables and their constraints ##########

    t = [solver.IntVar(0, 2*N + 1, f't[{i}]') for i in range(NUM_NODES)]


    # Time of arrival at the endpoints
    solver.Add(t[0] == 0)
    solver.Add(t[-1] == 2*N + 1)

    # Make sure that the passenger is picked up before the bus go to their drop-off point
    for i in range(1, N + 1):
        solver.Add(t[i] <= t[i + N] - 1)



    ########## Add 'current load' variables ##########

    # y[i]: load of the bus after leaving i
    y = [solver.IntVar(0, K, f'y[{i}]') for i in range(NUM_NODES)]

    # Load of the bus at endpoints
    solver.Add(y[0] == 0)
    solver.Add(y[NUM_NODES - 1] == 0)



    ########## Add relation constraints between x, y, t ##########

    # pax[i]: 'number of passengers' at location i
    # Denote: pax[i] == 0 when i in {0, 2N+1} (endpoints)
    #         pax[i] == 1 when i in [1, N] (the pick-up locations)
    #         pax[i] == -1 when i in [N+1, 2N] (the drop-off locations)
    pax = [1 for _ in range(N + 1)]
    pax.extend([-1 for _ in range(N + 1)])
    pax[0] = pax[-1] = 0

    # Constraint linearization
    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            solver.Add(3*N*(1-x[i, j]) + t[i] + 1 >= t[j])
            solver.Add(-3*N*(1-x[i, j]) + t[i] + 1 <= t[j])
            solver.Add(3*K*(1-x[i, j]) + y[j] >= y[i] + pax[j])
            solver.Add(-3*K*(1-x[i, j]) + y[j] <= y[i] + pax[j])



    ########## Set the objective function and solving the CP problem ##########
    objective = []
    x_flat, c_flat = x.flatten(), c.flatten()
    for i in range(len(x_flat)):
        objective.append(x_flat[i] * c_flat[i])

    solver.Minimize(solver.Sum(objective))
    # solver.EnableOutput()
    solver.Solve()

    

    ########## Print the solution ##########
    route = [None for _ in range(NUM_NODES - 1)]
    for loc in range(1, NUM_NODES - 1):
        route[int(t[loc].solution_value())] = loc

    # print(solver.Objective().Value())
    print(N)
    print(*route[1:])


if __name__ == '__main__':
    main()