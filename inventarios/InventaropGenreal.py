import numpy as np


def inventario_un_articulo (demand, setup_cost, holding_cost):
    y = np.sqrt((2 * demand * setup_cost) / holding_cost)
    tcu = (setup_cost * demand / y) + holding_cost* y / 2
    t0 = y/Demand
    n = int (l/(y/Demand))
    le = l - n*t0
    leD = le*demand
    
    print(f'Y = {int(y)} \nTCU = {int(tcu)} \nt0 = {int(t0)} \nn = {n} \nLe = {int(le)} \nLeD = {int(leD)}')


if __name__ == "__main__":  
    ## Azucar
    Demand = 102 # 
    k = 45  # Costo de pedido
    h = 0.015  # Costo de mantenimiento por unidad
    l = 20
    print('Inventario de Azucar')
    inventario_un_articulo(demand=Demand, setup_cost=k, holding_cost=h)
    ## Harina
    Demand = 120 #
    k = 32  # Costo de pedido
    h = 0.03  # Costo de mantenimiento por unidad
    l = 20
    print('Inventario de Harina')
    inventario_un_articulo(demand=Demand, setup_cost=k, holding_cost=h)
    