from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.models.forms.loginForm import LoginForm
from src.models.forms.confirmForm import ConfirmForm
##############################################################################################
##############################################################################################
##############################################################################################
import requests
import json
import random
import json
import requests
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from src.models.forms.confirmForm import ConfirmForm
platos_routes = Blueprint("platos_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@platos_routes.route('/platos/<nombre>', methods=['GET', 'POST'])
def platos(nombre):
    if 'username' not in session or 'carta' not in session:
        return redirect(url_for('user_routes.login'))
    session['seccion'] = nombre
    response = requests.get(url_for('platos_routes.getPlatos', _external=True), cookies={'auth': session.get('username'), 'carta': session.get('carta'), 'seccion': nombre})
    if response.status_code == 200:
        data = response.json()
        count_platos = data.get('num_platos', 0)
        platos_data = data.get('platos', [])
        platos = []
        for plato in platos_data:
            nombre_plato = plato['nombre']
            descripcion_plato = plato['descripcion']

            precio_plato = plato['precio']
            indice_plato = plato['indice']
            status_plato = "Inactivo" if plato['status'] == 0 else "Activo"
            platos.append((nombre_plato, descripcion_plato, precio_plato, indice_plato, status_plato))
        
        return render_template('platos.html', username=session.get('username'), count_platos=count_platos, secciones=platos, nombre=session.get('carta'), establecimiento=session.get('establecimiento'), seccion=nombre)

@platos_routes.route('/getPlatos', methods=['GET'])
def getPlatos():
    cookie_username = request.cookies.get('auth')
    cookie_carta = request.cookies.get('carta')
    cookie_seccion = request.cookies.get('seccion')

    if not cookie_username or not cookie_carta or not cookie_seccion:
        return redirect(url_for('user_routes.login'))
    
    bd = DBController()
    bd.connect()

    # Verificar si la existen platos en la carta
    existe = bd.fetch_data("SELECT COUNT(*) FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?", (cookie_carta, cookie_username, cookie_seccion))
    if existe[0][0] == 0: 
        plato ={"numero": "0", "nombre": "No hay cartas", "indice": "0", "status": "0"}

    data = {"carta": cookie_carta, "seccion": cookie_seccion, "num_platos": existe[0][0], "platos": []}

    data = {"num_platos": existe[0][0], "platos": []}
    if existe[0][0] > 0:
        platos = bd.fetch_data("SELECT * FROM platos WHERE carta = ? AND usuario = ? AND seccion = ?", (cookie_carta, cookie_username, cookie_seccion))
        for plato in platos:
            data["platos"].append({"nombre": plato[0], "precio": plato[7], "descripcion": plato[1], "status": plato[6], "indice": plato[5]})
    
    bd.disconnect()
    json_data = json.dumps(data)
    
    return json_data    

@platos_routes.route('/createPlato', methods=['POST'])
def create_plato():
    try:

        nombre_plato = request.form.get('nombre_seccion')
        descripcion_plato = request.form.get('descripción')
        precio = request.form.get('precio')
        indice_seccion = request.form.get('indice')
        status_seccion = request.form.get('estado')
        print("ENTRO AQUI")
        print(status_seccion)
        if status_seccion == 'on':
            status_seccion = True
        else:
            status_seccion = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO platos (nombre, descripcion, indice, status, usuario, carta, seccion, precio) VALUES (?,?,?,?,?,?,?,?)", (nombre_plato, descripcion_plato, indice_seccion, status_seccion, session["username"], session["carta"], session["seccion"],precio))
        bd.connection.commit()
        bd.disconnect()

        return jsonify({"message": "Datos recibidos correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@platos_routes.route('/removePlato', methods=['POST'])
def remove_Plato():
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
            
        data = request.get_json()  
        carta = data.get('cartaId') 
        bd = DBController()
        bd.connect()
        bd.execute_query("DELETE FROM platos WHERE nombre = ? AND usuario = ? AND seccion = ? AND carta = ?", (carta, session["username"], session["seccion"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta eliminada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

  
@platos_routes.route('/editPlato', methods=['POST'])
def edit_Plato():
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
        nombre_anterior = request.form.get('edita')
        nombre_carta = request.form.get('nombre_seccion_editar')
        descripcion_carta = request.form.get('descripcion_editar')
        precio_carta = request.form.get('precio_editar')
        indice_carta = request.form.get('indice_editar')
        status_carta = request.form.get('estado_editar')
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("UPDATE platos SET nombre = ?, descripcion = ?, precio = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ? AND carta = ? AND seccion = ?", (nombre_carta, descripcion_carta, precio_carta, indice_carta, status_carta, nombre_anterior, session["username"], session["carta"], session["seccion"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta editada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
