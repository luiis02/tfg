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

def obtenSecciones(nombre, usuario):
    try:
        bd = DBController()
        bd.connect()

        # Verificar si la carta existe
        existe = bd.fetch_data("SELECT COUNT(*) FROM cartas WHERE nombre = ? AND usuario = ?", (nombre, usuario))
        if existe[0][0] == 0: return "NO",json({"error": "La carta no existe"})

        # Verificar si existen secciones en esa carta
        existe = bd.fetch_data("SELECT COUNT(*) FROM seccion WHERE carta = ? AND usuario = ?", (nombre, usuario))
        num_secciones = existe[0][0]
        
        # Verificar si existen platos para esa seccion
        existe = bd.fetch_data("SELECT COUNT(*) FROM seccion WHERE carta = ? AND usuario = ?", (nombre, usuario))
        num_platos = existe[0][0]
        
        data = {"carta": nombre, "num_secciones": num_secciones, "num_platos": num_platos,"secciones": [], "platos":[]}

        if num_secciones > 0:
            secciones = bd.fetch_data("SELECT nombre, indice, status FROM seccion WHERE carta = ? AND usuario = ? ORDER BY indice", (nombre, usuario))
            for seccion in secciones:
                nombre_seccion = seccion[0]
                indice_seccion = seccion[1]
                status_seccion = "Inactiva" if seccion[2] == 0 else "Activa"
                data['secciones'].append((nombre_seccion, indice_seccion, status_seccion))

        if num_platos > 0:
            platos = bd.fetch_data("SELECT nombre, descripcion, precio, status, seccion, carta, indice FROM platos WHERE carta = ? AND usuario = ? ORDER BY indice", (nombre, usuario))
            for plato in platos:
                nombre_plato = plato[0]
                descripcion_plato = plato[1]
                precio_plato = plato[2]
                status_plato = "Inactivo" if plato[3] == 0 else "Activo"
                seccion_plato = plato[4]
                carta_plato = plato[5]
                indice_plato = plato[6]
                data['platos'].append((nombre_plato, descripcion_plato, precio_plato, status_plato, seccion_plato, carta_plato, indice_plato))

        bd.disconnect()
        json_data = json.dumps(data)
        return "OK",json_data
    except Exception as e:
        return e

def editarSeccion(nombre, usuario, nombre_anterior, indice, status, carta):
    try:
        bd = DBController()
        bd.connect()
        result = bd.execute_query("UPDATE seccion SET nombre = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ? AND carta = ?", (nombre, indice, status, nombre_anterior, usuario, carta))
        if result == 0: return "Error, clave duplicada"
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e:
        return str(e)
    
def borrarSeccion(nombre, carta, usuario):
    try:
        bd = DBController()
        bd.connect()
        bd.execute_query("DELETE FROM seccion WHERE nombre = ? AND usuario = ? AND carta = ?", (nombre, usuario, carta))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e:
        return e
    
def crearSeccion(nombre_seccion, indice_seccion, status_seccion, usuario, carta):
    try:
        bd = DBController()
        bd.connect()
        existe = bd.fetch_data("SELECT COUNT(*) FROM seccion WHERE nombre = ? AND usuario = ? AND carta = ?", (nombre_seccion, usuario, carta))
        if existe[0][0] > 0: return "Error, clave duplicada"
        bd.execute_query("INSERT INTO seccion (nombre, indice, status, usuario, carta) VALUES (?,?,?,?,?)", (nombre_seccion, indice_seccion, status_seccion, usuario, carta))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: 
        return str(e)