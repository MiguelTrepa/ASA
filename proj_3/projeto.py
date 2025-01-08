# """
# Resolução do projeto três de Análise e Síntese de Algoritmos

# Autores: Miguel Trêpa, nº 109370 & Joana Guia, nº 99147
# """

from pulp import *
import sys

#__________________________________________Ler input___________________________________________________

# Reading input
factories, countries, children = map(int, sys.stdin.readline().strip().split())

# Reading factory data
factory_data = []
for _ in range(factories):
    factory_data.append(list(map(int, sys.stdin.readline().strip().split())))

# Reading country data
country_data = []
for _ in range(countries):
    country_data.append(list(map(int, sys.stdin.readline().strip().split())))

# Reading child requests
child_requests = []
for _ in range(children):
    child_requests.append(list(map(int, sys.stdin.readline().strip().split())))

# Filter out factories with fmax = 0
filtered_factory_data = [factory for factory in factory_data if factory[2] > 0]

# Update the references of valid factories (IDs of factories that are relevant)
valid_factory_ids = {factory[0] for factory in filtered_factory_data}

# Filter children who do not have associated factories
filtered_child_requests = [
    child for child in child_requests if any(f in valid_factory_ids for f in child[2:])
]

#_______________________________________________________________________________________________________

# Iniciar o problema
problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

# Create binary variables for child-factory pairs
x = LpVariable.dicts("x", [(k, i) for k in range(1, children + 1) for i in range(1, factories + 1) 
                 if i in filtered_child_requests[k - 1][2:]], 0, None, LpBinary)

# Objective function: Maximize the number of satisfied children
problem += lpSum(x[k, i] for (k, i) in x), "Maximize_Satisfied_Children"

# Restriction 1: Each child receives at most one present
for k in range(1, children + 1):
    problem += lpSum(x[k, i] for i in range(1, factories + 1) if i in filtered_child_requests[k - 1][2:]) <= 1, f"Child_{k}_One_Present"

# Restriction 2: Maximum capacity for each factory
for i in range(1, factories + 1):
    max_capacity = filtered_factory_data[i - 1][2]
    problem += lpSum(x[k, i] for k in range(1, children + 1) if i in filtered_child_requests[k - 1][2:]) <= max_capacity, f"Factory_{i}_Capacity"

# Restrictions 3 and 4: Export and import limits per country
for j in range(1, countries + 1):
    max_export = country_data[j - 1][1]
    min_import = country_data[j - 1][2]

    factories_in_country = [f[0] for f in filtered_factory_data if f[1] == j]

    children_in_country = [k for k in range(1, children + 1) if filtered_child_requests[k - 1][1] == j]
    children_out_country = [k for k in range(1, children + 1) if filtered_child_requests[k - 1][1] != j]

    problem += lpSum(x[k, i] for i in factories_in_country for k in children_out_country 
                if (k, i) in x) <= max_export, f"Country_{j}_Export_Limit"

    problem += lpSum(x[k, i] for i in valid_factory_ids for k in children_in_country
                if (k, i) in x) >= min_import, f"Country_{j}_Import_Minimum"

# Solve the problem
problem.solve(PULP_CBC_CMD(msg=False))

# Print the result
status = problem.solve(PULP_CBC_CMD(msg=False))
if LpStatus[problem.status] == "Optimal":
    print(int(value(problem.objective)))
else:
    print(-1)
