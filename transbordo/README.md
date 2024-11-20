# Resolución de Problemas de Transbordo

Este proyecto implementa un sistema para resolver problemas de optimización de transbordo utilizando la biblioteca `PuLP` en Python. Se enfoca en minimizar costos de transporte sujetos a restricciones de oferta y demanda, balanceando automáticamente el problema si es necesario.

## Características

- **Lectura de datos desde un archivo**:
  La configuración del problema (nodos, oferta, demanda, conexiones y costos) se lee desde un archivo de texto estructurado.

- **Balanceo de oferta y demanda**:
  Si la oferta y la demanda no coinciden, se ajusta el problema añadiendo nodos ficticios ("Sobrante" o "Faltante") con costos asociados de 0.

- **Resolución del problema de transbordo**:
  Se utiliza programación lineal para minimizar el costo total de transporte, respetando las restricciones de oferta, demanda y conservación de flujo en nodos de transbordo.

- **Resultados detallados**:
  Muestra los envíos óptimos por conexión y el costo total asociado. Incluye manejo de casos donde no exista solución factible o el problema sea no acotado.

---

## Requisitos

- **Python 3.8+**
- Biblioteca `PuLP`:

  ```bash
  pip install pulp
