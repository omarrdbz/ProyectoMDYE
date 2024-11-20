import numpy as np


def inventario_un_articulo (demand, setup_cost, holding_cost):
    y = np.sqrt((2 * demand * setup_cost) / holding_cost)
    tcu = (setup_cost * demand / y) + holding_cost* y / 2
    t0 = y/Demand
    n = int (l/(y/Demand))
    le = l - n*t0
    leD = le*demand
    
    print(f'Y = {int(y)} \nTCU = {int(tcu)} \nt0 = {int(t0)} \nn = {n} \nLe = {le} \nLeD = {leD}')


if __name__ == "__main__":  
    Demand = 60 # 
    k = 120  # Costo de pedido
    h = 0.02  # Costo de mantenimiento por unidad
    l = 20
    inventario_un_articulo(demand=Demand, setup_cost=k, holding_cost=h)