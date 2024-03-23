from flask import redirect, url_for, session
from src.database.dbcontroller import DBController
from src.mail.send_email import sendEmail
import hashlib
import random
import json
import requests

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
    mail_url = url_for('mail', _external=True)
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
    return init

def ConfirmUser(username, codigo):
    bd = DBController()
    bd.connect()
    resultados = bd.fetch_data("SELECT * FROM usuario_sin_confirmar WHERE codigo = ?", (codigo,))
    if resultados:
        datos = resultados[0]
        bd.disconnect()
        if datos[6] == username:
            nombre = datos[0]
            apellido = datos[1]
            establecimiento = datos[2]
            provincia = datos[3]
            email = datos[4]
            password = datos[5]
            usuario = datos[6]
            telefono = datos[7]
            print(nombre, apellido, establecimiento, provincia, email, password, usuario, telefono)
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