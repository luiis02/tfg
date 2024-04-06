
from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request
from src.models.carta import obtenCartas,eliminarCarta,crearCarta,editaCarta
from datetime import datetime
##############################################################################################
##############################################################################################
##############################################################################################
import json
import requests
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, redirect, url_for, session, request, jsonify
gestion_routes = Blueprint("gestion_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@gestion_routes.route('/gestion', methods=['GET', 'POST'])
def Gestion():
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    
    if request.method == 'POST':
        data = request.get_json()
        estado = data.get('estado')
        bd = DBController()
        bd.connect()
        if estado == 'fin':   
            result = bd.fetch_data("SELECT * FROM pedidos_activos WHERE id = ?", (data.get('id'),))
            bd.execute_query("DELETE FROM pedidos_activos WHERE id = ?", (data.get('id'),))
            count = bd.fetch_data("SELECT COUNT(*) FROM pedidos_historicos")  # Obtener el conteo directamente
            fecha_cierre_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            bd.execute_query("INSERT INTO pedidos_historicos (id, usuario, mesa, plato, cantidad, precio, fecha, fecha_cierre) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                (count[0][0] + 1, result[0][1], result[0][2], result[0][3], result[0][4], result[0][5], result[0][6], fecha_cierre_actual))
        else:
            bd.execute_query("DELETE FROM pedidos_activos WHERE id = ?", (data.get('id'),))
        bd.disconnect()




    bd = DBController()
    bd.connect()
    resultados = bd.fetch_data("SELECT * FROM pedidos_activos WHERE usuario = ?", (session.get('username'),))
    bd.disconnect()
    
    resultados_serializables = []
    for resultado in resultados:
        resultado_dict = {
            'id': resultado[0],
            'usuario': resultado[1],
            'mesa': resultado[2],
            'plato': resultado[3],
            'cantidad': resultado[4],
            'precio': resultado[5],
            'fecha': resultado[6],
            'estado': resultado[7],
            'categoria': resultado[8]
        }
        resultados_serializables.append(resultado_dict)

    
    bd.connect()
    categorias = bd.fetch_data("SELECT nombre FROM seccion WHERE usuario = ?", (session.get('username'),))
    bd.disconnect()
    categorias_carta = []
    for categoria in categorias:
        categorias_carta.append(categoria[0])
    
    return render_template('gestion.html', pedidos=resultados_serializables, username=session.get('username'), establecimiento=session.get('establecimiento'), categorias=categorias_carta)



