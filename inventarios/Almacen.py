from scipy.optimize import minimize
import numpy as np
from sympy import symbols, sympify

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
        f_exprStr += f"{articulos[articulo]['k']}*{articulos[articulo]['d']}/y{i} + {articulos[articulo]['h']}*y{i}/2 + "
    
    f_exprStr = f_exprStr[:-3]  # Eliminar el último ' + '
    g_exprStr = lineas[-1].strip()
    
    return f_exprStr, g_exprStr, num_articulos

def lagrange_with_minimize(f_exprStr, g_exprStr, numVariables):
    # Convertir expresiones simbólicas a funciones numéricas
    y_symbols = symbols(f'y1:{numVariables + 1}')
    f_expr = sympify(f_exprStr)
    g_expr = sympify(g_exprStr)

    # Crear funciones lambda para evaluación numérica
    f_func = lambda y: float(f_expr.subs({f"y{i+1}": y[i] for i in range(numVariables)}))
    g_func = lambda y: float(g_expr.subs({f"y{i+1}": y[i] for i in range(numVariables)}))
    
    # Restricción de igualdad
    constraint = {'type': 'eq', 'fun': g_func}

    # Solución inicial (valores positivos arbitrarios)
    y0 = np.ones(numVariables)

    # Ejecutar minimización
    result = minimize(f_func, y0, constraints=[constraint], bounds=[(1e-6, None)] * numVariables)

    # Verificar el resultado
    if result.success:
        print("Solución encontrada:")
        # Redondear resultados a enteros
        y_rounded = [int(round(val)) for val in result.x]
        for i, val in enumerate(y_rounded, start=1):
            print(f"y{i} = {val}")
        print(f"Valor mínimo de la función objetivo (redondeado): {f_func(y_rounded):.2f}")
    else:
        print("No se encontró una solución. Razón:", result.message)

if __name__ == '__main__':
    print('Y1 = Leche Y2 = Mantequilla Y3 = Huevos')
    f_str, g_str, num_vars = readData('inventarios/AlmacenRefrigerado.txt')
    lagrange_with_minimize(f_str, g_str, num_vars)
