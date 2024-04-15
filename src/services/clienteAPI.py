
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
clientes_routes = Blueprint("clientes_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################

@clientes_routes.route('/carta/<nombre>/<mesa>', methods=['GET'])
def acorta_cartas_Url(nombre, mesa):
    nombre = nombre.replace("_", " ")
    session['username'] = nombre
    session['mesa'] = mesa
    session['rol'] = 'cliente'

    return redirect(url_for('clientes_routes.Carta'))


@clientes_routes.route('/carta', methods=['GET'])
def Carta():
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    response = requests.get(url_for('cartas_routes.getCartas', _external=True), cookies={'auth': session.get('username')})
    session['establecimiento'] = response.json().get('establecimiento')
    data = []
    if response.status_code == 200:
        cartas = response.json().get('cartas')
        for carta in cartas:
            if carta.get('status') == 1:
                data.append(carta["nombre"])
    
    if len(data) == 1:
        return redirect(url_for('clientes_routes.acorta_seccion_url', nombre=data[0]))
    return render_template('cliente_carta.html', cartas=data, establecimiento=session.get('establecimiento'))

@clientes_routes.route('/secciones/<nombre>', methods=['GET'])
def acorta_seccion_url(nombre):
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    session['carta'] = nombre
    return redirect(url_for('clientes_routes.Secciones'))

@clientes_routes.route('/secciones', methods=['GET'])
def Secciones():
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    response = requests.get(url_for('secciones_routes.getSeccion', _external=True), cookies={'auth': session.get('username'), 'carta': session.get('carta')})
    session['carta']=response.json().get('carta')
    
    data = []
    if response.status_code == 200:
        secciones = response.json().get('secciones')
        for seccion in secciones:
            if seccion[2] == 'Activa':
                data.append(seccion[0])
    if len(data) == 1:
        return redirect(url_for('clientes_routes.acorta_plato_url', nombre=data[0]))
    

    return render_template('cliente_seccion.html', secciones=data, nombre=session.get('carta'), establecimiento=session.get('establecimiento'))

@clientes_routes.route('/plato/<nombre>', methods=['GET'])
def acorta_plato_url(nombre):
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    session['seccion'] = nombre
    return redirect(url_for('clientes_routes.Plato'))

@clientes_routes.route('/plato', methods=['GET'])
def Plato():
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    response = requests.get(url_for('platos_routes.getPlatos', _external=True), cookies={'auth': session.get('username'), 'carta': session.get('carta'), 'seccion': session.get('seccion')})
    data = []
    if response.status_code == 200:
        platos = response.json().get('platos')
        for plato in platos:
            if plato['descripcion'] == "None": plato['descripcion'] = ""
            if plato['status'] == 1:
                data.append({'nombre': plato['nombre'], 'descripcion': plato['descripcion'], 'precio': plato['precio']})
    return render_template('cliente_plato.html', platos=data, nombre=session.get('seccion'), establecimiento=session.get('establecimiento'))

@clientes_routes.route('/pedido', methods=['GET', 'POST'])
def Pedido():
    data = []
    if request.method == 'POST':
        data = request.get_json()
    for plato in data:
        fecha_hora_actual = datetime.now()
        fecha_hora_formateada = fecha_hora_actual.strftime("%Y/%m/%d %H:%M:%S")
        bd = DBController()
        bd.connect()
        count = bd.fetch_data("SELECT COUNT(*) FROM pedidos_activos ")
        consulta = "INSERT INTO pedidos_activos (id, plato, cantidad, precio, usuario, mesa, fecha, estado, categoria) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
        valores = (count[0][0]+1,plato.get('nombre'), plato.get('cantidad'), plato.get('precio'), session.get('username'), session.get('mesa'), fecha_hora_formateada, 0, plato.get('categoria'))
        bd.execute_query(consulta, valores)
        bd.connection.commit()
    return render_template('cliente_carrito.html', establecimiento=session.get('establecimiento'))


@clientes_routes.route('/pedidoFin', methods=['GET'])
def pedidoFin():
    return render_template('cliente_carrito_fin.html')