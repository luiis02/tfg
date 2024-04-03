
from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request
from src.models.carta import obtenCartas,eliminarCarta,crearCarta,editaCarta
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
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    session['username'] = nombre
    session['mesa'] = mesa
    return redirect(url_for('clientes_routes.getCarta'))


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
        print ( "PAYASO CAMBIA ESTO" )
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
        return redirect(url_for('clientes_routes.Seccion', nombre=data[0]))
        print ( "PAYASO CAMBIA ESTO" )

    return render_template('cliente_seccion.html', secciones=data, nombre=session.get('carta'))

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
            if plato['status'] == 1:
                data.append({'nombre': plato['nombre'], 'descripcion': plato['descripcion'], 'precio': plato['precio']})
    return render_template('cliente_plato.html', platos=data, nombre=session.get('seccion'))
