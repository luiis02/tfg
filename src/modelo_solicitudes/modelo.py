
############################# IMPORTAR LIBRERÍAS ################################
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.layers import Input, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import EarlyStopping
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import joblib

############################# ABRIR CONJUNTO ################################

df = pd.read_excel('entrenamiento_2.xlsx')
df.drop(df.index[-1], inplace=True) # Eliminamos la última fila
df['categoria'] = df['CIBERATAQUE'].astype("category").cat.codes #Conversión de categoria a número

############################# CREAR CONJUNTOS ################################

df_train, df_test = train_test_split(df, test_size=0.3)
df_train['SOLICITUD'] = df_train['SOLICITUD'].astype(str) # Convertir a string
df_test['SOLICITUD'] = df_test['SOLICITUD'].astype(str) # Convertir a string

############################# TOKENIZAR FRASES ################################

tfidf = TfidfVectorizer()
Xtrain = tfidf.fit_transform(df_train['SOLICITUD'])
Xtest = tfidf.transform(df_test['SOLICITUD'])
Xtrain = Xtrain.toarray()
Xtest = Xtest.toarray()


############################# ENLAZAR CON CATEGORIAS ################################

Ytrain = df_train['categoria']
Ytest = df_test['categoria']

############################# OBTENCIÓN DE DIM. Y CLASES ################################

Dimensiones = Xtrain.shape[1]
Clases = df['categoria'].nunique()  # Usamos nunique para obtener el número de clases

############################# CREACIÓN DEL MODELO ################################

# Capa de entrada
i = Input(shape=(Dimensiones,))

# Capas ocultas
x = Dense(500, activation='relu')(i)  # Capa densa con 500 unidades y función de activación ReLU
y = Dense(500, activation='relu')(x)    
z = Dense(500, activation='relu')(y)

# Capa de salida
salida = Dense(Clases, activation='softmax')(z)  # Capa de salida con activación softmax para problemas de clasificación

# Definir el modelo
model = Model(i, salida)

model.summary() # Mostrar la arquitectura del modelo

############################# COMPILAR EL MODELO ################################

early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True) # evita el sobreajuste

model.compile(
    loss='sparse_categorical_crossentropy',
    optimizer='adam',
    metrics=['accuracy']
)

# Entrenar el modelo
r = model.fit(
    Xtrain, Ytrain,
    validation_data=(Xtest, Ytest),
    epochs=200,
    batch_size=1,
    callbacks=[early_stopping]
)

############################# GRÁFICAS DE ENTRENAMIENTO ##########################
plt.plot(r.history['loss'], label='train loss')
plt.plot(r.history['val_loss'], label='val loss')
plt.legend()
plt.savefig('curvas_perdida.png')

plt.plot(r.history['accuracy'], label='train acc')
plt.plot(r.history['val_accuracy'], label='val acc')
plt.legend()
plt.savefig('curvas_prediccion.png')

############################# GUARDAR EL MODELO ################################

#model.save("modelo_CIBERATACKS.keras")
model.save("modelo_CIBERATACKS.h5")

# Guardar el vectorizador TF-IDF
joblib.dump(tfidf, 'vector_CIBERATACKS.pkl')


############################# PREDICCIONES EN EL MODELO ################################

# while True:
#    nuevo_dato = input("Escriba la solicitud a predecir:\n")
#    nuevo_dato = str(nuevo_dato)
#    nuevo_dato_tfidf = tfidf.transform([nuevo_dato]) 
#    nuevo_dato_tfidf = nuevo_dato_tfidf.toarray()  
#    prediccion = model.predict(nuevo_dato_tfidf)
#    clase_predicha = np.argmax(prediccion)
#    if clase_predicha == 0:
#        clase_predicha = "Normal"
#    else:
#        clase_predicha = "Ataque"
#    print("La clase predicha para el nuevo dato es:", clase_predicha)