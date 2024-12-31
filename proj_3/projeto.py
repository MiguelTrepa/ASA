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

#_______________________________________________________________________________________________________

# Iniciar o problema
# Maximização do número de crianças satisfeitas
problem = LpProblem("Maximize_Satisfied_Children", LpMaximize)

# Variáveis x[k][i] : 1 se a criança k recebe um presente da fábrica i, 0 caso contrário
x = LpVariable.dicts("x", 
                     ((k, i) for k in range(1, children + 1) for i in range(1, factories + 1)), 
                     cat="Binary")

# Objetivo: Maximizar o número de crianças satisfeitas
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

    # Fábricas no país j e crianças fora do país j
    factories_in_country = [f[0] for f in factory_data if f[1] == j]
    children_outof_country = [k for k in range(1, children + 1) if child_requests[k - 1][1] != j]

    problem += lpSum(x[k, i] for i in factories_in_country for k in children_outof_country) <= max_export, f"Country_{j}_Export_Limit"

# Restrição 4: Mínimo de brinquedos por país
for j in range(1, countries + 1):
    min_import = country_data[j - 1][2]

    # Fábricas fora do pais j e crianças no país j
    factories_outof_country = [f[0] for f in factory_data if f[1] == j]
    children_in_country = [k for k in range(1, children + 1) if child_requests[k - 1][1] != j]

    problem += lpSum(x[k, i] for i in factories_outof_country for k in children_in_country) >= min_import, f"Country_{j}_Import_Minimum"

# Resolver o problema
# Sem mensagens de output
problem.solve(PULP_CBC_CMD(msg=False))

# Imprimir o resultado
if LpStatus[problem.status] == "Optimal":
    # Exibir o número máximo de crianças satisfeitas
    print(int(value(problem.objective)))
else:
    # Se não for possível satisfazer as restrições
    print(-1)