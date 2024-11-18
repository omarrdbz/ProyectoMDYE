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
    # Parametros para mantequilla
    #Volumen maximo = 350,000cm3
    """
    Harina
        X1 = 181 conchas * 100g por concha  = 18100
        X2 = 105 cuernitos * 90g por cuerno = 9450
        X3 = 83 donas de chocolate * 150g por dona = 12450

        Total de harina ocupada 40,000g

    Azucar
        X1 = 181 conchas * 90g  por concha  = 16290
        X2 = 105 cuernitos * 50g  por cuerno = 5250
        X3 = 83 donas de chocolate * 150g  por dona = 12450

        Total de azucar ocupada 34.000g
 
    Aceite
        X1 = 181 conchas * 40   por concha  = 7240
        X2 = 105 cuernitos *  50  por cuerno = 5250
        X3 = 83 donas de chocolate * 50  por dona = 4150    

        Total de Aceite 16640

    Mantequilla
        X1 = 181 conchas * 20 por concha  = 3620
        X2 = 105 cuernitos * 100 por cuerno = 10500
        X3 = 83 donas de chocolate * 70 por dona =  5810   

        Total de Mantequilla por tanda 20000 = 20Kg
        Total de Mantequilla final = 60kg
        Tantas totales 3
    """

    Demand = 60 # 
    k = 120  # Costo de pedido
    h = 0.02  # Costo de mantenimiento por unidad
    l = 20
    inventario_un_articulo(demand=Demand, setup_cost=k, holding_cost=h)