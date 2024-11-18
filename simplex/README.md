# Simplex para problemas de Programación Lineal

## Descripción
Calcula el valor óptimo de la función objetivo y las variables. Muestra también si la solución es única, tiene mútliples soluciones, no hay solución factible o el problema no está acotado.

El modelo matemático lo obtiene desde un archivo de texto llamado: `simplex.txt`.



## Instrucciones de Uso
1. Crear o modificar el archivo llamado `simplex.txt`.
2. Ejecutar el programa.
3. Revisar los resultados en la consola.


## Importante: Formato del Archivo de Entrada
El archivo de entrada tiene que seguir el siguiente formato:

1. **Primera línea**: Tipo de optimización (`max` o `min`).
2. **Segunda línea**: Coeficientes de la función objetivo, separados por comas (por ejemplo, `3,5`).
3. **Líneas restantes**: Restricciones, una por línea, en el formato:
   ```
   coeficientes separados por comas; signo; valor del lado derecho
   ```
   Nótese que cada parte debe estar separada por un punto y coma `;`

### Ejemplo de archivo de entrada (`simplex.txt`)
```txt
max
3,5
1,0;<=;4
0,2;>=;3
1,1;=;5
```
Representa el siguiente modelo:
- **Función objetivo**: `3x1 + 5x2`
- **Restricciones**:
  - `x1 <= 4`
  - `2x2 >= 3`
  - `x1 + x2 = 5`


## Posibles Errores y Disclaimer
- **Archivo no encontrado**: Si el archivo `simplex.txt` no existe.
- **Formato de archivo inválido**: Si el archivo no sigue *estrictamente* el formato anterior.


## Requisitos
- **PuLP**: Biblioteca. Instalarla con:
  ```bash
  pip install pulp
  ```



