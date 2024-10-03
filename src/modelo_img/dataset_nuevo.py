import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import numpy as np
import joblib
from PIL import Image
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential, save_model
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D, BatchNormalization, Activation
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping
from tensorflow.keras.regularizers import l2
from datetime import datetime

def cargar_datos(directorio):
    imagenes = []
    etiquetas = []
    for carpeta in os.listdir(directorio):
        for archivo in os.listdir(os.path.join(directorio, carpeta)):
            ruta_imagen = os.path.join(directorio, carpeta, archivo)
            imagenes.append(ruta_imagen)
            etiquetas.append(carpeta)
    return imagenes, etiquetas

def preprocesamiento(directorio='data'):
    imagenes, etiquetas = cargar_datos(directorio)
    etiqueta_encoder = LabelEncoder()
    etiquetas_codificadas = etiqueta_encoder.fit_transform(etiquetas)
    
    imagenes_procesadas = []
    etiquetas_filtradas = []
    
    for idx, ruta_imagen in enumerate(imagenes):
        imagen_procesada = procesar_imagen(ruta_imagen)
        if imagen_procesada is not None:
            imagenes_procesadas.append(imagen_procesada)
            etiquetas_filtradas.append(etiquetas_codificadas[idx])
    
    imagenes_procesadas = np.array(imagenes_procesadas)
    etiquetas_filtradas = np.array(etiquetas_filtradas)
    
    return imagenes_procesadas, etiquetas_filtradas, etiqueta_encoder

def procesar_imagen(ruta_imagen, tamaño=(225, 225)):
    try:
        imagen_original = Image.open(ruta_imagen)        
        imagen_redimensionada = imagen_original.resize(tamaño)        
        imagen_redimensionada = imagen_redimensionada.convert('RGB')        
        imagen_array = np.array(imagen_redimensionada)
        return imagen_array / 255.0  # Normalización de píxeles
    except Exception as e:
        os.remove(ruta_imagen)
        print('Imagen eliminada:', ruta_imagen, 'debido a:', e)
        return None

def crear_generadores(X_train, X_val, y_train, y_val, batch_size):
    train_datagen = ImageDataGenerator(
        rotation_range=30, 
        width_shift_range=0.2, 
        height_shift_range=0.2, 
        shear_range=0.2, 
        zoom_range=0.2, 
        horizontal_flip=True, 
        fill_mode='nearest'
    )
    train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
    
    val_datagen = ImageDataGenerator()
    val_generator = val_datagen.flow(X_val, y_val, batch_size=batch_size)
    
    return train_generator, val_generator

def crear_modelo(input_shape, num_clases):
    
    # Modelo base
    base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)
    model = Sequential()
    model.add(base_model)
    model.add(GlobalAveragePooling2D())
    
    # Primer bloque denso
    model.add(Dense(512, kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    # Segundo bloque denso
    model.add(Dense(256, kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    # Tercer bloque denso
    model.add(Dense(128, kernel_regularizer=l2(0.01)))
    model.add(BatchNormalization())
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    
    # Capa de salida
    model.add(Dense(num_clases, activation='softmax'))
    
    # Compilación del modelo
    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    
    return model

def main():
    # Obtener la hora actual para los nombres de archivo
    ahora = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Preprocesar datos
    X, y, etiqueta_encoder = preprocesamiento()

    # Dividir datos en entrenamiento y validación
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.3)

    # Crear generadores de datos aumentados
    batch_size = 8  # Puedes ajustar este valor
    train_generator, val_generator = crear_generadores(X_train, X_val, y_train, y_val, batch_size)

    # Crear y entrenar modelo
    n_epocas = 30  # Número alto de épocas
    input_shape = X_train[0].shape
    num_clases = len(np.unique(y_train))
    model = crear_modelo(input_shape, num_clases)
    
    # Ajustar steps_per_epoch y validation_steps
    #steps_per_epoch = len(X_train) // batch_size
    #validation_steps = len(X_val) // batch_size
    
    
    #model.fit(train_generator, steps_per_epoch=steps_per_epoch, validation_data=val_generator,validation_steps=validation_steps, epochs=n_epocas)

    model.fit(train_generator, validation_data=val_generator, epochs=n_epocas)


    # Guardar el modelo final
    modelo_guardado = f'model.h5'
    save_model(model, modelo_guardado)
    print(f'Modelo guardado como {modelo_guardado}')
    
    # Guardar etiquetas
    etiquetas_guardadas = f'etiqueta_encoder.pkl'
    joblib.dump(etiqueta_encoder, etiquetas_guardadas)
    print(f'Encoder de etiquetas guardado como {etiquetas_guardadas}')

if __name__ == "__main__":
    main()
