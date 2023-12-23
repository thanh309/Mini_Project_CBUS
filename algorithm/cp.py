from ortools.sat.python import cp_model
import numpy as np

def solve(N: int, K: int, c: 'list[list]') -> list:
        
    NUM_NODES = 2*N + 2
    model = cp_model.CpModel()
    c = np.array(c)


    ########## Add the flow variables and their constraints ##########

    x = np.array([[model.NewBoolVar(f'x[{i}, {j}]') for j in range(
        NUM_NODES)] for i in range(NUM_NODES)])

    # 1. Each location (except the origin and destination of the bus) is visited exactly once
    # (has 1 way in and 1 way out)
    for i in range(1, NUM_NODES - 1):
        model.Add(cp_model.LinearExpr.Sum(x[i, 1:NUM_NODES]) == 1)
        model.Add(cp_model.LinearExpr.Sum(x[0:NUM_NODES-1, i]) == 1)

    # 2. The next location from the origin must be one of the passenger pick-up points,
    # and the destination of the bus must be accessed through one of the drop-off points
    model.Add(cp_model.LinearExpr.Sum(x[0, 1:N+1]) == 1)
    model.Add(cp_model.LinearExpr.Sum(x[N+1:NUM_NODES-1, NUM_NODES-1]) == 1)



    ########## Add the time variables and their constraints ##########

    t = [model.NewIntVar(0, 2*N + 1, f't[{i}]') for i in range(NUM_NODES)]

    # The time of arrival of the locations must be different from each others
    # model.AddAllDifferent(t) # not needed, can be remove when doing linearization

    # Time of arrival at the endpoints
    model.Add(t[0] == 0)
    model.Add(t[-1] == 2*N + 1)

    # Make sure that the passenger is picked up before the bus go to their drop-off point
    for i in range(1, N + 1):
        model.Add(t[i] < t[i + N])


    ########## Add 'current load' variables ##########

    # l[i]: load of the bus after leaving i
    l = [model.NewIntVar(0, K, f'l[{i}]') for i in range(NUM_NODES)]

    # Load of the bus at endpoints
    model.Add(l[0] == 0)
    model.Add(l[NUM_NODES - 1] == 0)



    ########## Add relation constraints between x, l, t ##########

    # pax[i]: 'number of passengers' at location i
    # Denote: pax[i] == 0 when i in {0, 2N+1} (endpoints)
    #         pax[i] == 1 when i in [1, N] (the pick-up locations)
    #         pax[i] == -1 when i in [N+1, 2N] (the drop-off locations)
    pax = [1 for _ in range(N + 1)]
    pax.extend([-1 for _ in range(N + 1)])
    pax[0] = pax[-1] = 0

    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            model.Add(t[i] + 1 == t[j]).OnlyEnforceIf(x[i, j])
            model.Add(l[j] == l[i] + pax[j]).OnlyEnforceIf(x[i, j])



    ########## Set the objective function and solving the CP problem ##########
    objective = cp_model.LinearExpr.WeightedSum(x.flatten(), c.flatten())
    model.Minimize(objective)
    solver = cp_model.CpSolver()
    # solver.parameters.max_time_in_seconds = 300
    # solver.parameters.log_search_progress = True
    solver.Solve(model)

    # print(solver.ObjectiveValue())
    # print(solver.Values(t))
    # print(solver.Values(l))



    ########## Print the solution ##########
    route = [None for _ in range(NUM_NODES - 1)]
    for loc in range(1, NUM_NODES - 1):
        route[solver.Value(t[loc])] = loc

    return route[1:]