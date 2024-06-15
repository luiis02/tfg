import numpy as np
from datetime import datetime
from src.database.dbcontroller import DBController

def ponderarCriterios(bd):
    result_name = bd.fetch_data("SELECT * FROM criterios")
    resulta_nombres = [row[0] for row in result_name]
    result = len(result_name)
    matriz_cuadrada = np.ones((result, result))

    result_relation = bd.fetch_data("SELECT * FROM relaciones")
    for row in result_relation:
        i, j, value = resulta_nombres.index(row[0]), resulta_nombres.index(row[1]), row[2]
        matriz_cuadrada[i, j] = value
        matriz_cuadrada[j, i] = 1 / value
    
    print("MATRIZ BÁSICA DE CRITERIOS")
    print(matriz_cuadrada)

    suma_columnas = np.sum(matriz_cuadrada, axis=0)
    print("SUMA DE COLUMNAS")
    print(suma_columnas)

    matriz_div = matriz_cuadrada / suma_columnas
    print("MATRIZ PONDERADA DE CRITERIOS")
    print(matriz_div)

    pesos_criterios = np.mean(matriz_div, axis=1)
    print("PESOS DE CRITERIOS")
    print(pesos_criterios)
    
    # COMPROBACIÓN
    if not np.allclose(np.sum(matriz_div, axis=0), 1):
        print("ERROR: La suma de las columnas no es igual a 1")
    if not np.allclose(np.sum(pesos_criterios), 1):
        print("ERROR: La suma de los pesos no es igual a 1")

    return pesos_criterios

def ponderarAlternativas(bd, criterio, usuario='root', carta='Desayuno', seccion='Cafes'):
    platos_consult = bd.fetch_data(
        "SELECT * FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?",
        (carta, usuario, seccion)
    )
    platos = [plato[0] for plato in platos_consult]

    if not platos:
        return []

    matriz_alternativas = np.ones((len(platos), len(platos)))

    if criterio == 'precio':
        platos_precios = [{'plato': plato[0], 'precio': plato[7]} for plato in platos_consult]
        for i in range(len(platos)):
            for j in range(len(platos)):
                if i != j:
                    precio_diff = platos_precios[i]['precio'] - platos_precios[j]['precio']
                    if 1 < precio_diff < 3:
                        matriz_alternativas[i, j] = 1
                        matriz_alternativas[j, i] = 1
                    elif 3 < precio_diff < 7:
                        matriz_alternativas[i, j] = 1/3
                        matriz_alternativas[j, i] = 3
                    elif 7 < precio_diff < 10:
                        matriz_alternativas[i, j] = 1/5
                        matriz_alternativas[j, i] = 5
                    elif 10 < precio_diff < 13:
                        matriz_alternativas[i, j] = 1/7
                        matriz_alternativas[j, i] = 7
                    elif precio_diff > 13:
                        matriz_alternativas[i, j] = 1/9
                        matriz_alternativas[j, i] = 9

    elif criterio in ['tiempo', 'popularidad']:
        tiempos_popularidad = {}
        for plato in platos:
            tiempos_popularidad[plato] = bd.fetch_data(
                "SELECT * FROM pedidos_historicos WHERE usuario = ? AND categoria = ? AND plato = ?",
                (usuario, seccion, plato)
            )

        for i in range(len(platos)):
            for j in range(len(platos)):
                if i != j:
                    if criterio == 'tiempo':
                        tiempo1 = tiempos_popularidad[platos[i]]
                        tiempo2 = tiempos_popularidad[platos[j]]

                        if not tiempo1 or not tiempo2:
                            continue

                        tiempo_medio1 = np.mean([
                            (datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')).total_seconds()
                            for row in tiempo1
                        ])
                        tiempo_medio2 = np.mean([
                            (datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S') - datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S')).total_seconds()
                            for row in tiempo2
                        ])
                        diff = tiempo_medio1 - tiempo_medio2
                        if -101 < diff < 101:
                            matriz_alternativas[i, j] = 1
                            matriz_alternativas[j, i] = 1
                        elif diff < 200:
                            matriz_alternativas[i, j] = 3
                            matriz_alternativas[j, i] = 1/3
                        elif diff < 300:
                            matriz_alternativas[i, j] = 5
                            matriz_alternativas[j, i] = 1/5
                        elif diff < 400:
                            matriz_alternativas[i, j] = 7
                            matriz_alternativas[j, i] = 1/7
                        else:
                            matriz_alternativas[i, j] = 9
                            matriz_alternativas[j, i] = 1/9

                    elif criterio == 'popularidad':
                        popu1 = len(tiempos_popularidad[platos[i]])
                        popu2 = len(tiempos_popularidad[platos[j]])

                        if popu1 > popu2:
                            matriz_alternativas[i, j] = 1
                            matriz_alternativas[j, i] = 1
                        elif popu1 < popu2:
                            matriz_alternativas[i, j] = 1/3
                            matriz_alternativas[j, i] = 3

    print(f"MATRIZ BÁSICA DE ALTERNATIVAS PARA EL CRITERIO {criterio}")
    print(matriz_alternativas)

    suma_columnas = np.sum(matriz_alternativas, axis=0)
    print(f"SUMA DE COLUMNAS PARA EL CRITERIO {criterio}")
    print(suma_columnas)

    matriz_div = matriz_alternativas / suma_columnas
    print(f"MATRIZ PONDERADA DE ALTERNATIVAS PARA EL CRITERIO {criterio}")
    print(matriz_div)

    pesos_alternativas = np.mean(matriz_div, axis=1)
    print(f"PESOS DE ALTERNATIVAS PARA EL CRITERIO {criterio}")
    print(pesos_alternativas)

    return pesos_alternativas

