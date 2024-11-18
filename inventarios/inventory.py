from sympy import symbols, diff, Eq, solve, sympify

def readData(ruta_archivo):
    articulos = {}
    with open(ruta_archivo, 'r') as archivo:
        lineas = archivo.readlines()

    num_articulos = int(lineas[0].split('=')[1].strip())

    for i in range(1, num_articulos + 1):
        articulo = f"articulo{i}"
        articulos[articulo] = {}

        for linea in lineas:
            if f"k{i}" in linea:
                articulos[articulo]["k"] = float(linea.split('=')[1].strip())
            if f"d{i}" in linea:
                articulos[articulo]["d"] = float(linea.split('=')[1].strip())
            if f"h{i}" in linea:
                articulos[articulo]["h"] = float(linea.split('=')[1].strip())
            if f"dimension{i}" in linea:
                articulos[articulo]["dimension"] = int(linea.split('=')[1].strip())

    f_exprStr = ''
    for i, articulo in enumerate(articulos, start=1):
        f_exprStr += f"{articulos[articulo]['k']}*{articulos[articulo]['d']}/x{i} + {articulos[articulo]['h']}*x{i}/2 + "
    
    f_exprStr = f_exprStr[:-3]  # Eliminar el último ' + '
    g_exprStr = lineas[-1].strip()
    
    return f_exprStr, g_exprStr, num_articulos

def lagrange_multiplier(f_exprStr, g_exprStr, numVariables):
    # Definir variables simbólicas
    variables = symbols(f'x1:{numVariables + 1}')  # Genera x1, x2, ..., xn
    lam = symbols('lam')  # Multiplicador de Lagrange

    # Función objetivo y restricción
    f_expr = sympify(f_exprStr)  # Convierte a expresión simbólica
    g_expr = sympify(g_exprStr)

    print(f"Función objetivo: {f_expr}")
    print(f"Restricción: {g_expr}")

    # Gradientes de f y g
    grad_f = [diff(f_expr, var) for var in variables]
    grad_g = [diff(g_expr, var) for var in variables]

    # Ecuaciones de los multiplicadores de Lagrange
    equations = [
        Eq(grad_f[i] - lam * grad_g[i], 0) for i in range(len(variables))
    ]
    equations.append(Eq(g_expr, 0))  # Agregar la restricción

    # Resolver el sistema de ecuaciones
    solutions = solve(equations, (*variables, lam))

    # Mostrar soluciones
    print("\nSoluciones encontradas:")
    for sol in solutions:
        if isinstance(sol, dict):
            # Si la solución es un diccionario
            var_solutions = [int(round(sol[var].evalf())) for var in variables]
            lam_solution = int(round(sol[lam].evalf()))
        elif isinstance(sol, tuple):
            # Si la solución es una tupla
            #int(x_sol.evalf()) if x_sol.is_real else None
            var_solutions = [int(round(val.evalf())) if val.is_real else None for val in sol[:-1]]
            lam_solution = int(round(sol[-1].evalf())) if sol[-1].is_real else None
        else:
            raise TypeError("Formato inesperado en las soluciones devueltas por solve.")

        # Mostrar soluciones enteras
        variable_values = ", ".join(f"{var} = {val}" for var, val in zip(variables, var_solutions))
        print(f"{variable_values}, λ = {lam_solution}")


if __name__ == '__main__':
    print('<<<<<<<<<<<<< X1 = Harina X2 = Azucar >>>>>>>>>>>>>>>>')
    f_str, g_str, num_vars = readData('inventarios\AlmacenSinRefrigeracion.txt')
    lagrange_multiplier(f_str, g_str, num_vars)

    print('<<<<<<<<<<<<< X1 = Leche X2 = Mantequilla X3 = Huevos >>>>>>>>>>>>>>>>')
    f_str, g_str, num_vars = readData('inventarios\AlmacenRefrigerado.txt')
    lagrange_multiplier(f_str, g_str, num_vars)
    
    

