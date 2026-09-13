import numpy as np

# Big M value
M = 1000000

variables = ['x1', 'x2', 's1', 's2', 'A1']

C = np.array([3, 2, 0, 0, -M], dtype=float)

A = np.array([
    [1, 1, -1, 0, 1],
    [1, 2, 0, 1, 0]
], dtype=float)

b = np.array([4, 6], dtype=float)

basis = [4, 3]


def calculate_z(A, b, basis):

    cb = C[basis]

    Zj = np.zeros(len(variables))

    for j in range(len(variables)):

        value = 0

        for i in range(len(basis)):
            value += cb[i] * A[i, j]

        Zj[j] = value

    Cj_Zj = C - Zj

    Z = 0

    for i in range(len(basis)):
        Z += cb[i] * b[i]

    return Zj, Cj_Zj, Z


def is_positive(value):

    return value > 0


def pivot(A, b, basis, pivot_row, pivot_col):

    A = A.copy()
    b = b.copy()
    basis = basis.copy()

    pivot_value = A[pivot_row, pivot_col]

    A[pivot_row, :] = A[pivot_row, :] / pivot_value

    b[pivot_row] = b[pivot_row] / pivot_value

    for i in range(A.shape[0]):

        if i != pivot_row:

            factor = A[i, pivot_col]

            A[i, :] = A[i, :] - factor * A[pivot_row, :]

            b[i] = b[i] - factor * b[pivot_row]

    basis[pivot_row] = pivot_col

    return A, b, basis


iteration = 0


while True:

    Zj, Cj_Zj, Z = calculate_z(A, b, basis)

    print("\nIteration:", iteration)

    print("Basic Variables:",
          [variables[i] for i in basis])

    print("\nTableau:")

    print("Basis\t", end="")

    for var in variables:
        print(var, "\t", end="")

    print("RHS")

    for i in range(A.shape[0]):

        print(variables[basis[i]], "\t", end="")

        for j in range(A.shape[1]):
            print(round(A[i, j], 2), "\t", end="")

        print(round(b[i], 2))

    print("Cj-Zj\t", end="")

    for value in Cj_Zj:
        print(round(value, 2), "\t", end="")

    print("\nZ =", round(Z, 2))


    # Find entering variable

    positive_columns = []

    for j in range(len(variables)):

        if is_positive(Cj_Zj[j]):
            positive_columns.append(j)


    if not positive_columns:
        break


    pivot_col = positive_columns[0]

    for j in positive_columns:

        if Cj_Zj[j] > Cj_Zj[pivot_col]:

            pivot_col = j


    # Ratio test

    ratios = []

    for i in range(A.shape[0]):

        if A[i, pivot_col] > 0:

            ratio = b[i] / A[i, pivot_col]

            if ratio >= 0:
                ratios.append((ratio, i))


    if not ratios:

        print("The solution is unbounded.")
        break


    ratio, pivot_row = min(ratios)


    print("\nEntering Variable:",
          variables[pivot_col])

    print("Leaving Variable:",
          variables[basis[pivot_row]])

    print("Pivot Element:",
          A[pivot_row, pivot_col])


    A, b, basis = pivot(
        A,
        b,
        basis,
        pivot_row,
        pivot_col
    )


    iteration += 1


print("\n========== OPTIMAL SOLUTION ==========")

solution = {}

for i in range(len(variables)):
    solution[variables[i]] = 0


for i in range(A.shape[0]):
    solution[variables[basis[i]]] = b[i]


for var in variables:

    print(var, "=", round(solution[var], 2))


print("Maximum Profit Z =", round(Z, 2))