from io import BytesIO
from src.database.dbcontroller import DBController
##############################################################################################
##############################################################################################
##############################################################################################
import qrcode
import base64
import json
from src.database.dbcontroller import DBController
from src.database.dbcontroller import DBController
##############################################################################################
##############################################################################################
##############################################################################################
def obtenPlatos(usuario, carta, seccion):
    try:
        bd = DBController()
        bd.connect()
        

        # Verificar si la existen platos en la carta
        existe = bd.fetch_data("SELECT COUNT(*) FROM platos WHERE carta = %s AND usuario = %s AND seccion = %s", (carta, usuario, seccion))
        if existe[0][0] == 0: 
            plato ={"numero": "0", "nombre": "No hay cartas", "indice": "0", "status": "0"}

        data = {"carta": carta, "seccion": seccion, "num_platos": existe[0][0], "platos": []}

        data = {"num_platos": existe[0][0], "platos": []}
        if existe[0][0] > 0:
            platos = bd.fetch_data("SELECT nombre,precio,descripcion,status,indice FROM platos WHERE carta = %s AND usuario = %s AND seccion = %s", (carta, usuario, seccion))
            for plato in platos:
                data["platos"].append({"nombre": plato[0], "precio": plato[1], "descripcion": plato[2], "status": plato[3], "indice": plato[4]})
        
        bd.disconnect()
        json_data = json.dumps(data)
        return "OK", json_data
    except Exception as e: return e

def crearPlato(nombre, descripcion, precio, indice, status, usuario, carta, seccion,key):
    try:
        if status == 'on':
            status = True
        else:
            status = False
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"
        existe = bd.fetch_data("SELECT COUNT(*) FROM platos WHERE nombre = %s AND usuario = %s AND carta = %s AND seccion = %s", (nombre, usuario, carta, seccion))
        if existe[0][0] > 0: return "Error, clave duplicada"

        if descripcion == "": descripcion = None
        if precio == "": precio = 0
        if indice == "": indice = 0
        if status == "": status = 0
        bd.execute_query("INSERT INTO platos (nombre, descripcion, indice, status, usuario, carta, seccion, precio) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (nombre, descripcion, indice, status, usuario, carta, seccion,precio))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e

def eliminarPlato(nombre, carta, usuario, seccion, otro):
    try:
        bd = DBController()
        bd.connect()
        print(nombre, carta, usuario, seccion, otro)
        bd.execute_query("DELETE FROM platos WHERE nombre = %s AND usuario = %s AND seccion = %s AND carta = %s", (nombre, usuario, seccion, carta))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e

def editaPlato(nombre, descripcion, precio, indice, status, usuario, carta, seccion, nombre_anterior,key):
    try:
        if status == 'on':
            status = True
        else:
            status = False
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"

        if descripcion == "": descripcion = "'"
        if precio == "": precio = 0
        if indice == "": indice = 0
        if status == "": status = 0

        result = bd.execute_query("UPDATE platos SET nombre = %s, descripcion = %s, precio = %s, indice = %s, status = %s WHERE nombre = %s AND usuario = %s AND carta = %s AND seccion = %s", (nombre, descripcion, precio, indice, status, nombre_anterior, usuario, carta, seccion))
        if result == 0: return "Error, clave duplicada"
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e