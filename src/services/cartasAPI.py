
from flask import jsonify, redirect, request, session, url_for
from flask import redirect, url_for
from flask import request
from src.models.carta import obtenCartas,eliminarCarta,crearCarta,editaCarta
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, redirect, url_for, session, request, jsonify
cartas_routes = Blueprint("cartas_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################


@cartas_routes.route('/getCartas', methods=['GET'])
def getCartas():
    cookie_value = request.cookies.get('auth')
    session['username'] = cookie_value
    session['rol'] = 'cliente'
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    
    # Llama a models
    status, data = obtenCartas(session['username'])
    if status == "OK":
        return data
    else: return "Error obteniendo cartas"
    

@cartas_routes.route('/removeCarta', methods=['POST'])
def remove_carta():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))      
    data = request.get_json()  
    carta = data.get('cartaId') 
    
    # Llama a models
    status = eliminarCarta(carta,session['username'],session['authapi'])
    if status == "OK":
        return jsonify({"message": "Carta eliminada correctamente"})
    else:
        return jsonify({"error": "Error eliminando carta"})
    

@cartas_routes.route('/createCarta', methods=['POST'])
def create_carta():
    nombre_carta = request.form.get('nombre_carta')
    nombre_carta = request.form.get('nombre_carta').strip()
    indice_carta = request.form.get('indice')
    status_carta = request.form.get('estado')


    # Llama a models
    status = crearCarta(nombre_carta, indice_carta, status_carta, session['username'], session['authapi'])
    if status == "OK":
        return jsonify({"message": "Carta creada correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de carta duplicado'}), 452
        else:
            return jsonify({"error": "Error creando carta"}), 453
        

        
    

@cartas_routes.route('/editCarta', methods=['POST'])
def edit_carta():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    
    nombre_anterior = request.form.get('edita')
    nombre_carta = request.form.get('nombre_carta_editar')
    indice_carta = request.form.get('indice_editar')
    status_carta = request.form.get('estado_editar')

    # Llama a models
    status= editaCarta(nombre_anterior, nombre_carta, indice_carta, status_carta, session['username'])
    if status == "OK":
        return jsonify({"message": "Carta editada correctamente"})
    else:
        if status == "Error, clave duplicada":
            return jsonify({'error': 'Nombre de carta duplicado'}), 452
        else:
            return jsonify({"error": "Error creando carta"}), 453