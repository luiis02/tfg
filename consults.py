import random


alternativas = ["Cocacola", "Caña", "Fanta"]
titulos = ['Precio', 'Tiempo', 'Popularidad']

##################################################################################
def generaMatriz(tam_titulos):
    filas = columnas = tam_titulos +2 
    matriz = [[" " for _ in range(columnas)] for _ in range(filas)]
    return matriz

def generaMatrizNoCuadrada(tam_titulos, tam_posib):
    filas = tam_posib + 2
    columnas = tam_titulos +2 
    matriz = [[" " for _ in range(columnas)] for _ in range(filas)]
    return matriz
def imprimeMatriz(matriz):
    for fila in matriz:
        for elemento in fila:
            print(str(elemento).center(20), end=' ')
        print()  

##################################################################################
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
    aleatorio = random.randint(1, 9)
    inverso = 1 / aleatorio
    if random.choice([True, False]):
        return aleatorio
    else:
        return inverso

def generarPesos(titulos):
    matriz = generaMatriz(len(titulos))
    matriz = rellenaPesos(matriz, titulos)
    imprimeMatriz(matriz)
    matriz,vector = matrizNormalizadaPesos(matriz, titulos)
    imprimeMatriz(matriz)
    return matriz, vector
##################################################################################
def calculaalternativa(maxi,mini, titulo):
    aleatorio = random.randint(1, 9)
    inverso = 1 / aleatorio
    if random.choice([True, False]):
        return aleatorio
    else:
        return inverso

def rellenaAlternativas(matriz, alternativas, titulo):
    print(" & GENERANDO MATRIZ DE ALTERNATIVAS PARA  " + titulo)
    matriz[0][0] = ' '
    matriz[len(alternativas)+1][0]= "Total"
    for i in range(len(alternativas)):
        matriz[i+1][0] = alternativas[i]
        matriz[0][i+1] = alternativas[i]
        matriz[i+1][i+1] = 1
    for i in range(1, len(alternativas)+1):
        for j in range(i+1, len(alternativas)+1):
            matriz[i][j] = calculaalternativa(matriz[i][0], matriz[0][j], titulo)
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

def generaCriterios(alternativas, titulos):
    matriz_vectores = generaMatrizNoCuadrada(len(alternativas),len(titulos))
    for i in range(len(titulos)):
        matriz = generaMatriz(len(alternativas))
        matriz = rellenaAlternativas(matriz, alternativas, titulos[i])
        imprimeMatriz(matriz)
        matriz,vector = matrizNormalizadaAlternativas(matriz, alternativas, titulos[i])
        imprimeMatriz(matriz)

        for j in range(len(vector)):
            matriz_vectores[i][j]=vector[j]
    
    return matriz, matriz_vectores


##################################################################################
def matrizFinal(alternativas,titulos):
    
    matriz_peso,vector = generarPesos(titulos)

    matriz = generaMatriz(len(alternativas))
    for i in range(len(alternativas)):
        matriz[i+1][0] = alternativas[i]
        if (i == len(alternativas)-1):
            matriz[i+2][0] = "Ponderación"
            for j in range(len(vector)):
                matriz[i+2][j+1] = vector[j]
    for i in range(len(titulos)):
        matriz[0][i+1] = titulos[i]
        if (i == len(titulos)-1):
            matriz[0][i+2] = "Priorización"

    matriz_crit, matriz_vectores = generaCriterios(alternativas, titulos)
    
    for i in range(1, len(matriz)-1):
        for j in range(1, len(matriz[0])-1):
            if(matriz[i][j]==" "):
                matriz[i][j] = matriz_vectores[j-1][i-1]
    
    for i in range(1, len(matriz)-1):
        suma = 0
        for j in range(1, len(matriz[0])-1):
            suma += matriz[i][j]*matriz_peso[i][len(titulos)+1]
        matriz[i][len(matriz[0])-1] = suma

    print(" & GENERANDO MATRIZ FINAL ")
    imprimeMatriz(matriz)
    

matrizFinal(alternativas,titulos)