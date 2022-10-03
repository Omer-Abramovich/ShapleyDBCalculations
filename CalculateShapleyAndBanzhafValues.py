import math
import numpy

# Checks satisfiability of boolean formula.
# Here you define the provenance
# The facts here aren't devided into different sections/relations (as it doesn't matter in provenance form)
# For example - the definition below can represent (a1 and b1 and c1) or (a1 and b2 anc c2) or (a2 and b3 and c3)
# or it can represent (a0 and a2 and a5) or (a0 and a3 and a6) or (a1 and a4 and a7)
# You need to make sure that the numebr of variables here suits the number N below.
def calc_sat():
    return (variables[0] and variables[2] and variables[5]) or\
           (variables[0] and variables[3] and variables[6]) or \
           (variables[1] and variables[4] and variables[7])

# Counts the number of variables in the current subset
def count_trues():
    global variables

    res = 0
    for i in variables:
        if i:
            res +=1
    return res

# Updates the current subset based on a boolean representation of the number num
def update_vars(num):
    global variables
    binary = bin(num)[2:]
    prefix = "0" * (N - len(binary))
    binary_formated = prefix + binary
    variables = [bool(int(x)) for x in binary_formated]

# Adds to the shapley value of all critical variables (S! * ((n -1)-S)!)
# where n is the number of variables and S is the size of subset without the critical variable
def update_shapley_vals():
    global variables, shapley_vals

    size = count_trues() - 1

    for idx, i in enumerate(variables):
        if i:
            variables[idx] = False
            if not calc_sat():
                shapley_vals[idx] = shapley_vals[idx] + (math.factorial(size) * math.factorial(N - size - 1))

            variables[idx] = True

# Adds 1 to the Banzhaf values of all critical variables in the subset
def update_banzhaf_vals():
    global variables, banzhaf_vals, total_banzhaf_criticals

    for idx, i in enumerate(variables):
        if i:
            variables[idx] = False
            if not calc_sat():
                banzhaf_vals[idx] = banzhaf_vals[idx] + 1
                total_banzhaf_criticals += 1

            variables[idx] = True

if __name__ == '__main__':
    global N
    # Here you define the number of variables, please make sure it fits the boolean formula above
    N = 8
    global variables
    variables = [False] * N
    global shapley_vals
    shapley_vals = [0] * N
    global banzhaf_vals
    global total_banzhaf_criticals
    banzhaf_vals = [0] * N
    total_banzhaf_criticals = 0

    # goes over all subsets of the variables (boolean representation)
    for i in range(pow(2, N)):
        update_vars(i)

        # If the assignment is satisfiable
        if calc_sat():
            update_shapley_vals() # Adds to the Shapley values of all critical variables a number based on the size of the subset
            update_banzhaf_vals() # Adds 1 to the Banzhaf values of all critical variables

    shapley_vals = [val / math.factorial(N) for val in shapley_vals] # Normalization Shapley
    banzhaf_vals = [val / total_banzhaf_criticals for val in banzhaf_vals] # Normalization Banzhaf

    print("Shapley values - " + str(shapley_vals))
    print("Banzhaf values - " + str(banzhaf_vals))
    print("\n")
    print("Shapley power index " + str(numpy.argsort(shapley_vals)[::-1]))
    print("Banzhaf power index " + str(numpy.argsort(banzhaf_vals)[::-1]))
    print("\n")
    print("Shapley sanity check (needs to be equal to 1) " + str(sum(shapley_vals)))
    print("Banzhaf sanity check (needs to be equal to 1) " + str(sum(banzhaf_vals)))