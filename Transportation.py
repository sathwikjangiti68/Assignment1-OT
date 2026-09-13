import numpy as np

# Transportation Problem
m = 4
n = 4
cost = [
    [19, 30, 50, 10],
    [70, 30, 40, 60],
    [40, 8, 70, 20],
    [30, 25, 35, 15]
]

supply = [7, 9, 18, 16]
demand = [5, 8, 20, 17]

allocation = [[0 for j in range(n)] for i in range(m)]

s = supply.copy()
d = demand.copy()

# ---------------- VAM ----------------

while sum(s) > 0 and sum(d) > 0:

    row_penalty = [-1] * m
    col_penalty = [-1] * n

    for i in range(m):

        values = []

        for j in range(n):

            if s[i] > 0 and d[j] > 0:
                values.append(cost[i][j])

        if len(values) >= 2:
            values.sort()
            row_penalty[i] = values[1] - values[0]

        elif len(values) == 1:
            row_penalty[i] = values[0]

    for j in range(n):

        values = []

        for i in range(m):

            if s[i] > 0 and d[j] > 0:
                values.append(cost[i][j])

        if len(values) >= 2:
            values.sort()
            col_penalty[j] = values[1] - values[0]

        elif len(values) == 1:
            col_penalty[j] = values[0]

    max_row = max(row_penalty)
    max_col = max(col_penalty)

    if max_row >= max_col:

        i = row_penalty.index(max_row)

        j = -1
        minimum = float('inf')

        for k in range(n):

            if s[i] > 0 and d[k] > 0:

                if cost[i][k] < minimum:
                    minimum = cost[i][k]
                    j = k

    else:

        j = col_penalty.index(max_col)
        i = -1
        minimum = float('inf')

        for k in range(m):

            if s[k] > 0 and d[j] > 0:

                if cost[k][j] < minimum:
                    minimum = cost[k][j]
                    i = k

    amount = min(s[i], d[j])

    allocation[i][j] = amount

    s[i] -= amount
    d[j] -= amount

print("------------------------------------------")
print("Initial Basic Feasible Solution using VAM:")
print("------------------------------------------")

for i in range(m):

    for j in range(n):
        print(int(allocation[i][j]), end="\t")

    print()

initial_cost = 0

for i in range(m):

    for j in range(n):

        initial_cost += allocation[i][j] * cost[i][j]

print("\nInitial Transportation Cost =", int(initial_cost))

# ---------------- MODI ----------------

while True:
    u = [None] * m
    v = [None] * n

    u[0] = 0

    changed = True

    while changed:

        changed = False

        for i in range(m):

            for j in range(n):

                if allocation[i][j] > 0:

                    if u[i] is not None and v[j] is None:

                        v[j] = cost[i][j] - u[i]
                        changed = True

                    elif u[i] is None and v[j] is not None:

                        u[i] = cost[i][j] - v[j]
                        changed = True


    print("\nU values:")
    print(u)

    print("V values:")
    print(v)

    # Opportunity Cost
    delta = [[0 for j in range(n)] for i in range(m)]

    for i in range(m):

        for j in range(n):

            if allocation[i][j] == 0:
                delta[i][j] = cost[i][j] - u[i] - v[j]

    print("\nOpportunity Cost Table:")

    for i in range(m):

        for j in range(n):
            print(int(delta[i][j]), end="\t")

        print()

    # Find entering cell
    minimum = 0
    enter_i = -1
    enter_j = -1

    for i in range(m):

        for j in range(n):

            if delta[i][j] < minimum:

                minimum = delta[i][j]
                enter_i = i
                enter_j = j

    # Optimal solution

    if enter_i == -1:
        break

    print("\nEntering cell:", enter_i + 1, enter_j + 1)

    # ---------------- Closed Loop ----------------

    start = (enter_i, enter_j)

    def find_loop(path):

        current = path[-1]

        if len(path) >= 4 and current == start:
            return path

        i, j = current

        if len(path) % 2 == 1:

            for col in range(n):

                if col == j:
                    continue

                if allocation[i][col] > 0 or (i, col) == start:

                    next_cell = (i, col)

                    if next_cell == start and len(path) >= 4:
                        return path + [next_cell]

                    if next_cell not in path:

                        result = find_loop(path + [next_cell])

                        if result:
                            return result

        else:

            for row in range(m):

                if row == i:
                    continue

                if allocation[row][j] > 0 or (row, j) == start:

                    next_cell = (row, j)

                    if next_cell == start and len(path) >= 4:
                        return path + [next_cell]

                    if next_cell not in path:

                        result = find_loop(path + [next_cell])

                        if result:
                            return result

        return None


    loop = find_loop([start])

    print("\nClosed Loop:")

    for cell in loop:

        print("(" + str(cell[0] + 1) + "," +
              str(cell[1] + 1) + ")", end=" ")

    print()

    # ---------------- Theta ----------------

    theta = float('inf')

    for k in range(1, len(loop) - 1, 2):

        i, j = loop[k]

        if allocation[i][j] < theta:
            theta = allocation[i][j]

    print("\nTheta =", int(theta))

    # ---------------- Modify Allocation ----------------

    for k in range(len(loop) - 1):

        i, j = loop[k]

        if k % 2 == 0:
            allocation[i][j] += theta

        else:
            allocation[i][j] -= theta

# ---------------- Final Answer ----------------
print("\n--------------------------------")
print("Final Optimal Allocation Table:")
print("--------------------------------")

for i in range(m):

    for j in range(n):
        print(int(allocation[i][j]), end="\t")

    print()

total_cost = 0

for i in range(m):

    for j in range(n):
        total_cost += allocation[i][j] * cost[i][j]

print("\nMinimum Transportation Cost =", int(total_cost))
