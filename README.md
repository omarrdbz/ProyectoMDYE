# Flujo Máximo (según algoritmo de Ford-Fulkerson)

## Descripción
Se obtiene el modelo de la red desde un archivo de texto `red.txt` para calcular el flujo máximo de un nodo a otro y el flujo residual en la red. Finalmente se mencionan las rutas que pueden ser eliminadas (sólo si se da el caso de que no son utilizadas)

## Instrucciones de Uso
1. Crear o modificar el archivo llamado `red.txt`.
2. Ejecutar el programa.
3. Disfrutar :)

## Importante: Formato del archivo de entrada
El archivo de entrada tiene que seguir el siguiente formato:

1. **Primera línea**: Número de nodos en la red.
2. **Segunda línea**: Lista de los nombres de los nodos, separados por comas (ejemplo, `A,B,C,D,E,F,G,H`).
3. **Tercera línea**: Nombre del nodo origne y nombre del nodo destino, separados por una coma (ejemplo, `A,H`).
4. **Líneas restantes**: Cada línea es una conexión entre nodos con el formato `nodo_origen nodo_destino capacidad` (ejemplo, `A B 4`). El orden importa puesto que es un grafo dirigido

### Ejemplo de archivo de entrada (`red.txt`)
```
8
A,B,C,D,E,F,G,H
A,H
A B 4
A C 2
B D 3
B E 6
C E 1
D F 5
E F 2
E G 3
F H 8
G H 2
```

## Posibles Errores y Disclaimer de responsabilidad :)
- **Archivo no encontrado**: Si el archivo de `red.txt` no existe.
- **Formato de archivo inválido**: Si el archivo no sigue `estrictamente` el formato anterior.

