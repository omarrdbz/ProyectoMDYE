import pulp

def leer_problema(file_path):
    """
    Lee la configuración de un problema de transbordo desde un archivo de texto.

    Args:
        file_path (str): Ruta del archivo de texto.

    Returns:
        dict: Diccionario con nodos, oferta, demanda, conexiones y costos
    """
    
    with open(file_path, "r") as file:
        lines = file.readlines()

    problem_data = {
        "nodos": [],
        "oferta": {},
        "demanda": {},
        "conexiones": [],
        "costos": {},
    }

    problem_data["nodos"] = lines[0].strip().split(",") # Nodos en la red
    
    for oferta in lines[1].split(","): # Nodos de oferta
        nodo, cantidad = oferta.strip().split(":")
        problem_data["oferta"][nodo] = int(cantidad)
    
    for demanda in lines[2].split(","): # Nodos de demanda
        nodo, cantidad = demanda.strip().split(":")
        problem_data["demanda"][nodo] = int(cantidad)

    for conexion in lines[3:]:
        origen, destino, costo = conexion.split()
        problem_data["conexiones"].append((origen, destino))
        problem_data["costos"][(origen, destino)] = int(costo)
    
    return problem_data

# Función para revisar que la oferta y la demanda sea la misma, y si no la corrige 
def revisar_balance(problem_data):
    """
    Args:
        problem_data (dict): Diccionario con nodos, oferta, demanda, conexiones y costos

    Returns:
        dict: Diccionario con nodos, oferta, demanda, conexiones y costos. Tiene oferta y demanda balanceada
    """

    oferta_total = sum(problem_data["oferta"].values())
    demanda_total = sum(problem_data["demanda"].values())

    if oferta_total == demanda_total:
        return problem_data
    
    if oferta_total > demanda_total:
        problem_data["nodos"].append("Sobrante")
        problem_data["demanda"]["Sobrante"] = oferta_total - demanda_total
        for nodo_oferta in problem_data["oferta"].keys():  
          problem_data["conexiones"].append((nodo_oferta, "Sobrante"))
          problem_data["costos"][(nodo_oferta, "Sobrante")] = 0
    else:
        problem_data["nodos"].append("Faltante")
        problem_data["oferta"]["Faltante"] = demanda_total - oferta_total
        for nodo_demanda in problem_data["demanda"].keys():  
          problem_data["conexiones"].append(("Faltante", nodo_demanda))
          problem_data["costos"][("Faltante", nodo_demanda)] = 0
    
    return problem_data

# Función para resolver el problema de transbordo
def resolver_problema_transbordo(problem_data):
    """
    Args:
        problem_data (dict): Diccionario con nodos, oferta, demanda, conexiones y costos

    Returns:
        dict: Flujo óptimo por arco y valor óptimo de la función objetivo.
    """

    costos = problem_data["costos"]
    oferta = problem_data["oferta"]
    demanda = problem_data["demanda"]
    nodos = problem_data["nodos"]
    conexiones = problem_data["conexiones"]

    # Crear el modelo de optimización
    modelo = pulp.LpProblem("LP_Problem", pulp.LpMinimize)

    # Variables de decisión
    variables = pulp.LpVariable.dicts("Conexiones", conexiones, lowBound=0, cat="Integer")

    # Función objetivo
    modelo += pulp.lpSum(variables[i, j] * costos[i, j] for i, j in conexiones), "Costo_Total"

    # Restricciones de oferta y demanda
    for nodo in nodos:
        if nodo in oferta:
            # Nodo fuente: saliente - entrante = oferta
            modelo += (
                pulp.lpSum(variables[nodo, j] for j in nodos if (nodo, j) in conexiones) -
                pulp.lpSum(variables[i, nodo] for i in nodos if (i, nodo) in conexiones) == oferta[nodo],
                f"Oferta_{nodo}"
            )
        elif nodo in demanda:
            # Nodo destino: entrante - saliente = demanda
            modelo += (
                pulp.lpSum(variables[i, nodo] for i in nodos if (i, nodo) in conexiones) -
                pulp.lpSum(variables[nodo, j] for j in nodos if (nodo, j) in conexiones) == demanda[nodo],
                f"Demanda_{nodo}"
            )
        else:
            # Nodo transbordo: saliente = entrante
            modelo += (
                pulp.lpSum(variables[i, nodo] for i in nodos if (i, nodo) in conexiones) ==
                pulp.lpSum(variables[nodo, j] for j in nodos if (nodo, j) in conexiones),
                f"Transbordo_{nodo}"
            )

    # Resolver el modelo
    modelo.solve(pulp.PULP_CBC_CMD(msg=False))

    envios = {}
    mensaje = ""
    costo_total = 0

    # Resultados
    if modelo.status == pulp.LpStatusOptimal:
        envios = { (i, j): variables[i, j].varValue for i, j in conexiones }
        costo_total = pulp.value(modelo.objective)
        mensaje = "Solución encontrada."
    elif modelo.status == pulp.LpStatusInfeasible:
        mensaje = "No existe solución factible para el problema."
    elif modelo.status == pulp.LpStatusUnbounded:
        mensaje = "El problema no está acotado." 
    else:
        mensaje = "No se pudo resolver el problema."

    return { "Status": modelo.status, "Envios": envios, "Costo_Total": costo_total, "Mensaje": mensaje }

if __name__ == "__main__":
    # Leer datos del problema de archivo
    file_path = "red.txt"
    problem_data = leer_problema(file_path)

    # Revisar que la oferta y la demanda sea la misma, y si no la corrige
    problem_data = revisar_balance(problem_data)

    # Resolver problema
    resultado = resolver_problema_transbordo(problem_data)

    #Mostrar resultados
    print("Resultados del problema de transbordo:")
    print(resultado["Mensaje"])

    if(resultado["Status"] == pulp.LpStatusOptimal):
        print("Envíos:")
        for arco, flujo in resultado["Envios"].items():
            if flujo == 0: continue
            print(f"{arco}: {flujo}")
        print(f"Costo total: {resultado['Costo_Total']}")

