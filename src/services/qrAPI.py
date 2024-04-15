from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from io import BytesIO
from src.database.dbcontroller import DBController
from src.models.qr import createMesa, obtenerMesa, eliminaMesa
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
    auth_crear_mesa=0
    if not session.get('username') or not session.get('rol') == 'admin':
        auth_crear_mesa=1
        return redirect(url_for('user_routes.login'))
    response = requests.get(url_for('qr_routes.getMesa', _external=True), cookies={'auth': session.get('username')})
    if response.status_code == 200:
        data = response.json()
        return render_template('mesa.html', mesas=data["mesas"],establecimiento=session.get('establecimiento'))
    else:
        return "Error al obtener datos de las mesas"
    
    
@qr_routes.route('/createMesa', methods=['POST'])
def CreateQR():
    data = request.get_json()
    crear = data.get("numero")
    if not session["username"] or not crear or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    
    #Llamar a la funcion de models
    result = createMesa(session["username"], crear, session["authapi"] )
    if(result =="OK"): return jsonify({"message": "Datos recibidos correctamente"})
    else : return jsonify({"message": "Error al crear mesa"})

@qr_routes.route('/getMesa', methods=['GET', 'POST'])
def getMesa():

    cookie_username = request.cookies.get('auth')
    
    if not cookie_username:
        return redirect(url_for('user_routes.login'))
    
    #Llamar a la funcion de models
    status, json_data= obtenerMesa(cookie_username)
    print(status)
    if status == "OK": return json_data
    else: return jsonify({"message": "Error al obtener datos de las mesas"})


def deco(img_base64):
    img_bytes = base64.b64decode(img_base64)

    # Guardar los bytes decodificados en un archivo
    nombre_archivo = "imagen_decodificada.jpg"  # Puedes cambiar el nombre y la extensión del archivo según tu necesidad
    with open(nombre_archivo, "wb") as archivo:
        archivo.write(img_bytes)



@qr_routes.route('/deleteMesa', methods=['GET', 'POST'])
def deleteMesa():
    data = request.get_json()
    numero = data.get("numero")
    if not session["username"] or not numero or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    
    status = eliminaMesa(session["username"], numero, session["authapi"])
    if status == "OK": return jsonify({"message": "Datos recibidos correctamente"})
    else: return jsonify({"message": "Error al eliminar mesa"})

