import random
from src.database.dbcontroller import DBController
from datetime import timedelta

# Función que obtiene los platos de una carta
def obtenerAlternativas(usuario, carta, seccion):
    alternativas = []
    bd = DBController()
    bd.connect()
    result = bd.fetch_data("SELECT id, nombre FROM platos WHERE usuario = %s AND carta = %s AND seccion =%s AND status = 1", (usuario, carta, seccion, ))
    bd.disconnect()
    for i in range(len(result)):
        alternativas.append(result[i][1])
    return alternativas

# Función que obtiene los parametros a comparar
def obtenerTitulos():
    titulos = []
    bd = DBController()
    bd.connect()
    result = bd.fetch_data("SELECT nombre FROM parametros")
    bd.disconnect()
    for i in range(len(result)):
        titulos.append(result[i][0])
    return titulos

# Función que genera una matriz de tamaño tam_titulos x tam_alternativas
def generaMatriz(tam_titulos=0, tam_alternativas=0):
    if(tam_titulos == 0):
        tam_titulos = tam_alternativas
    elif(tam_alternativas == 0):
        tam_alternativas = tam_titulos

    filas = tam_alternativas + 2
    columnas = tam_titulos + 2
    matriz = [[" " for _ in range(columnas)] for _ in range(filas)]
    return matriz

# Función que imprime una matriz
def imprimeMatriz(matriz):
    for fila in matriz:
        for elemento in fila:
            print(str(elemento).center(20), end=' ')
        print()  


def rellenaPesos(matriz, titulos):
    print(" & GENERANDO MATRIZ DE PESOS ")
    matriz[0][0] = ' '
    matriz[len(titulos)+1][0]= "Total"
    for i in range(len(titulos)):
        matriz[i+1][0] = titulos[i]
        matriz[0][i+1] = titulos[i]
        matriz[i+1][i+1] = 1
    for i in range(1, len(titulos)+1):
        for j in range(i+1, len(titulos)+1):
            matriz[i][j] = calculapeso(matriz[i][0], matriz[0][j])
            matriz[j][i] = 1 / matriz[i][j]
    for i in range(1, len(titulos)+1):
        suma = 0
        for j in range(1, len(titulos)+1):
            suma += matriz[j][i]
        matriz[len(titulos)+1][i] = suma
    return matriz

def matrizNormalizadaPesos(matriz, titulos):
    print(" & NORMALIZANDO MATRIZ DE PESOS ")
    matriz[0][len(titulos)+1] = "Ponderación"
    for i in range(1, len(titulos)+1):
        for j in range(1, len(titulos)+1):
            matriz[i][j] = matriz[i][j] / matriz[len(titulos)+1][j]
    
    vector=[]
    for i in range(1, len(titulos)+1):
        suma = 0
        for j in range(1, len(titulos)+1):
            suma += matriz[i][j]
        vector.append(suma/len(titulos))
        matriz[i][len(titulos)+1] = suma / len(titulos)
    return matriz,vector

def calculapeso(maxi,mini):
    if maxi == mini:
        return 1
    else:
        bd = DBController()
        bd.connect()
        result = bd.fetch_data("SELECT COUNT(*) FROM relacionesParametros WHERE parametro1 = %s AND parametro2= %s", (maxi, mini,))
        if result[0][0] > 0:            
            result = bd.fetch_data("SELECT valor FROM relacionesParametros WHERE parametro1 = %s AND parametro2= %s", (maxi, mini,))
            bd.disconnect()
            return result[0][0]
        else:
            result = bd.fetch_data("SELECT valor FROM relacionesParametros WHERE parametro1 = %s AND parametro2= %s", (mini, maxi,))
            result = 1 / result[0][0]
            bd.disconnect()
            return result
    
def generarPesos(titulos):
    matriz = generaMatriz(len(titulos), len(titulos))
    matriz = rellenaPesos(matriz, titulos)
    imprimeMatriz(matriz)
    matriz,vector = matrizNormalizadaPesos(matriz, titulos)
    imprimeMatriz(matriz)
    return matriz, vector

def calculaalternativa(maxi,mini, titulo, usuario):
    if maxi == mini:
        return 1
    if titulo == "tiempo":
        return objetivo_tiempo(usuario, maxi, mini)
    bd = DBController()
    bd.connect()
    maxi = bd.fetch_data("SELECT id FROM platos WHERE nombre = %s AND usuario = %s", (maxi, usuario,))
    maxi = maxi[0][0]
    mini = bd.fetch_data("SELECT id FROM platos WHERE nombre = %s AND usuario = %s", (mini, usuario,))
    mini = mini[0][0]
    result = bd.fetch_data("SELECT COUNT(*) FROM relacionesPlatos WHERE id_plato1 = %s AND id_plato2= %s AND parametro = %s", (maxi, mini, titulo,))
    if result[0][0] > 0:
        result = bd.fetch_data("SELECT valor FROM relacionesPlatos WHERE id_plato1 = %s AND id_plato2= %s AND parametro = %s", (maxi, mini, titulo,))
        bd.disconnect()
        return result[0][0]
    else:
        result = bd.fetch_data("SELECT COUNT(*) FROM relacionesPlatos WHERE id_plato1 = %s AND id_plato2= %s AND parametro = %s", (mini, maxi, titulo,))
        if result[0][0] > 0:
            result = bd.fetch_data("SELECT valor FROM relacionesPlatos WHERE id_plato1 = %s AND id_plato2= %s AND parametro = %s", (mini, maxi, titulo,))
            bd.disconnect()
            result = 1 / result[0][0]
        else: 
            result = 1
            return result
    
