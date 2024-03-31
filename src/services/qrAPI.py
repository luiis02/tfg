from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from io import BytesIO

from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.models.forms.loginForm import LoginForm
from src.models.forms.confirmForm import ConfirmForm
##############################################################################################
##############################################################################################
##############################################################################################
import qrcode
import base64
import requests
import json
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from src.models.forms.confirmForm import ConfirmForm
qr_routes = Blueprint("qr_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@qr_routes.route('/mesa', methods=['GET', 'POST'])
def mesa():
    response = requests.get(url_for('qr_routes.getMesa', _external=True), cookies={'auth': session.get('username')})
    if response.status_code == 200:
        data = response.json()
        return render_template('mesa.html', mesas=data["mesas"],establecimiento=session.get('establecimiento'))
    else:
        return "Error al obtener datos de las mesas"
    
    
@qr_routes.route('/createMesa', methods=['POST'])
def CreateQR(id_establecimiento, crear):
    cookie_username = request.cookies.get('auth')
    cookie_crear = request.cookies.get('crear')

    if not cookie_username or not cookie_crear:
        return redirect(url_for('user_routes.login'))
    bd = DBController()
    bd.connect()
    existe = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
    recover = bd.fetch_data("SELECT establecimiento FROM usuario WHERE id = ?;", (id_establecimiento,))
    print(existe[0][0])
    print(recover[0][0])

    for i in range(crear):
        newMesa = existe[0][0] + i + 1
        qr_code = f"https://127.0.0.1/carta/{recover[0][0]}/{newMesa}"
        img = qrcode.make(qr_code)
        img_bytes = BytesIO()
        img.save(img_bytes)
        img_bytes = img_bytes.getvalue()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        bd.execute_query("INSERT INTO mesas (id_establecimiento,numero_mesa,img_qr) VALUES (?,?,?);", (id_establecimiento, newMesa, img_base64))


@qr_routes.route('/getMesa', methods=['GET', 'POST'])
def getMesa():
    cookie_username = request.cookies.get('auth')
    if not cookie_username:
        return redirect(url_for('user_routes.login'))
    
    bd = DBController()
    bd.connect()
    id = bd.fetch_data("SELECT id FROM usuario WHERE usuario = ?;", (cookie_username,))
    id_establecimiento = id[0][0]
    num_mesas = bd.fetch_data("SELECT COUNT(*) FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
    data = {"num_mesas": num_mesas, "mesas":[]}
    qr = bd.fetch_data("SELECT img_qr, numero_mesa FROM mesas WHERE id_establecimiento = ?;", (id_establecimiento,))
    for i in qr:
        data["mesas"].append({"numero": i[1], "qr": i[0]})  
    bd.disconnect()
    json_data = json.dumps(data)
    print(num_mesas)
    return json_data    


def deco(img_base64):
    img_bytes = base64.b64decode(img_base64)

    # Guardar los bytes decodificados en un archivo
    nombre_archivo = "imagen_decodificada.jpg"  # Puedes cambiar el nombre y la extensión del archivo según tu necesidad
    with open(nombre_archivo, "wb") as archivo:
        archivo.write(img_bytes)

    print("La imagen ha sido decodificada y guardada correctamente.")


