def dfs(capacity, source, sink, parent, visited):
    visited[source] = True
    if source == sink:
        return True
    
    for v, cap in enumerate(capacity[source]):
        if not visited[v] and cap > 0:  # Si hay capacidad disponible y no hemos visitado el nodo
            parent[v] = source
            if dfs(capacity, v, sink, parent, visited):
                return True
    return False

def ford_fulkerson(capacity, source, sink):
    parent = [-1] * len(capacity)
    max_flow = 0
    
    residual_capacity = [row[:] for row in capacity]  # Copia de la capacidad original para mantener el residual
    
    while True:
        visited = [False] * len(capacity)
        if not dfs(residual_capacity, source, sink, parent, visited):
            break
        
        # Encontrar la capacidad mínima en el camino aumentante
        path_flow = float('Inf')
        s = sink
        while s != source:
            path_flow = min(path_flow, residual_capacity[parent[s]][s])
            s = parent[s]
        
        # Actualizar las capacidades residuales de las aristas y las aristas inversas
        v = sink
        while v != source:
            u = parent[v]
            residual_capacity[u][v] -= path_flow
            residual_capacity[v][u] += path_flow
            v = parent[v]
        
        max_flow += path_flow
    
    return max_flow, residual_capacity

def main():
    print("\n-------------------------Flujo máximo (según algoritmo de Ford-Fulkerson)-------------------------")
    
    # Leer datos desde archivo
    file_name = ".\\flujo maximo\\red.txt"
    try:
        with open(file_name, 'r', encoding="utf-8") as file:
            print("\nObteniendo el modelo de red desde el archivo de texto 'red.txt'...")
            lines = file.readlines()
            
            # Leer número de nodos
            num_nodes = int(lines[0].strip())
            
            # Leer nombres de los nodos
            node_names = lines[1].strip().split(',')
            if len(node_names) != num_nodes:
                print("Error: La cantidad de nombres de nodos no coincide con el número de nodos.")
                return
            
            # Leer fuente y sumidero
            source_name, sink_name = lines[2].strip().split(',')
            if source_name not in node_names or sink_name not in node_names:
                print("Error: Nombres de fuente o sumidero no válidos.")
                return
            source = node_names.index(source_name)
            sink = node_names.index(sink_name)
            
            # Inicializar capacidades
            capacity = [[0] * num_nodes for _ in range(num_nodes)]
            
            # Leer conexiones
            for line in lines[3:]:
                origen_name, destino_name, cap = line.strip().split()
                cap = int(cap)
                if origen_name in node_names and destino_name in node_names:
                    origen = node_names.index(origen_name)
                    destino = node_names.index(destino_name)
                    capacity[origen][destino] = cap
                else:
                    print(f"Error: Nombres de nodos inválidos en la conexión: {origen_name} -> {destino_name}")
                    return
            
            print("\nCalculando flujo máximo...")

            max_flow, final_capacity = ford_fulkerson(capacity, source, sink)
            print(f"\nEl flujo máximo desde el nodo {source_name} hasta el nodo {sink_name} es: {max_flow}\n")
            print("Flujo residual en cada conexión:")
            areNotNecessary = []
            for i in range(num_nodes):
                print("--------------------------------------------------------------------")
                for j in range(num_nodes):
                    if capacity[i][j] > 0:  # Solo imprimir conexiones en la dirección original
                        flujo_utilizado = capacity[i][j] - final_capacity[i][j]
                        capacidad_restante = final_capacity[i][j]
                        if flujo_utilizado > 0 or capacidad_restante > 0:
                            print(f"De nodo {node_names[i]} a nodo {node_names[j]}: capacidad restante {capacidad_restante}, flujo utilizado {flujo_utilizado}")
                        if flujo_utilizado == 0:
                            areNotNecessary.append(f"La ruta de {node_names[i]} a {node_names[j]} puede ser eliminada")
            
            print("\nRutas no necesarias:")
            print("--------------------------------------------------------------------")
            for notNecessaryRoute in areNotNecessary:
                print(notNecessaryRoute)
            print("--------------------------------------------------------------------\n")

    except FileNotFoundError:
        print("Error: No se pudo encontrar el archivo especificado.")
    except ValueError:
        print("Error: Formato de archivo no válido.")

if __name__ == "__main__":
    main()