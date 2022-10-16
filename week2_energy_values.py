# python3

EPS = 1e-6
PRECISION = 20

class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row

def ReadEquation():
    size = int(input())

    if size == 0:
        return None

    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)

def ReadEquation_mine(path):

    a = []
    b = []

    with open(path) as file:
        lines = file.readlines()
        size = int(lines[0])

        if size == 0:
            return None

        for l in lines[1:]:
            line = list(map(float, l.split()))
            a.append(line[:size])
            b.append(line[size])

    return Equation(a, b)


def solve_equation(equation):
    n_equations = len(equation.a)

    if n_equations == 0:
        return

    n_parameters = len(equation.a[0])

    rows = {j for j in range(n_equations)}
    remaining_columns = {i for i in range(n_parameters)}
    remaining_rows = {j for j in range(n_equations)}

    while len(remaining_columns):
        i = remaining_columns.pop()

        for j in rows:

            if equation.a[j][i] != 0 and j in remaining_rows:
                remaining_rows.remove(j)

                # do the calculations
                pivot = equation.a[j][i]
                equation.a[j] = [item/pivot for item in equation.a[j]]
                equation.b[j] = equation.b[j]/pivot

                for jj in rows:
                    if jj != j:
                        ratio = -1 * equation.a[jj][i]

                        equation.a[jj] = [item_jj + (ratio * item_j) for (item_jj, item_j) in zip(equation.a[jj], equation.a[j])]
                        equation.b[jj] = equation.b[jj] + ratio * equation.b[j]
    return equation


def make_diagonal_matrix(A, b,):
    n = len(A)
    m = len(A[0])

    remaining = [k for k in range(m)]

    solutions = [0 for _ in range(m)]
    for i in range(m):
        has_solution = False
        for j in range(n):

            if A[j][i] != 0 and j in remaining:
                has_solution = True
                remaining.remove(j)

                solution = b[j]/A[j][i]

                solutions[i] = solution

                break

        if has_solution is False:
            return None
    return solutions

def create_final_string(sol):
    if len(sol):

        st = ''
        for item in sol:
            st = st + str(item) + ' '

        return st[:-1]
    return ''

equation = ReadEquation()


if equation is not None:
    gaussian_solved = solve_equation(equation)
    solution = make_diagonal_matrix(gaussian_solved.a, gaussian_solved.b)


    final_string = create_final_string(solution)
    print(final_string)
