import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

############################# CARGAR MODELO Y VECTORIZADOR ##########################

# Cargar el modelo previamente guardado
#model = load_model('modelo_CIBERATACKS.h5')
model = load_model('src/modelo_solicitudes/modelo_CIBERATACKS.h5')
# Cargar el vectorizador TF-IDF previamente guardado
tfidf = joblib.load('src/modelo_solicitudes/vector_CIBERATACKS.pkl')

############################# FUNCION DE CLASIFICACION #############################

def clasificar_frase(frase):
    frase_tfidf = tfidf.transform([frase])
    frase_tfidf = frase_tfidf.toarray()
    prediccion = model.predict(frase_tfidf)
    clase_predicha = np.argmax(prediccion)
    if clase_predicha == 0:
        return "Normal"
    else:
        return "Ataque"

############################# EJEMPLO DE USO #############################

if __name__ == "__main__":
    nueva_frase = input("Escriba la solicitud a predecir:\n")
    resultado = clasificar_frase(nueva_frase)
    print("La clase predicha para el nuevo dato es:", resultado)
