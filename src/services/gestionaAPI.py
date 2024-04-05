
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
            'estado': resultado[7]
        }
        resultados_serializables.append(resultado_dict)
    
    return render_template('gestion.html', pedidos=resultados_serializables, username=session.get('username'), establecimiento=session.get('establecimiento'))



