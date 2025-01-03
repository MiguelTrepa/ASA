from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value, PULP_CBC_CMD
import sys

#__________________________________________Ler input___________________________________________________

factories, countries, children = map(int, sys.stdin.readline().strip().split())

factory_data = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(factories)]
country_data = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(countries)]
child_requests = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(children)]

# Dicionários para facilitar a indexação
factories_by_country = {j: [f[0] for f in factory_data if f[1] == j] for j in range(1, countries + 1)}
children_by_country = {j: [k for k in range(1, children + 1) if child_requests[k - 1][1] == j] for j in range(1, countries + 1)}

#__________________________________________Configurar o Problema_________________________________________

# Definir o problema de otimização
problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

x = {(k, i): LpVariable(f"x_{k}_{i}", cat="Binary")
     for k, child_request in enumerate(child_requests, start=1)
     for i in child_request[2:]}

# Objetivo: Maximizar o número de crianças satisfeitas
problem += lpSum(x[k, i] for (k, i) in x), "Maximize_Satisfied_Children"

# Restrição 1: Cada criança recebe no máximo 1 presente
for k, child_request in enumerate(child_requests, start=1):
    problem += lpSum(x[k, i] for i in child_request[2:]) <= 1, f"Child_{k}_One_Present"

# Restrição 2: Capacidade máxima de cada fábrica
for i, (_, _, max_capacity) in enumerate(factory_data, start=1):
    problem += lpSum(x[k, i] for k in range(1, children + 1) if (k, i) in x) <= max_capacity, f"Factory_{i}_Capacity"

# Restrição 3: Limite de exportação por país
for j, (_, max_export, _) in enumerate(country_data, start=1):
    problem += lpSum(x[k, i] for i in factories_by_country[j] for k in range(1, children + 1)
                     if (k, i) in x and child_requests[k - 1][1] != j) <= max_export, f"Country_{j}_Export_Limit"

# Restrição 4: Mínimo de brinquedos por país
for j, (_, _, min_import) in enumerate(country_data, start=1):
    problem += lpSum(x[k, i] for i in factories_by_country[j] for k in range(1, children + 1)
                     if (k, i) in x and child_requests[k - 1][1] == j) >= min_import, f"Country_{j}_Import_Minimum"

# Resolver o problema
problem.solve(PULP_CBC_CMD(msg=False))

# Imprimir o resultado
if LpStatus[problem.status] == "Optimal":
    print(int(value(problem.objective)))
else:
    print(-1)
