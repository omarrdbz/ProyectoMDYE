import numpy as np


def inventario_un_articulo (demand, setup_cost, holding_cost):
    y = np.sqrt((2 * demand * setup_cost) / holding_cost)
    tcu = (setup_cost * demand / y) + holding_cost* y / 2
    t0 = y/Demand
    n = int (l/(y/Demand))
    
    print(f'Y = {y} \nTCU = {tcu} \nt0 = {t0} \nn = {n}')


if __name__ == "__main__":
    # Parámetros
    Demand = 30 # Demanda 
    k = 100  # Costo de pedido
    h = 0.05  # Costo de mantenimiento por unidad
    l = 30
    inventario_un_articulo(demand=Demand, setup_cost=k, holding_cost=h)