
from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from src.database.dbcontroller import DBController
from flask import request

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
funcionalidades_routes = Blueprint("funcionalidades_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@funcionalidades_routes.route('/funcionalidad', methods=['POST'])
def funcionalidad():
    post_data = request.get_json()
    print(post_data)
    bd = DBController()
    bd.connect()
    result = bd.fetch_data("SELECT COUNT(*) FROM funcionalidades WHERE funcionalidad = %s AND usuario = %s", (post_data['funcion'],session.get('username'),))
    if result[0][0]>0:
        bd.execute_query("DELETE FROM funcionalidades WHERE funcionalidad = %s AND usuario = %s", (post_data['funcion'],session.get('username'),))
    else:
        bd.execute_query("INSERT INTO funcionalidades (funcionalidad, usuario) VALUES (%s, %s)", (post_data['funcion'],session.get('username'),))
    bd.disconnect()
    return jsonify("OK"), 200

@funcionalidades_routes.route('/getfuncionalidades', methods=['GET'])
def getfuncionalidades():
    bd = DBController()
    bd.connect()
    cookies = request.cookies
    result = bd.fetch_data("SELECT * FROM funcionalidades WHERE usuario = %s", (cookies['auth'],))
    print(result)
    bd.disconnect()
    return jsonify(result), 200