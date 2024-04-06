from flask import jsonify, redirect, render_template, request, session, url_for
from flask import redirect, url_for
from flask_login import login_required, login_user
from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.models.forms.loginForm import LoginForm
from src.models.forms.confirmForm import ConfirmForm
##############################################################################################
##############################################################################################
##############################################################################################
import requests
import json
import random
import json
import requests
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from src.models.forms.confirmForm import ConfirmForm
user_routes = Blueprint("user_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################

'''
    - Ruta: register
    - Método: GET, POST
    - Descripción: Permite el registro de un usuario en la aplicación. Crea un formulario 
      y en funcion del estado devuelto por el servicio redirige o muestra un error.
'''
@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        provincia = form.provincia.data
        telefono = form.telefono.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        establecimiento = form.establecimiento.data
        
        #Servicio crear usuario
        status = CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono)
        if( status == 0):
            return redirect(url_for('user_routes.confirm', username=username) + '?cdg=1')
        else: 
            return redirect(url_for('user_routes.register') + '?err=' + str(status))
    
    return render_template('register.html', title='Register', form=form)


@user_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        if LoginUser(username, password):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('user_routes.login')+ '?err=1')

    return render_template('login.html', title='Login', form=form)



@user_routes.route('/confirm/<username>', methods=['GET', 'POST'])
def confirm(username):
    form = ConfirmForm()
    if form.validate_on_submit():
        codigo = form.codigo.data
        estado= ConfirmUser(username, codigo)
        if estado == 0:
            return redirect(url_for('user_routes.login', username=username) + '?err=1')    
        else:
            return redirect(url_for('user_routes.confirm', username=username) + '?err=1')    
    return render_template('confirm.html', title='Confirm', form=form, username=username)



@user_routes.route('/cierresesion')
def cierresesion():
    session.pop('username', None)
    return redirect(url_for('user_routes.login'))




####
# Si retorna 0 ha funcionado correctamente
# Si retorna 1 el usuario esta duplicado
# Si retorna 2 el mail esta duplicado
# Si retorna 3 el telefono esta duplicado
#
####
def CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono):
    db = DBController()
    db.connect()

    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ?", (username,))
    if resultados:
        db.disconnect()
        return 1

    resultados = db.fetch_data("SELECT * FROM usuario WHERE email = ?", (email,))
    if resultados:
        db.disconnect()
        return 2
            
    resultados = db.fetch_data("SELECT * FROM usuario WHERE telefono = ?", (telefono,))
    if resultados:
        db.disconnect()
        return 3    
    resultados = db.fetch_data("SELECT * FROM usuario_sin_confirmar WHERE usuario = ?", (username,))
    if resultados:
        db.disconnect()
        return 1

    resultados = db.fetch_data("SELECT * FROM usuario_sin_confirmar WHERE email = ?", (email,))
    if resultados:
        db.disconnect()
        return 2
            
    resultados = db.fetch_data("SELECT * FROM usuario_sin_confirmar WHERE telefono = ?", (telefono,))
    if resultados:
        db.disconnect()
        return 3

    codigo = str(random.randint(100000, 999999))
    password = password.encode('utf-8')
    db.execute_query("INSERT INTO usuario_sin_confirmar (nombre, apellido, establecimiento, provincia, email, passwd, usuario, telefono, codigo) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, establecimiento, provincia, email, password, username, telefono, codigo))
    db.connection.commit()
    db.disconnect()

    
    msg = f'''
    Hola {nombre}, 

    Nos complace informarte que tu cuenta ha sido creada con éxito. 
    Para confirmar tu cuenta, por favor ingresa el siguiente código: 
    {codigo}
    
    Bienvenido a nuestro sistema.
    '''

    data = {
        'asunto': "Confirma tu cuenta " + nombre,
        'msg': msg,
        'destinatario': email
    }
    json_data = json.dumps(data)
    mail_url = url_for('mail_routes.mail', _external=True)
    requests.post(mail_url, json=data, cookies={'auth':'True'})
    return 0


def LoginUser(username, password):
    db = DBController()
    db.connect()
    password = password.encode('utf-8')
    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ? AND passwd = ?", (username, password))
    db.disconnect()
    init = False
    for resultado in resultados:
        init = True

    if  init:
        session['username'] = username
        session['rol'] = 'admin'
    return init

def ConfirmUser(username, codigo):
    bd = DBController()
    bd.connect()
    resultados = bd.fetch_data("SELECT * FROM usuario_sin_confirmar WHERE codigo = ?", (codigo,))
    if resultados:
        datos = resultados[0]
        bd.disconnect()
        if datos[6] == username:
            bd.connect()
            bd.execute_query("INSERT INTO usuario (nombre, apellido, establecimiento, provincia, email, passwd, usuario, telefono) VALUES (?,?,?,?,?,?,?,?)", datos[0:8])
            bd.execute_query("DELETE FROM usuario_sin_confirmar WHERE usuario = ?", (username,))
            bd.connection.commit()
            return 0
        else:
            return 1
    else:
        bd.disconnect()
        return 1
    
