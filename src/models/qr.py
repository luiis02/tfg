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
def createMesa(usuario, crear):
    try:
        bd = DBController()
        bd.connect()
        id_establecimiento = bd.fetch_data("SELECT id FROM usuario WHERE usuario = ?;", (usuario,))
        id_establecimiento = id_establecimiento[0][0]
        existe = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
        recover = bd.fetch_data("SELECT establecimiento FROM usuario WHERE id = ?;", (id_establecimiento,))
        for i in range(int(crear)):
            newMesa = existe[0][0] + i + 1
            formatrecover = recover[0][0].replace(" ", "_")
            qr_code = f"https://127.0.0.1/carta/{usuario}/{newMesa}"
            img = qrcode.make(qr_code)
            img_bytes = BytesIO()
            img.save(img_bytes)
            img_bytes = img_bytes.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            bd.execute_query("INSERT INTO mesas (id_establecimiento,numero_mesa,img_qr) VALUES (?,?,?);", (id_establecimiento, newMesa, img_base64))
        bd.disconnect()
        return "OK"
    except Exception as e: return e



def obtenerMesa(usuario):
    try:
        bd = DBController()
        bd.connect()
        id = bd.fetch_data("SELECT id FROM usuario WHERE usuario = ?;", (usuario,))
        id_establecimiento = id[0][0]
        num_mesas = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
        data = {"num_mesas": num_mesas, "mesas":[]}
        qr = bd.fetch_data("SELECT img_qr, numero_mesa FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
        for i in qr:
            data["mesas"].append({"numero": i[1], "qr": i[0]})  
        bd.disconnect()
        json_data = json.dumps(data)
        return "OK", json_data
    except Exception as e: return e

def eliminaMesa(usuario, numero):
    try:
        bd = DBController()
        bd.connect()
        id = bd.fetch_data("SELECT id FROM usuario WHERE usuario = ?;", (usuario,))
        id_establecimiento = id[0][0]
        bd.execute_query("DELETE FROM mesas WHERE id_establecimiento = ? AND numero_mesa = ?;", (id_establecimiento, numero))
        bd.disconnect()
        return "OK"
    except Exception as e: return e