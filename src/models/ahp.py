import numpy as np
from datetime import datetime
from src.database.dbcontroller import DBController

def ponderarCriterios():
    bd = DBController()
    bd.connect()
    resulta_nombres =[]
    result_name = bd.fetch_data("SELECT * FROM criterios")
    for row in result_name:
        resulta_nombres.append(row[0])
    result = len(result_name)
    matriz_cuadrada = np.zeros((result, result))

    for i in range(result):
        for j in range(result):
            matriz_cuadrada[i, j] = 1 

    result_relation = bd.fetch_data("SELECT * FROM relaciones")
    for row in result_relation:
        i = resulta_nombres.index(row[0])
        j = resulta_nombres.index(row[1])
        matriz_cuadrada[i, j] = row[2]
        matriz_cuadrada[j, i] = 1 / row[2]
    
    matriz_criterios = matriz_cuadrada
    bd.disconnect()

    
    print("MATRIZ BÁSICA DE CRITERIOS")
    print(matriz_criterios)
    

    suma_columnas = np.sum(matriz_criterios, axis=0)
    print("SUMA DE COLUMNAS")
    print(suma_columnas)

    matriz_div = matriz_criterios / suma_columnas
    print("MATRIZ PONDERADA DE CRITERIOS")
    print(matriz_div)

    pesos_criterios = np.mean(matriz_div, axis=1)
    print("PESOS DE CRITERIOS")
    print(pesos_criterios)
    
    #COMPROBACIÓN
    if not np.allclose(np.sum(matriz_div, axis=0), np.array([1, 1, 1, 1])):
        print("ERROR: La suma de las columnas no es igual a 1")
    if not np.allclose(np.sum(pesos_criterios), 1):
        print("ERROR: La suma de los pesos no es igual a 1")

    return pesos_criterios

def ponderarAlternativas(criterio, usuario='root', carta='Desayuno', seccion='Cafes'):

    bd = DBController()
    platos = []
    platos_precios = []
    bd.connect()
    platos_consult = bd.fetch_data("SELECT * FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?", (carta, usuario, seccion))
    for plato in platos_consult:
        platos.append(plato[0])
        if (criterio == 'precio'):
            platos_precios.append({'plato':platos[0],'precio':plato[7]})
    
    matriz_alternativas = np.zeros((len(platos), len(platos)))

    if (criterio == 'precio'):
        for i in range(len(platos)):
            for j in range(len(platos)):
                if i == j:
                    matriz_alternativas[i, j] = 1
                else:
                    if platos_precios[i]['precio'] - platos_precios[j]['precio'] > 1 and platos_precios[i]['precio'] - platos_precios[j]['precio'] < 3:
                        print(platos_precios[i]['precio']- platos_precios[j]['precio'])
                        matriz_alternativas[i, j] = 1
                        matriz_alternativas[j, i] = 1
                    elif platos_precios[i]['precio'] - platos_precios[j]['precio'] > 3 and platos_precios[i]['precio'] - platos_precios[j]['precio'] < 7:
                        matriz_alternativas[i, j] = 3
                        matriz_alternativas[j, i] = 1/3
                    elif platos_precios[i]['precio'] - platos_precios[j]['precio'] > 7 and platos_precios[i]['precio'] - platos_precios[j]['precio'] < 10:
                        matriz_alternativas[i, j] = 5
                        matriz_alternativas[j, i] = 1/5
                    elif platos_precios[i]['precio'] - platos_precios[j]['precio'] > 10 and platos_precios[i]['precio'] - platos_precios[j]['precio'] < 13:
                        matriz_alternativas[i, j] = 7
                        matriz_alternativas[j, i] = 1/7
                    elif platos_precios[i]['precio'] - platos_precios[j]['precio'] > 13 :
                        matriz_alternativas[i, j] = 9
                        matriz_alternativas[j, i] = 1/9
    
    if (criterio == 'tiempo'):
        for i in range(len(platos)):
            for j in range(len(platos)):
                if i == j:
                    matriz_alternativas[i, j] = 1
                else:
                    tiempo_plato1 = bd.fetch_data("SELECT * FROM pedidos_historicos WHERE usuario = ? AND categoria = ? AND plato=?", (usuario, seccion, platos_consult[i][0]))
                    tiempo_plato2 = bd.fetch_data("SELECT * FROM pedidos_historicos WHERE usuario = ? AND categoria = ? AND plato=?", (usuario, seccion, platos_consult[j][0]))

                    if len(tiempo_plato1) == 0 or len(tiempo_plato2) == 0:
                        print(tiempo_plato1, tiempo_plato2)
                        print("No se encontraron datos para tiempo_plato1 o tiempo_plato2.")
                        matriz_alternativas[i, j] = 1
                    else:
                        tiempo_medio_plato1 = 0
                        for tiempo_partial in tiempo_plato1:
                            tiempo_plato1_init = datetime.strptime(tiempo_partial[6], '%Y-%m-%d %H:%M:%S')
                            tiempo_plato1_init = tiempo_plato1_init.timestamp()

                            tiempo_plato1_end = datetime.strptime(tiempo_partial[7], '%Y-%m-%d %H:%M:%S')
                            tiempo_plato1_end = tiempo_plato1_end.timestamp()
    
                            tardanza_plato1 = tiempo_plato1_end - tiempo_plato1_init

                            tiempo_medio_plato1 += tardanza_plato1
                        
                        tiempo_medio_plato1 = tiempo_medio_plato1 / len(tiempo_plato1)

                        tiempo_medio_plato2 =0
                        for tiempo_partial in tiempo_plato2:
                            tiempo_plato2_init = datetime.strptime(tiempo_partial[6], '%Y-%m-%d %H:%M:%S')
                            tiempo_plato2_init = tiempo_plato2_init.timestamp()

                            tiempo_plato2_end = datetime.strptime(tiempo_partial[7], '%Y-%m-%d %H:%M:%S')
                            tiempo_plato2_end = tiempo_plato2_end.timestamp()

                            tardanza_plato2 = tiempo_plato2_end - tiempo_plato2_init

                            tiempo_medio_plato2 += tardanza_plato2

                        tiempo_medio_plato2 = tiempo_medio_plato2 / len(tiempo_plato2)
                        tardanza_total = tiempo_medio_plato1 - tiempo_medio_plato2
                        if tardanza_total > -101 and tardanza_total < 101:
                            matriz_alternativas[i][j] = 1
                            matriz_alternativas[j][i] = 1
                        elif tardanza_total < 200:
                            matriz_alternativas[i][j] = 3
                            matriz_alternativas[j][i] = 1/3
                        elif tardanza_total < 300:
                            matriz_alternativas[i][j] = 5
                            matriz_alternativas[j][i] = 1/5
                        elif tardanza_total < 400:
                            matriz_alternativas[i][j] = 7
                            matriz_alternativas[j][i] = 1/7
                        elif tardanza_total < 500:
                            matriz_alternativas[i][j] = 9
                            matriz_alternativas[j][i] = 1/9


                        print(tardanza_plato1, tardanza_plato2)
    

    if (criterio == 'popularidad'):
        for i in range(len(platos)):
            for j in range(len(platos)):
                if i == j:
                    matriz_alternativas[i, j] = 1
                else:
                    
    
    bd.disconnect()
    print("MATRIZ BÁSICA DE ALTERNATIVAS PARA EL CRITERIO " + criterio)
    print(matriz_alternativas)

    


