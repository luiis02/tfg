
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
    try:
        if 'username' not in session:
            return redirect(url_for('user_routes.login'))

        estado = 200    
        db = DBController()
        db.connect()

        # Contar el número de cartas del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM cartas WHERE usuario = ?", (session['username'],))
        num_cartas = resultado[0][0] if resultado else 0

        # Contar el número de secciones del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM seccion WHERE usuario = ?", (session['username'],))
        num_secciones = resultado[0][0] if resultado else 0

        # Contar el número de platos del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM platos WHERE usuario = ?", (session['username'],))
        num_platos = resultado[0][0] if resultado else 0

        # Obtengo el nombre del establecimiento
        resultado = db.fetch_data("SELECT establecimiento FROM usuario WHERE usuario = ?", (session['username'],))
        establecimiento = resultado[0][0] if resultado else "No establecido"

        data = {"establecimiento": establecimiento, "num_cartas": num_cartas, "num_secciones": num_secciones, "num_platos": num_platos, "cartas": [], "secciones": [], "platos": []}
        
        if num_cartas > 0:
            obteninfo = db.fetch_data("SELECT nombre, indice, status FROM cartas WHERE usuario = ? ORDER BY indice", (session['username'],))
            for info in obteninfo:
                carta = {
                    "nombre": info[0],
                    "indice": info[1],
                    "status": info[2]
                }
                data["cartas"].append(carta)
        
        if num_secciones > 0:
            obteninfo = db.fetch_data("SELECT nombre, carta, indice, status FROM seccion WHERE usuario = ? ORDER BY indice", (session['username'],))
            for info in obteninfo:
                seccion = {
                    "nombre": info[0],
                    "carta": info[1],
                    "indice": info[2],
                    "status": info[3]
                }
                data["secciones"].append(seccion)
        
        if num_platos > 0:
            obteninfo = db.fetch_data("SELECT nombre, descripcion, precio, status, seccion, carta, indice FROM platos WHERE usuario = ? ORDER BY indice", (session['username'],))
            for info in obteninfo:
                plato = {
                    "nombre": info[0],
                    "descripcion": info[1],
                    "precio": info[2],
                    "status": info[3],
                    "seccion": info[4],
                    "carta": info[5],
                    "indice": info[6]
                }
                data["platos"].append(plato)
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
