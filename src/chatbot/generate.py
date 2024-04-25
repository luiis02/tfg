#from src.database.dbcontroller import DBController
from dbcontroller import DBController
import json

def generaJSON():
    # Crear un diccionario que represente el JSON inicial
    intentos = {
        "intents": []
    }

    bd = DBController()
    bd.connect()
    intents = bd.fetch_data("SELECT DISTINCT tag FROM intents", )
    for intent in intents:
        intentos["intents"].append({"tag": intent[0], "patterns": [], "responses": []})

    texto = bd.fetch_data("SELECT tag, Tipo, Texto FROM intents where indice_apoyo > 1", )
    for res in texto:
        for intent in intentos["intents"]:
            if intent["tag"] == res[0]:
                if res[1] == 0: intent["patterns"].append(res[2])
                else: intent["responses"].append(res[2])


    return intentos