import numpy as np

def AHP(usuario='root', carta='Desayuno', seccion='Cafes'):
    bd = DBController()
    bd.connect()

    criterios = [row[0] for row in bd.fetch_data("SELECT * FROM criterios")]

    ponderacionCriterios = ponderarCriterios(bd)
    ponderacionAlternativasCriterios = []

    for criterio in criterios:
        print(f"\n\n\nCRITERIO: {criterio}")
        ponderacionAlternativasCriterios.append(ponderarAlternativas(bd, criterio, usuario, carta, seccion))

    print("\n\n\nPESOS DE LOS CRITERIOS:")
    print(ponderacionCriterios)

    print("\n\n\nPESOS DE LAS ALTERNATIVAS PARA CADA CRITERIO:")
    for ponderacion in ponderacionAlternativasCriterios:
        print(ponderacion)

    ponderacionAlternativasCriterios = np.array(ponderacionAlternativasCriterios).T
    puntuaciones_finales = np.dot(ponderacionAlternativasCriterios, ponderacionCriterios)

    print("\n\n\nPUNTUACIONES FINALES DE LAS ALTERNATIVAS:")
    for i, puntuacion in enumerate(puntuaciones_finales, start=1):
        print(f"Puntuación de la Alternativa {i}: {puntuacion}")

    platos_consult = bd.fetch_data(
        "SELECT * FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?",
        (carta, usuario, seccion)
    )
    print("\n\n\nPLATOS DISPONIBLES:")
    for plato in platos_consult:
        print(plato[0])

    plato_puntuacion = {plato[0]: puntuaciones_finales[i] for i, plato in enumerate(platos_consult)}

    print("\n\n\nPUNTUACIONES DE LOS PLATOS ORDENADAS:")
    for plato, puntuacion in sorted(plato_puntuacion.items(), key=lambda item: item[1], reverse=True):
        print(f"{plato}: {puntuacion}")

    print("\n\n\nPLATOS ORDENADOS POR PUNTUACIÓN:")
    platos = []
    for plato in sorted(plato_puntuacion, key=plato_puntuacion.get, reverse=True):
        platos.append(plato)
        print(plato)

    bd.disconnect()

    return platos
