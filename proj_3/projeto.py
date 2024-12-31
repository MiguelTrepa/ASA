# """
# Resolução do projeto três de Análise e Síntese de Algoritmos

# Autores: Miguel Trêpa, nº 109370 & Joana Guia, nº 99147
# """

from pulp import *
import sys

#__________________________________________Ler input___________________________________________________

factories, countries, children = map(int, sys.stdin.readline().strip().split())

# Lê as fábricas
factory_data = []
for _ in range(factories):
    factory_data.append(list(map(int, sys.stdin.readline().strip().split())))

# Lê os países
country_data = []
for _ in range(countries):
    country_data.append(list(map(int, sys.stdin.readline().strip().split())))

# Lê os pedidos das crianças
child_requests = []
for _ in range(children):
    child_requests.append(list(map(int, sys.stdin.readline().strip().split())))

# Debugging: Exibir as informações lidas
# print("Factories:", factory_data)
# print("Countries:", country_data)
# print("Child Requests:", child_requests)

#_______________________________________________________________________________________________________

# Criar o problema de maximização
problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

# Variáveis de decisão: x[k][i] - se a criança k recebe um presente da fábrica i
x = LpVariable.dicts("x", 
                     ((k, i) for k in range(1, children + 1) for i in range(1, factories + 1)), 
                     cat="Binary")

# Função objetivo: Maximizar o número de crianças satisfeitas
problem += lpSum(x[k, i] for k in range(1, children + 1) for i in range(1, factories + 1) 
                 if i in child_requests[k - 1][2:]), "Maximize_Satisfied_Children"

# Restrição 1: Cada criança recebe no máximo 1 presente
for k in range(1, children + 1):
    problem += lpSum(x[k, i] for i in range(1, factories + 1) if i in child_requests[k - 1][2:]) <= 1, f"Child_{k}_One_Present"

# Restrição 2: Capacidade máxima de cada fábrica
for i in range(1, factories + 1):
    max_capacity = factory_data[i - 1][2]
    problem += lpSum(x[k, i] for k in range(1, children + 1) if i in child_requests[k - 1][2:]) <= max_capacity, f"Factory_{i}_Capacity"

# Restrição 3: Limite de exportação por país
for j in range(1, countries + 1):
    max_export = country_data[j - 1][1]
    factories_in_country = [f[0] for f in factory_data if f[1] == j]
    children_in_country = [k for k in range(1, children + 1) if child_requests[k - 1][1] == j]
    problem += lpSum(x[k, i] for i in factories_in_country for k in children_in_country) <= max_export, f"Country_{j}_Export_Limit"

# Restrição 4: Mínimo de brinquedos por país
for j in range(1, countries + 1):
    min_import = country_data[j - 1][2]
    factories_in_country = [f[0] for f in factory_data if f[1] == j]
    children_in_country = [k for k in range(1, children + 1) if child_requests[k - 1][1] == j]
    problem += lpSum(x[k, i] for i in factories_in_country for k in children_in_country) >= min_import, f"Country_{j}_Import_Minimum"

# Resolver o problema
# problem.solve()
problem.solve(PULP_CBC_CMD(msg=False))

# # Exibir os resultados
# if LpStatus[problem.status] == "Optimal":
#     print("Número máximo de crianças satisfeitas:", value(problem.objective))
#     for k in range(1, children + 1):
#         for i in range(1, factories + 1):
#             if x[k, i].varValue == 1:
#                 print(f"Criança {k} recebe um presente da fábrica {i}")
# else:
#     print("Não é possível satisfazer as restrições.")

# Exibir o resultado esperado pelo projeto
if LpStatus[problem.status] == "Optimal":
    # Exibir o número máximo de crianças satisfeitas
    print(int(value(problem.objective)))
else:
    # Se não for possível satisfazer as restrições
    print(-1)