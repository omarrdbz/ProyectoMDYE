from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable, value, lpSum, PULP_CBC_CMD
import warnings

# Ignorar advertencias de desuso
warnings.filterwarnings("ignore", category=DeprecationWarning)

def read_problem_from_file(file_path):
    """
    Lee la configuración de un problema de programación lineal desde un archivo de texto.

    Args:
        file_path (str): Ruta del archivo de texto.

    Returns:
        dict: Diccionario con tipo de problema, función objetivo y restricciones.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    problem_data = {}
    problem_data['type'] = lines[0].strip().lower()  # Tipo de problema: max o min
    problem_data['objective'] = list(map(float, lines[1].strip().split(',')))  # Función objetivo

    constraints = []
    for line in lines[2:]:
        if line.strip():
            parts = line.strip().split(';')
            coefficients = list(map(float, parts[0].split(',')))
            sign = parts[1].strip()
            rhs = float(parts[2].strip())
            constraints.append((coefficients, sign, rhs))
    problem_data['constraints'] = constraints

    return problem_data

def solve_problem_from_file(file_path):
    """
    Resuelve un problema de programación lineal definido en un archivo de texto.

    Args:
        file_path (str): Ruta del archivo de texto con la definición del problema.
    """
    # Leer datos del problema desde el archivo
    problem_data = read_problem_from_file(file_path)

    # Determinar el tipo de problema
    is_minimization = problem_data['type'] == 'min'

    # Crear el problema
    if is_minimization:
        problem = LpProblem("LP_Problem", LpMinimize)
    else:
        problem = LpProblem("LP_Problem", LpMaximize)

    # Crear las variables de decisión
    num_vars = len(problem_data['objective'])
    variables = [LpVariable(f"x{i+1}", lowBound=0,  cat="Integer") for i in range(num_vars)]

    # Definir la función objetivo
    problem += lpSum([problem_data['objective'][i] * variables[i] for i in range(num_vars)]), "Objective_Function"

    # Agregar restricciones
    for coeffs, sign, rhs in problem_data['constraints']:
        if sign == "<=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) <= rhs
        elif sign == "=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) == rhs
        elif sign == ">=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) >= rhs

    # Resolver el problema usando el solver CBC
    problem.solve(PULP_CBC_CMD(msg=False))

    # Imprimir los resultados dependiendo del estado de la solución
    if LpStatus[problem.status] == "Optimal":
        print("\nSolución encontrada:")
        optimal_value = round(value(problem.objective))
        print("\tValor óptimo:", optimal_value)
        print("\tValores de las variables:")
        for var in variables:
            print(f"\t    {var.name}: {var.varValue}")

        # Verificar soluciones múltiples
        multiple_solutions = any(var.varValue == 0 and abs(var.dj) < 1e-5 for var in variables)
        if multiple_solutions:
            print("\nEl problema tiene soluciones múltiples (soluciones infinitas).\n")
        else:
            print("\nEl problema tiene una única solución óptima.\n")

    elif LpStatus[problem.status] == "Infeasible":
        print("\nNo existe solución factible para el problema.\n")
    elif LpStatus[problem.status] == "Unbounded":
        print("\nEl problema no está acotado.\n")
    else:
        print("\nNo se pudo resolver el problema.\n")

# Punto de entrada principal del script
if __name__ == "__main__":
    file_path = ".\\simplex\\simplex.txt"
    solve_problem_from_file(file_path)