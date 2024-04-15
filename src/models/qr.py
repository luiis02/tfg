from io import BytesIO
from src.database.dbcontroller import DBController
##############################################################################################
##############################################################################################
##############################################################################################
import qrcode
import base64
import json
##############################################################################################
##############################################################################################
##############################################################################################
def createMesa(usuario, crear, key):
    try:
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"
        id_establecimiento = bd.fetch_data("SELECT id FROM usuario WHERE usuario = %s;", (usuario,))
        id_establecimiento = id_establecimiento[0][0]
        existe = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = %s;", (id_establecimiento,))
        recover = bd.fetch_data("SELECT establecimiento FROM usuario WHERE id = %s;", (id_establecimiento,))
        for i in range(int(crear)):
            newMesa = existe[0][0] + i + 1
            formatrecover = recover[0][0].replace(" ", "_")
            qr_code = f"https://127.0.0.1/carta/{usuario}/{newMesa}"
            print(qr_code)
            img = qrcode.make(qr_code)
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes = img_bytes.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            bd.execute_query("INSERT INTO mesas (id_establecimiento,numero_mesa,img_qr) VALUES (%s,%s,%s);", (id_establecimiento, newMesa, img_base64))
        bd.disconnect()
        return "OK"
    except Exception as e: return e



def obtenerMesa(usuario):
    try:
        bd = DBController()
        bd.connect()

        id = bd.fetch_data("SELECT id FROM usuario WHERE usuario = %s;", (usuario,))
        id_establecimiento = id[0][0]
        num_mesas = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = %s;", (id_establecimiento,))
        data = {"num_mesas": num_mesas, "mesas":[]}
        qr = bd.fetch_data("SELECT img_qr, numero_mesa FROM mesas WHERE id_establecimiento = %s;", (id_establecimiento,))
        for i in qr:
            # Convert bytes to string
            qr_image = i[0].decode('utf-8') if i[0] is not None else None
            data["mesas"].append({"numero": i[1], "qr": qr_image})  
        bd.disconnect()
        return "OK", data
    except Exception as e:
        return "ERROR", str(e)

def eliminaMesa(usuario, numero,key):
    try:
        bd = DBController()
        bd.connect()
        auth = bd.fetch_data("SELECT COUNT(*) FROM usuario WHERE usuario = %s AND passwd = %s", (usuario, key))
        if auth[0][0] == 0: return "NO"
        id = bd.fetch_data("SELECT id FROM usuario WHERE usuario = %s;", (usuario,))
        id_establecimiento = id[0][0]
        bd.execute_query("DELETE FROM mesas WHERE id_establecimiento = %s AND numero_mesa = %s;", (id_establecimiento, numero))
        bd.disconnect()
        return "OK"
    except Exception as e: return e