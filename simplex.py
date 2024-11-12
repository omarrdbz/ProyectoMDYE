from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable, value, lpSum, PULP_CBC_CMD 
import warnings

# Ignorar advertencias de desuso
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Función para determinar el tipo de problema (maximización o minimización)
def get_problem_type():
    """
    Solicita al usuario que indique si el problema es de maximización o minimización.
    
    Returns:
        bool: True si es un problema de minimización, False si es de maximización.
    """
    while True:
        choice = input("¿Es un problema de maximización o minimización? (max/min): ").strip().lower()
        if choice in ['max', 'min']:
            return choice == 'min'
        else:
            print("Entrada inválida. Escribe 'max' para maximización o 'min' para minimización.")

# Función para obtener la función objetivo
def get_objective_function():
    """
    Solicita al usuario los coeficientes de la función objetivo.
    
    Returns:
        list[float]: Lista de coeficientes de la función objetivo.
    """
    print("Introduce los coeficientes de la función objetivo (separados por comas):")
    return list(map(float, input().split(',')))

# Función para obtener las restricciones
def get_constraints():
    """
    Solicita al usuario ingresar las restricciones del problema, incluyendo los coeficientes, el tipo de desigualdad, y el lado derecho.
    
    Returns:
        list[tuple]: Lista de restricciones, donde cada restricción es un tuple con:
                     (coeficientes, signo, lado derecho).
    """
    constraints = []
    while True:
        print("\nIntroduce los coeficientes de la restricción (separados por comas), o deja en blanco para terminar:")
        line = input().strip()
        if not line:
            break
        coefficients = list(map(float, line.split(',')))
        
        # Solicitar el tipo de restricción
        while True:
            sign = input("Introduce el tipo de restricción (<=, =, >=): ").strip()
            if sign in ['<=', '=', '>=']:
                break
            else:
                print("Entrada inválida. Usa '<=', '=' o '>='.")
        
        # Solicitar el lado derecho de la restricción
        rhs = float(input("Introduce el lado derecho de la restricción: "))
        constraints.append((coefficients, sign, rhs))
    
    return constraints

# Función principal para resolver el problema
def solve_problem():
    """
    Resuelve un problema de programación lineal utilizando PuLP. Solicita al usuario definir el tipo de problema,
    la función objetivo y las restricciones.
    """
    # Obtener tipo de problema, función objetivo y restricciones del usuario
    is_minimization = get_problem_type()
    objective       = get_objective_function()
    constraints     = get_constraints()

    # Definir el problema (maximización o minimización)
    if is_minimization:
        problem = LpProblem("LP_Problem", LpMinimize)
    else:
        problem = LpProblem("LP_Problem", LpMaximize)

    # Crear las variables de decisión (asumiendo todas tienen un límite inferior de 0)
    num_vars = len(objective)
    variables = [LpVariable(f"x{i+1}", lowBound=0) for i in range(num_vars)]

    # Definir la función objetivo
    problem += lpSum([objective[i] * variables[i] for i in range(num_vars)]), "Objective_Function"

    # Agregar restricciones
    for coeffs, sign, rhs in constraints:
        if sign == "<=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) <= rhs
        elif sign == "=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) == rhs
        elif sign == ">=":
            problem += lpSum([coeffs[i] * variables[i] for i in range(num_vars)]) >= rhs

    # Resolver el problema usando el solver CBC (por defecto de PuLP)
    problem.solve(PULP_CBC_CMD(msg=False))

    # Imprimir los resultados dependiendo del estado de la solución
    if LpStatus[problem.status] == "Optimal":
        print("\nSolución encontrada:")
        optimal_value = value(problem.objective)
        print("\tValor óptimo:", optimal_value)
        print("\tValores de las variables:")
        for var in variables:
            print(f"\t    {var.name}: {var.varValue}")

        # Verificación de soluciones múltiples mediante el costo reducido (reduced cost)
        multiple_solutions = False
        for var in variables:
            # Si la variable es no básica (valor igual a 0) y su costo reducido es cero, existen soluciones múltiples
            if var.varValue == 0 and abs(var.dj) < 1e-5:
                multiple_solutions = True
                break

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
    solve_problem()


# LpProblem: define un problema de programación lineal. Puede ser de maximización (LpMaximize) o minimización (LpMinimize).
# LpVariable: las variables tienen un límite inferior de 0 (lowBound=0), lo cual significa que ninguna es negativa.
# lpSum: Se utiliza para definir una suma lineal al definir la función objetivo y las restricciones.