def generarmatrizPrecio(usuario='root', carta='Desayuno', seccion='Cafes'):

    matriz_alternativas = np.array([[1, 3, 5], [1/3, 1, 3], [1/5, 1/3, 1]])
    
    print("MATRIZ BÁSICA DE ALTERNATIVAS PARA EL CRITERIO " + criterio)
    print(matriz_alternativas)

    suma_columnas = np.sum(matriz_alternativas, axis=0)

    print("SUMA DE COLUMNAS PARA EL CRITERIO " + criterio)
    print(suma_columnas)

    matriz_div = matriz_alternativas / suma_columnas

    print("MATRIZ PONDERADA DE ALTERNATIVAS PARA EL CRITERIO " + criterio)
    print(matriz_div)

    pesos_alternativas = np.mean(matriz_div, axis=1)
    print("PESOS DE ALTERNATIVAS PARA EL CRITERIO " + criterio)
    print(pesos_alternativas)

    #COMPROBACIÓN
    if not np.allclose(np.sum(matriz_div, axis=0), np.array([1, 1, 1])):
        print("ERROR: La suma de las columnas no es igual a 1")
    if not np.allclose(np.sum(pesos_alternativas), 1):
        print("ERROR: La suma de los pesos no es igual a 1")
    
    return pesos_alternativas




def AHP():
    db = DBController()
    db.connect()
    result = db.fetch_data("SELECT * FROM criterios")
    criterios = []
    for row in result:
        criterios.append(row[0])
    ponderacionCriterios = ponderarCriterios()
    ponderacionAlternativasCriterios =[]
    for criterio in criterios:
        print("\n\n\nCRITERIO: " + criterio)
        ponderacionAlternativasCriterios.append(ponderarAlternativas(criterio))

#    print("\n\n\nPESOS DE LOS CRITERIOS:")
#    print(ponderacionCriterios)
#    print("\n\n\nPESOS DE LAS ALTERNATIVAS PARA CADA CRITERIO:")
#    for ponderacion in ponderacionAlternativasCriterios:
#        print(ponderacion)