def rellenaAlternativas(matriz, alternativas, titulo, usuario):
    print(" & GENERANDO MATRIZ DE ALTERNATIVAS PARA  " + titulo)
    matriz[0][0] = ' '
    matriz[len(alternativas)+1][0]= "Total"
    for i in range(len(alternativas)):
        matriz[i+1][0] = alternativas[i]
        matriz[0][i+1] = alternativas[i]
        matriz[i+1][i+1] = 1
    for i in range(1, len(alternativas)+1):
        for j in range(i+1, len(alternativas)+1):
            matriz[i][j] = calculaalternativa(matriz[i][0], matriz[0][j], titulo, usuario)
            matriz[j][i] = 1 / matriz[i][j]
    
    vector=[]
    for i in range(1, len(alternativas)+1):
        suma = 0
        for j in range(1, len(alternativas)+1):
            suma += matriz[j][i]
        matriz[len(alternativas)+1][i] = suma
    return matriz

def matrizNormalizadaAlternativas(matriz, alternativas, titulo):
    print(" & NORMALIZANDO MATRIZ DE ALTERNATIVAS PARA  " + titulo)
    matriz[0][len(alternativas)+1] = "Promedio"
    for i in range(1, len(alternativas)+1):
        for j in range(1, len(alternativas)+1):
            matriz[i][j] = matriz[i][j] / matriz[len(alternativas)+1][j]
    
    vector=[]
    for i in range(1, len(alternativas)+1):
        suma = 0
        for j in range(1, len(alternativas)+1):
            suma += matriz[i][j]
        vector.append(suma/len(alternativas))
        matriz[i][len(alternativas)+1] = suma / len(alternativas)
    return matriz,vector

def generaCriterios(alternativas, titulos, usuario):
    matriz_vectores = generaMatriz(len(alternativas), len(titulos))
    for i in range(len(titulos)):
        matriz = generaMatriz(len(alternativas), len(alternativas))
        matriz = rellenaAlternativas(matriz, alternativas, titulos[i], usuario)
        imprimeMatriz(matriz)
        matriz,vector = matrizNormalizadaAlternativas(matriz, alternativas, titulos[i])
        imprimeMatriz(matriz)

        for j in range(len(vector)):
            matriz_vectores[i][j]=vector[j]
    
    return matriz, matriz_vectores

def matriz_final(usuario,carta, seccion):
    alternativas = obtenerAlternativas(usuario, carta, seccion)
    titulos = obtenerTitulos()
    matriz_fin = generaMatriz(len(titulos),len(alternativas))
    matriz_ponderacion, vector = generarPesos(titulos)
    matriz,matriz_v = generaCriterios(alternativas, titulos, usuario)
    for i in range(len(titulos)):
        matriz_fin[0][i+1] = titulos[i]
        if (i == len(titulos)-1):
            matriz_fin[0][i+2] = "Predicción"
    for i in range(len(alternativas)):
        matriz_fin[i+1][0] = alternativas[i]
        if (i == len(alternativas)-1):
            matriz_fin[i+2][0] = "Ponderación"
    for i in range(len(titulos)):
        for j in range(len(alternativas)):
            matriz_fin[j+1][i+1] = matriz_v[i][j]
    for i in range(len(titulos)):
        matriz_fin[len(alternativas)+1][i+1] = matriz_ponderacion[i+1][len(titulos)+1]
    
    for i in range(len(alternativas)):
        for j in range(len(titulos)):
            if(matriz_fin[i+1][len(titulos)+1]==" "): 
                matriz_fin[i+1][len(titulos)+1] = 0
            
            matriz_fin[i+1][len(titulos)+1] += matriz_fin[len(alternativas)+1][j+1] * matriz_fin[i+1][j+1]
            
    print(" & GENERANDO MATRIZ FINAL")   
    
    imprimeMatriz(matriz_fin)

def objetivo_tiempo(usuario, plato1, plato2):
    bd = DBController()
    bd.connect()
    total_tiempo_1 = 0
    tiempos_pedido1 = bd.fetch_data("SELECT fecha, fecha_cierre, cantidad FROM pedidos_historicos WHERE usuario = %s AND plato = %s", (usuario, plato1,))
    for i in range(len(tiempos_pedido1)):
        intervalo_tiempo  = tiempos_pedido1[i][1] - tiempos_pedido1[i][0]
        cantidad = tiempos_pedido1[i][2]
        total_tiempo_1 += (intervalo_tiempo.total_seconds() / 60)/ float(cantidad)
    try:        
        media_tiempo_1 = total_tiempo_1 / len(tiempos_pedido1)
    except:
        media_tiempo_1 = 0
    tiempos_pedido2 = bd.fetch_data("SELECT fecha, fecha_cierre,cantidad FROM pedidos_historicos WHERE usuario = %s AND plato = %s", (usuario, plato2,))
    total_tiempo_2 = 0
    for i in range(len(tiempos_pedido2)):
        intervalo_tiempo  = tiempos_pedido2[i][1] - tiempos_pedido2[i][0]
        cantidad = tiempos_pedido2[i][2]
        total_tiempo_2 += (intervalo_tiempo.total_seconds() / 60) / float(cantidad)
    try:
        media_tiempo_2 = total_tiempo_2 / len(tiempos_pedido2)
    except:
        media_tiempo_2 = 0
    media_general = media_tiempo_2-media_tiempo_1
    if media_general > -2 and media_general < 2:
        return 1
    elif media_general > 2 and media_general < 5:
        return 3
    elif media_general < -2 and media_general > -5:
        return 1/3
    elif media_general > 5 and media_general < 10:
        return 5
    elif media_general < -5 and media_general > -10:
        return 1/5
    elif media_general > 10 and media_general < 15:
        return 7
    elif media_general < -10 and media_general > -15:
        return 1/7
    elif media_general > 15:
        return 9
    elif media_general < -15:
        return 1/9

matriz_final("root","Desayunos","Cafes")
