from sympy import symbols, diff, Eq, solve
import re


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
    
    
    i = 0
    f_exprStr = ''
    for articulo in articulos:
        if(i == 0): var = 'x'
        if(i == 1): var = 'y'
        if(i == 2): var = 'z'
        f_exprStr = f_exprStr + f' {articulos[articulo]['k']}*{articulos[articulo]['d']}/{var} + {articulos[articulo]['h']}*{var}/2 +'
        i=+1
        #print(f_exprStr)


    f_exprStr = f_exprStr[:-1] if f_exprStr.endswith('+') else f_exprStr
    #print(f_exprStr)
    g_exprStr = lineas[-1]
    return f_exprStr, g_exprStr
    pass



def lagrange_multiplier(f_exprSrt, g_exprStr):
    # Definir variables
    x, y, lam = symbols('x y lam')  # Variables y multiplicador de Lagrange
        
    # Función objetivo y restricción
    f_expr = eval(f_exprSrt)  # Función objetivo
    g_expr = eval(g_exprStr)  # Restricción

    print(f"Función objetivo: {f_expr}")
    print(f"Restricción: {g_expr}")

    # Gradiente de f y g
    grad_f = [diff(f_expr, var) for var in (x, y)]
    grad_g = [diff(g_expr, var) for var in (x, y)]

    # Ecuaciones de los multiplicadores de Lagrange
    equations = [
        Eq(grad_f[i] - lam * grad_g[i], 0) for i in range(len(grad_f))
    ]
    equations.append(Eq(g_expr, 0))  # Agregar restricción

    # Resolver el sistema de ecuaciones
    solutions = solve(equations, (x, y, lam))

    # Mostrar soluciones
    print("\nSoluciones encontradas:")
    for sol in solutions:
        # sol es una tupla, con los valores de (x, y, λ)
        x_sol, y_sol, lam_sol = sol  # Extraemos los valores de la tupla

        # Calcular lambda explícitamente usando la relación grad_f / grad_g
        grad_f_eval = [grad_f[i].subs({x: x_sol, y: y_sol}) for i in range(len(grad_f))]
        grad_g_eval = [grad_g[i].subs({x: x_sol, y: y_sol}) for i in range(len(grad_g))]
        calculated_lambda = grad_f_eval[0] / grad_g_eval[0]  # Usamos una componente del gradiente

        print(f"x = {x_sol}, y = {y_sol}, λ (solución simbólica) = {lam_sol}")
        print(f"λ (calculado) = {calculated_lambda}")



if __name__ == '__main__':
    f_exprStr, g_exprStr = readData('inventarios/funciones.txt')
    lagrange_multiplier(f_exprStr, g_exprStr)
