
from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request
##############################################################################################
##############################################################################################
##############################################################################################
import json
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
    print(session['username'])
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))

        estado = 200    
        db = DBController()
        db.connect()

        # Contar el número de cartas del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM cartas WHERE usuario = ?", (session['username'],))
        num_cartas = resultado[0][0] if resultado else 0

        data = {"num_cartas": num_cartas, "cartas": []}
        
        if num_cartas > 0:
            obteninfo = db.fetch_data("SELECT nombre, indice, status FROM cartas WHERE usuario = ? ORDER BY indice", (session['username'],))
            for info in obteninfo:
                carta = {
                    "numero": num_cartas,
                    "nombre": info[0],
                    "indice": info[1],
                    "status": info[2]
                }
                data["cartas"].append(carta)
        else:
            carta ={"numero": "0", "nombre": "No hay cartas", "indice": "0", "status": "0"}
        
        db.disconnect()
        json_data = json.dumps(data)
        return json_data
    
    except Exception as e:
        return jsonify({"error": "Ocurrió un error en la API"}), 500

@cartas_routes.route('/removeCarta', methods=['POST'])
def remove_carta():
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
        
        data = request.get_json()  
        carta = data.get('cartaId') 
        bd = DBController()
        bd.connect()
        bd.execute_query("DELETE FROM cartas WHERE nombre = ? AND usuario = ?", (carta,session["username"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta eliminada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

@cartas_routes.route('/createCarta', methods=['POST'])
def create_carta():
    try:
        nombre_carta = request.form.get('nombre_carta')
        indice_carta = request.form.get('indice')
        status_carta = request.form.get('estado')
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO cartas (nombre, indice, status, usuario) VALUES (?,?,?,?)", (nombre_carta, indice_carta, status_carta, session["username"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Datos recibidos correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@cartas_routes.route('/editCarta', methods=['POST'])
def edit_carta():
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))
        nombre_anterior = request.form.get('edita')
        nombre_carta = request.form.get('nombre_carta_editar')
        indice_carta = request.form.get('indice_editar')
        status_carta = request.form.get('estado_editar')
        print(nombre_anterior, nombre_carta, indice_carta, status_carta)
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("UPDATE cartas SET nombre = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ?", (nombre_carta, indice_carta, status_carta, nombre_anterior, session["username"]))
        bd.execute_query("UPDATE seccion SET carta = ? WHERE carta = ?", (nombre_carta, nombre_anterior))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta editada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
