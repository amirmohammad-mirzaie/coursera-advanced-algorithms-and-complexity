
from sys import stdin
from sys import maxsize
import itertools



class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b




def read_data():
    n, m = list(map(int, stdin.readline().split()))
    A = []
    for i in range(n):
        A += [list(map(int, stdin.readline().split()))]
    b = list(map(int, stdin.readline().split()))
    c = list(map(int, stdin.readline().split()))

    return n, m, A, b, c

def read_data_from_path(path):

    with open(path) as file:
        lines = file.readlines()
        n, m = list(map(int, lines[0].split()))

        A = []

        for i in range(n):
            A += [list(map(int, lines[i+1].split()))]

        b = list(map(int, lines[n + 1].split()))
        c = list(map(int, lines[n + 2].split()))

        return n, m, A, b, c

def construct_simplex_matrix(A, b):

    m = len(A[0])
    empty_list = [0 for _ in range(m)]

    for i in range(m):
        empty_list_copy = empty_list.copy()
        empty_list_copy[i] = -1
        A.append(empty_list_copy)
        b.append(0)

    return A, b


def solve_equation_gaussian_elimination(data):
    equation = Equation(data.a, data.b)
    n_equations = len(equation.a)

    if n_equations == 0:
        return equation

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
    # print('equation.a', equation.a, '  ', equation.b)
    return equation


def make_diagonal_matrix(A, b, c):
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


def calculate_profit(solution, c):
    return sum([s*item for (s, item) in zip(solution, c)])


def check_inequality(solution, remaining_A, remaining_b):



    for i, a in enumerate(remaining_A):

        sum_ = sum(item1*item2 for (item1, item2) in zip(a, solution))


        if sum_ > remaining_b[i]:

            return False
    return True


def calculate_profits(A, b, c):

    m = len(A[0])

    A, b = construct_simplex_matrix(A, b)

    A.append([1 for _ in range(m)])
    b.append(10**9)


    n = len(A)

    template_profit = {'profit': 0, 'solution': [], 'equations': []}
    profits = []

    subsets = create_subsets(n, m)

    for ss in subsets:

        sub_A = [A[ss[i]][:] for i in range(len(ss))]
        sub_b = [b[ss[i]] for i in range(len(ss))]

        equation = Equation(sub_A, sub_b)

        result = solve_equation_gaussian_elimination(equation)

        solution = make_diagonal_matrix(result.a, result.b, c)


        if solution is not None:

            all_ = [i for i in range(n)]

            rem = [item for item in all_ if item not in ss]

            rem_A = [A[rem[i]][:] for i in range(len(rem))]
            rem_b = [b[rem[i]] for i in range(len(rem))]

            if check_inequality(solution, rem_A, rem_b):

                profit = calculate_profit(solution, c)

                template_profit_copy = template_profit.copy()
                template_profit_copy['profit'] = profit
                template_profit_copy['solution'] = solution
                template_profit_copy['equations'] = ss



                profits.append(template_profit_copy)


    if len(profits):
        selected_profit_details = None
        selected_prof = -maxsize
        selected_solution = 0

        for pro in profits:
            calculated_prof = calculate_profit(pro['solution'], c)

            if calculated_prof > selected_prof:
                selected_solution = pro['solution']
                selected_prof = calculated_prof
                selected_profit_details = pro

        if (n-1) in selected_profit_details['equations']:
            print('Infinity')
            return

        print('Bounded solution')
        string = ''.join(str(item) + ' ' for item in selected_solution)
        print(string[:-1])
        return

    else:
        print('No solution')
        return



def create_subsets(n, m):
    n_indices = [i for i in range(n)]
    subsets = []

    for subset in itertools.combinations(n_indices, m):
        subsets.append(subset)

    return subsets






n, m, A, b, c = read_data()
profits = calculate_profits(A, b, c)
