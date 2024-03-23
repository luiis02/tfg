from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request
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
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    session['carta'] = nombre

    response = requests.get(url_for('secciones_routes.getSeccion', _external=True), cookies={'auth': session.get('username'), 'carta': session.get('carta')})
    if response.status_code == 200:  # Verificar si la solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON en un diccionario
        
        count_secciones = data.get('num_secciones', 0)  # Obtener el número de cartas, si está disponible
        secciones_data = data.get('secciones', [])  # Obtener la lista de secciones, si está disponible
        print(count_secciones)
        
        secciones = []
        for seccion in secciones_data:
            nombre_carta = seccion[0]  # El nombre de la carta está en la primera posición
            print(nombre_carta)
            indice_carta = seccion[1]  # El índice de la carta está en la segunda posición
            print(indice_carta)
            status_carta = "Inactiva" if seccion[2] == 'Inactiva' else "Activa"  # El estado de la carta está en la tercera posición
            print(status_carta)
            secciones.append((nombre_carta, indice_carta, status_carta))

        return render_template('carta.html', username=session.get("username"), count_secciones=count_secciones, secciones=secciones)
    else:
        # Manejar el caso donde la solicitud no fue exitosa
        return "Error al obtener las cartas", 500  # Puedes personalizar el mensaje de error y el código de estado según sea necesario


@secciones_routes.route('/createSeccion', methods=['POST'])
def create_seccion():
    try:
        nombre_seccion = request.form.get('nombre_seccion')
        indice_seccion = request.form.get('indice')
        status_seccion = request.form.get('estado')
        if status_seccion == 'on':
            status_seccion = True
        else:
            status_seccion = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO seccion (nombre, indice, status, usuario, carta) VALUES (?,?,?,?,?)", (nombre_seccion, indice_seccion, status_seccion, session["username"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()

        return jsonify({"message": "Datos recibidos correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@secciones_routes.route('/removeSeccion', methods=['POST'])
def remove_Seccion():
    
    print("entra")
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
            
        data = request.get_json()  
        carta = data.get('cartaId') 
        bd = DBController()
        bd.connect()
        print(carta, session["username"], session["carta"])
        bd.execute_query("DELETE FROM seccion WHERE nombre = ? AND usuario = ? AND carta = ?", (carta, session["username"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta eliminada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@secciones_routes.route('/editSeccion', methods=['POST'])
def edit_Seccion():
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
        nombre_anterior = request.form.get('edita')
        nombre_carta = request.form.get('nombre_seccion_editar')
        indice_carta = request.form.get('indice_editar')
        status_carta = request.form.get('estado_editar')
        print(nombre_anterior, nombre_carta, indice_carta, status_carta)
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("UPDATE seccion SET nombre = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ? AND carta = ?", (nombre_carta, indice_carta, status_carta, nombre_anterior, session["username"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta editada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@secciones_routes.route('/getSeccion', methods=['GET'])
def getSeccion():
    
    cookie_value = request.cookies.get('auth')
    cookie_value2 = request.cookies.get('carta')
    session['username'] = cookie_value
    session['carta'] = cookie_value2
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    
    nombre = session['carta']

    bd = DBController()
    bd.connect()

    existe = bd.fetch_data("SELECT COUNT(*) FROM seccion WHERE carta = ? AND usuario = ?", (nombre, session['username']))
    if existe[0][0] == 0:
        seccion ={"numero": "0", "nombre": "No hay cartas", "indice": "0", "status": "0"}

    data = {"num_secciones": existe[0][0], "secciones": []}
    if existe[0][0] > 0:
        secciones = bd.fetch_data("SELECT nombre, indice, status FROM seccion WHERE carta = ? AND usuario = ? ORDER BY indice", (nombre, session['username']))
        for seccion in secciones:
            nombre_seccion = seccion[0]
            indice_seccion = seccion[1]
            status_seccion = "Inactiva" if seccion[2] == 0 else "Activa"
            data['secciones'].append((nombre_seccion, indice_seccion, status_seccion))
        
    bd.disconnect()
    json_data = json.dumps(data)

    return json_data

