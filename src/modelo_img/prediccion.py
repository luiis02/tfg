import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model
import joblib


def procesar_imagen(ruta_imagen, tamaño=(225, 225)):
    try:
        imagen_original = Image.open(ruta_imagen)
        imagen_redimensionada = imagen_original.resize(tamaño)
        imagen_redimensionada = imagen_redimensionada.convert('RGB')
        imagen_array = np.array(imagen_redimensionada)
        return imagen_array / 255.0  # Normalización de píxeles
    except Exception as e:
        print('Error procesando la imagen:', ruta_imagen, 'debido a:', e)
        return None

def predecir_imagen(modelo, ruta_imagen, encoder):
    # Procesar la imagen
    imagen_procesada = procesar_imagen(ruta_imagen)
    if imagen_procesada is None:
        return
    
    # Añadir dimensión para el batch size
    imagen_procesada = np.expand_dims(imagen_procesada, axis=0)
    
    # Realizar la predicción
    prediccion = modelo.predict(imagen_procesada)
    clase_predicha = np.argmax(prediccion, axis=1)
    etiqueta_predicha = encoder.inverse_transform(clase_predicha)
    
    print(f'La imagen {ruta_imagen} se predice como: {etiqueta_predicha[0]}')

# Cargar el modelo entrenado
modelo_guardado = 'model.h5'
model = load_model(modelo_guardado)

# Cargar etiqueta_encoder desde el archivo pickle
etiqueta_encoder = joblib.load('etiqueta_encoder.pkl')

# Predecir una imagen
ruta_imagen_prediccion = 'pruebas/burguer1.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/burguer2.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/pizza.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/pizza2.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/pizza3.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/pizza4.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/spaguettis.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/spaguettis2.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/tercio.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/tercio2.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/vino1.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/huevos_rotos1.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/habas1.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)

ruta_imagen_prediccion = 'pruebas/palmera1.jpeg'
predecir_imagen(model, ruta_imagen_prediccion, etiqueta_encoder)