
from glob import escape
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import redirect, url_for
import json

##########################################################################
##################################### SRC ################################
##########################################################################

from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.services.manageUser import CreateUser, LoginUser
from src.models.forms.loginForm import LoginForm


def getCartasAPI():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))

        estado = 200    
        db = DBController()
        db.connect()

        # Contar el número de cartas del usuario
        resultado = db.fetch_data("SELECT COUNT(*) FROM cartas WHERE usuario = ?", (session['username'],))
        num_cartas = resultado[0][0] if resultado else 0

        data = {"num_cartas": num_cartas, "cartas": []}
        
        if num_cartas > 0:
            obteninfo = db.fetch_data("SELECT nombre, indice, status FROM cartas WHERE usuario = ?", (session['username'],))
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