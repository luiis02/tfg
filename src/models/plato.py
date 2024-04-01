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
        existe = bd.fetch_data("SELECT COUNT(*) FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?", (carta, usuario, seccion))
        if existe[0][0] == 0: 
            plato ={"numero": "0", "nombre": "No hay cartas", "indice": "0", "status": "0"}

        data = {"carta": carta, "seccion": seccion, "num_platos": existe[0][0], "platos": []}

        data = {"num_platos": existe[0][0], "platos": []}
        if existe[0][0] > 0:
            platos = bd.fetch_data("SELECT * FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?", (carta, usuario, seccion))
            for plato in platos:
                data["platos"].append({"nombre": plato[0], "precio": plato[7], "descripcion": plato[1], "status": plato[6], "indice": plato[5]})
        
        bd.disconnect()
        json_data = json.dumps(data)
        return "OK", json_data
    except Exception as e: return e

def crearPlato(nombre, descripcion, precio, indice, status, usuario, carta, seccion):
    try:
        if status == 'on':
            status = True
        else:
            status = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO platos (nombre, descripcion, indice, status, usuario, carta, seccion, precio) VALUES (?,?,?,?,?,?,?,?)", (nombre, descripcion, indice, status, usuario, carta, seccion,precio))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e

def eliminarPlato(nombre, carta, usuario, seccion):
    try:
        bd = DBController()
        bd.connect()
        bd.execute_query("DELETE FROM platos WHERE nombre = ? AND usuario = ? AND seccion = ? AND carta = ?", (nombre, usuario, seccion, carta))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e

def editaPlato(nombre, descripcion, precio, indice, status, usuario, carta, seccion, nombre_anterior):
    try:
        if status == 'on':
            status = True
        else:
            status = False
        bd = DBController()
        bd.connect()
        bd.execute_query("UPDATE platos SET nombre = ?, descripcion = ?, precio = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ? AND carta = ? AND seccion = ?", (nombre, descripcion, precio, indice, status, nombre_anterior, usuario, carta, seccion))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return e