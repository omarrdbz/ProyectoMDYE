# Optimización de Inventarios con Multiplicadores de Lagrange

# Descripcion
Este programa calcula el valor óptimo de la función objetivo y las cantidades de cada artículo en inventario, cumpliendo restricciones de capacidad o recursos mediante el método de multiplicadores de Lagrange. El modelo matemático se obtiene desde archivos de texto y se resuelve utilizando la biblioteca scipy.optimize.minimize.

# Instrucciones de uso
    1. Preparar los archivos de entrada: Crear o modificar archivos con la información de los artículos y restricciones.
    2. Ejecutar el programa: Inicia el script desde la consola.
    3. Consultar los resultados: Los valores óptimos de las variables y el costo mínimo se mostrarán en la consola.

# Formato del Archivo de Entrada
El archivo de entrada debe contener:
    1. **Primera línea** : Número total de artículos: 
        num_articulos = <valor>
    2. **Siguientes líneas** : Parámetros para cada artículo, en el formato:
        k<índice> = <valor>
        d<índice> = <valor>
        h<índice> = <valor>
        dimension<índice> = <valor>
    3. Última línea: Restricción de igualdad en formato simbólico:
        <expresión simbólica>

### Ejemplo de archivo de entrada (`inventarios\AlmacenSinRefrigeracion.txt`)
```txt
num_articulos = 2
k1 = 100
d1 = 50
h1 = 1.2
dimension1 = 1
k2 = 200
d2 = 40
h2 = 1.5
dimension2 = 1
y1 + y2 - 1000
```


Representa el siguiente modelo:
- **Función objetivo**: `3x1 + 5x2`
- **Restricciones**:
  - `x1 <= 4`
  - `2x2 >= 3`
  - `x1 + x2 = 5`

Este archivo representa:
- **Dos artículos con los siguientes parámetros**:
    *Artículo 1*: k=100, d=50, h=1.2, dimension=1
    *Artículo 2*: k=200, d=40, h=1.5, dimension=1
    *Restricción*: y1 + y2 = 1000

# Posibles Errores
- **Archivo no encontrado** : Si el archivo de entrada no existe.
- **Formato inválido**: Si el archivo no sigue el formato especificado.
- **Restricciones incompatibles**: Si la restricción no permite encontrar una solución.

# Requisitos
- **Python 3.8 o superior.**
- **Bibliotecas**: pip install scipy numpy sympy