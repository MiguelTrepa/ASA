# """
# Resolução do projeto três de Análise e Síntese de Algoritmos

# Autores: Miguel Trêpa, nº 109370 & Joana Guia, nº 99147
# """

# from pulp import *
# import sys

# # Lê a primeira linha contendo o número de fábricas, países e crianças
# factories, countries, children = map(int, sys.stdin.readline().strip().split())

# # Lê as fábricas
# factory_data = []
# for _ in range(factories):
#     factory_data.append(list(map(int, sys.stdin.readline().strip().split())))

# # Lê os países
# country_data = []
# for _ in range(countries):
#     country_data.append(list(map(int, sys.stdin.readline().strip().split())))

# # Lê os pedidos das crianças
# child_requests = []
# for _ in range(children):
#     child_requests.append(list(map(int, sys.stdin.readline().strip().split())))

# # Debugging: Exibir as informações lidas
# print("Factories:", factory_data)
# print("Countries:", country_data)
# print("Child Requests:", child_requests)






# # Dados de entrada
# factories = [
#     {"id": 1, "country": 1, "capacity": 1},  # Fábrica 1 no país 1 com capacidade 1
#     {"id": 2, "country": 1, "capacity": 1},  # Fábrica 2 no país 1 com capacidade 1
#     {"id": 3, "country": 2, "capacity": 1},  # Fábrica 3 no país 2 com capacidade 1
# ]

# countries = [
#     {"id": 1, "export_limit": 2, "min_import": 1},  # País 1
#     {"id": 2, "export_limit": 1, "min_import": 1},  # País 2
# ]

# children = [
#     {"id": 1, "country": 1, "factories": [1, 2]},  # Criança 1 no país 1 quer brinquedos das fábricas 1 e 2
#     {"id": 2, "country": 1, "factories": [2, 3]},  # Criança 2 no país 1 quer brinquedos das fábricas 2 e 3
#     {"id": 3, "country": 2, "factories": [1, 3]},  # Criança 3 no país 2 quer brinquedos das fábricas 1 e 3
# ]

# # Criar o problema de maximização
# problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

# # Variáveis de decisão: x[k][i] - se a criança k recebe um presente da fábrica i
# x = LpVariable.dicts("x", 
#                      ((child["id"], factory["id"]) for child in children for factory in factories), 
#                      cat="Binary")

# # Função objetivo: Maximizar o número de crianças satisfeitas
# problem += lpSum(x[child["id"], factory["id"]] for child in children for factory in factories if factory["id"] in child["factories"])

# # Restrição 1: Cada criança recebe no máximo 1 presente
# for child in children:
#     problem += lpSum(x[child["id"], factory["id"]] for factory in factories if factory["id"] in child["factories"]) <= 1

# # Restrição 2: Capacidade máxima de cada fábrica
# for factory in factories:
#     problem += lpSum(x[child["id"], factory["id"]] for child in children if factory["id"] in child["factories"]) <= factory["capacity"]

# # Restrição 3: Limite de exportação por país
# for country in countries:
#     factories_in_country = [factory for factory in factories if factory["country"] == country["id"]]
#     children_in_country = [child for child in children if child["country"] == country["id"]]
#     problem += lpSum(x[child["id"], factory["id"]] for child in children_in_country for factory in factories_in_country) <= country["export_limit"]

# # Restrição 4: Mínimo de brinquedos por país
# for country in countries:
#     factories_in_country = [factory for factory in factories if factory["country"] == country["id"]]
#     children_in_country = [child for child in children if child["country"] == country["id"]]
#     problem += lpSum(x[child["id"], factory["id"]] for child in children_in_country for factory in factories_in_country) >= country["min_import"]

# # Resolver o problema
# problem.solve()

# # Resultado
# if LpStatus[problem.status] == "Optimal":
#     print("Número máximo de crianças satisfeitas:", value(problem.objective))
#     for child in children:
#         for factory in factories:
#             if x[child["id"], factory["id"]].varValue == 1:
#                 print(f"Criança {child['id']} recebe um presente da fábrica {factory['id']}")
# else:
#     print("Não é possível satisfazer as restrições.")

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
print("Factories:", factory_data)
print("Countries:", country_data)
print("Child Requests:", child_requests)

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
problem.solve()

# Exibir os resultados
if LpStatus[problem.status] == "Optimal":
    print("Número máximo de crianças satisfeitas:", value(problem.objective))
    for k in range(1, children + 1):
        for i in range(1, factories + 1):
            if x[k, i].varValue == 1:
                print(f"Criança {k} recebe um presente da fábrica {i}")
else:
    print("Não é possível satisfazer as restrições.")
