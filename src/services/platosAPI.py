from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.models.forms.loginForm import LoginForm
from src.models.forms.confirmForm import ConfirmForm
from src.models.plato import obtenPlatos,crearPlato,eliminarPlato,editaPlato
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
    if 'username' not in session or 'carta' not in session or session['rol'] != 'admin':
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
    
    # Llama a models
    status, json_data= obtenPlatos(cookie_username,cookie_carta,cookie_seccion)
    if status=="OK": return json_data    
    else: return "Error obteniendo platos"

@platos_routes.route('/createPlato', methods=['POST'])
def create_plato():
    nombre_plato = request.form.get('nombre_seccion')
    nombre_plato = nombre_plato.strip()
    descripcion_plato = request.form.get('descripción')
    precio = request.form.get('precio')
    indice_seccion = request.form.get('indice')
    status_seccion = request.form.get('estado')

    # Llama a models
    status = crearPlato(nombre_plato, descripcion_plato, precio, indice_seccion, status_seccion, session.get('username'), session.get('carta'), session.get('seccion'), session.get('authapi'))
    if status=="OK": return jsonify({"message": "Plato creado correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de carta duplicado'}), 452
        else:
            return jsonify({"error": "Error creando carta"}), 453


@platos_routes.route('/removePlato', methods=['POST'])
def remove_Plato():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
            
    data = request.get_json()  
    nombre = data.get('cartaId') 

    status=eliminarPlato(nombre, session["carta"], session["username"], session["seccion"], session["authapi"])
    if status=="OK": return jsonify({"message": "Carta eliminada correctamente"})
    else: return "Error eliminando carta"
    

  
@platos_routes.route('/editPlato', methods=['POST'])
def edit_Plato():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    nombre_anterior = request.form.get('edita')
    nombre_carta = request.form.get('nombre_seccion_editar')
    descripcion_carta = request.form.get('descripcion_editar')
    precio_carta = request.form.get('precio_editar')
    indice_carta = request.form.get('indice_editar')
    status_carta = request.form.get('estado_editar')
    
    #----------------------------------------------Dentro de models
    status = editaPlato(nombre_carta, descripcion_carta, precio_carta, indice_carta, status_carta, session["username"], session["carta"], session["seccion"], nombre_anterior, session["authapi"])
    if status=="OK": return jsonify({"message": "Carta editada correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de carta duplicado'}), 452
        else:
            return jsonify({"error": "Error creando carta"}), 453