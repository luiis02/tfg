from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request
from src.models.secciones import obtenSecciones,editarSeccion,borrarSeccion,crearSeccion
##############################################################################################
##############################################################################################
##############################################################################################
import json
import requests
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
secciones_routes = Blueprint("secciones_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################



@secciones_routes.route('/carta/<nombre>', methods=['GET', 'POST'])
def seccion(nombre):
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    session['carta'] = nombre
    response = requests.get(url_for('secciones_routes.getSeccion', _external=True), cookies={'auth': session.get('username'), 'carta': session.get('carta')})
    if response.status_code == 200:  # Verificar si la solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON en un diccionario
        
        count_secciones = data.get('num_secciones', 0)  # Obtener el número de cartas, si está disponible
        secciones_data = data.get('secciones', [])  # Obtener la lista de secciones, si está disponible
        
        secciones = []
        for seccion in secciones_data:
            nombre_carta = seccion[0]  # El nombre de la carta está en la primera posición
            indice_carta = seccion[1]  # El índice de la carta está en la segunda posición
            status_carta = "Inactiva" if seccion[2] == 'Inactiva' else "Activa"  # El estado de la carta está en la tercera posición
            secciones.append((nombre_carta, indice_carta, status_carta))

        return render_template('carta.html',establecimiento=session.get('establecimiento'), nombre=nombre, count_secciones=count_secciones, secciones=secciones)
    else:
        # Manejar el caso donde la solicitud no fue exitosa
        return "Error al obtener las cartas", 500  # Puedes personalizar el mensaje de error y el código de estado según sea necesario


@secciones_routes.route('/createSeccion', methods=['POST'])
def create_seccion():
    nombre_seccion = request.form.get('nombre_seccion').strip()
    indice_seccion = request.form.get('indice')
    status_seccion = request.form.get('estado')
    if status_seccion == 'on':
        status_seccion = True
    else:
        status_seccion = False
    status = crearSeccion(nombre_seccion,indice_seccion,status_seccion,session['username'],session['carta'])
    if status == "OK": return jsonify({"message": "Sección creada correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de sección duplicado'}), 452
        else:
            return jsonify({"error": "Error creando sección"}), 453

@secciones_routes.route('/removeSeccion', methods=['POST'])
def remove_Seccion():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
            
    data = request.get_json()  
    carta = data.get('cartaId') 
    
    # Llama a models
    status = borrarSeccion(carta,session['carta'], session['username'])
    if status == "OK":
        return jsonify({"message": "Carta eliminada correctamente"})
    else:
        return jsonify({"error": "Error eliminando carta"})
    
@secciones_routes.route('/editSeccion', methods=['POST'])
def edit_Seccion():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    nombre_anterior = request.form.get('edita')
    nombre_carta = request.form.get('nombre_seccion_editar')
    indice_carta = request.form.get('indice_editar')
    status_carta = request.form.get('estado_editar')
    if status_carta == 'on':
        status_carta = True
    else:
        status_carta = False
    
    # Llama a models
    status = editarSeccion(nombre_carta, session['username'], nombre_anterior, indice_carta, status_carta, session['carta'])
    if status == "OK":
        return jsonify({"message": "Carta editada correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de sección duplicado'}), 452
        else:
            return jsonify({"error": "Error creando sección"}), 453


@secciones_routes.route('/getSeccion', methods=['GET'])
def getSeccion():
    cookie_value = request.cookies.get('auth')
    cookie_value2 = request.cookies.get('carta')
    session['username'] = cookie_value
    session['carta'] = cookie_value2
    if 'username' not in session :
        return redirect(url_for('user_routes.login'))
    nombre = session['carta']
    # Llama a models
    status, data = obtenSecciones(nombre, session['username'])
    if status == "OK":
        return data
    else: return "Error obteniendo secciones"


