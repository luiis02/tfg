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

def obtenCartas(usuario):    
    try:
        estado = 200    
        db = DBController()
        db.connect()
        # Contar el número de cartas del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM cartas WHERE usuario = %s", (usuario,))
        num_cartas = resultado[0][0] if resultado else 0

        # Contar el número de secciones del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM seccion WHERE usuario = %s", (usuario,))
        num_secciones = resultado[0][0] if resultado else 0

        # Contar el número de platos del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM platos WHERE usuario = %s", (usuario,))
        num_platos = resultado[0][0] if resultado else 0

        # Obtengo el nombre del establecimiento
        resultado = db.fetch_data("SELECT establecimiento FROM usuario WHERE usuario = %s", (usuario,))
        establecimiento = resultado[0][0] if resultado else "No establecido"

        data = {"establecimiento": establecimiento, "num_cartas": num_cartas, "num_secciones": num_secciones, "num_platos": num_platos, "cartas": [], "secciones": [], "platos": []}
        
        if num_cartas > 0:
            obteninfo = db.fetch_data("SELECT nombre, indice, status FROM cartas WHERE usuario = %s ORDER BY indice", (usuario,))
            for info in obteninfo:
                carta = {
                    "nombre": info[0],
                    "indice": info[1],
                    "status": info[2]
                }
                data["cartas"].append(carta)
        
        if num_secciones > 0:
            obteninfo = db.fetch_data("SELECT nombre, carta, indice, status FROM seccion WHERE usuario = %s ORDER BY indice", (usuario,))
            for info in obteninfo:
                seccion = {
                    "nombre": info[0],
                    "carta": info[1],
                    "indice": info[2],
                    "status": info[3]
                }
                data["secciones"].append(seccion)
        
        if num_platos > 0:
            obteninfo = db.fetch_data("SELECT nombre, descripcion, precio, status, seccion, carta, indice FROM platos WHERE usuario = %s ORDER BY indice", (usuario,))
            for info in obteninfo:
                plato = {
                    "nombre": info[0],
                    "descripcion": info[1],
                    "precio": info[2],
                    "status": info[3],
                    "seccion": info[4],
                    "carta": info[5],
                    "indice": info[6]
                }
                data["platos"].append(plato)
        db.disconnect()
        json_data = json.dumps(data)
        return "OK", json_data
    
    except Exception as e:
        return "NO"
    
def eliminarCarta(carta, usuario, key):  
    
    try:
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"
        bd.execute_query("DELETE FROM cartas WHERE nombre = %s AND usuario = %s", (carta,usuario))
        bd.execute_query("DELETE FROM seccion WHERE carta = %s AND usuario = %s", (carta,usuario))
        bd.execute_query("DELETE FROM platos WHERE carta = %s AND usuario = %s", (carta,usuario))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return "NO"

def crearCarta(nombre_carta, indice_carta, status_carta, usuario, key):
    try:
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"
        existe = bd.fetch_data("SELECT COUNT(*) FROM cartas WHERE nombre = %s AND usuario = %s", (nombre_carta, usuario))
        if existe[0][0] > 0: return "Error, clave duplicada"

        if indice_carta == "": indice_carta = 0
        if status_carta == "": status_carta = None


        bd.execute_query("INSERT INTO cartas (nombre, indice, status, usuario) VALUES (%s,%s,%s,%s)", (nombre_carta, indice_carta, status_carta, usuario))
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return str(e)

def editaCarta(nombre_anterior, nombre_carta, indice_carta, status_carta, usuario):
    try:
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()

        if indice_carta == "": indice_carta = 0
        if status_carta == "": status_carta = None
        result= bd.execute_query("UPDATE cartas SET nombre = %s, indice = %s, status = %s WHERE nombre = %s AND usuario = %s", (nombre_carta, indice_carta, status_carta, nombre_anterior, usuario))
        if result == 0: return "Error, clave duplicada"
        result = bd.execute_query("UPDATE seccion SET carta = %s WHERE carta = %s", (nombre_carta, nombre_anterior))
        if result == 0: return "Error, clave duplicada"
        
        bd.connection.commit()
        bd.disconnect()
        return "OK"
    except Exception as e: return "NO"