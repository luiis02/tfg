from flask import redirect, url_for, session
from src.database.dbcontroller import DBController

def CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono):
    db = DBController()
    db.connect()

    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ?", (username,))
    if resultados:
        db.disconnect()
        return redirect(url_for('register'))

    resultados = db.fetch_data("SELECT * FROM usuario WHERE email = ?", (email,))
    if resultados:
        db.disconnect()
        return redirect(url_for('register'))
            
    resultados = db.fetch_data("SELECT * FROM usuario WHERE telefono = ?", (telefono,))
    if resultados:
        db.disconnect()
        return redirect(url_for('register'))

    db.execute_query("INSERT INTO usuario (nombre, apellido, establecimiento, provincia, email, passwd, usuario, telefono) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (nombre, apellido, establecimiento, provincia, email, password, username, telefono))
    db.connection.commit()
    db.disconnect()
    return redirect(url_for('login'))

def LoginUser(username, password):
    db = DBController()
    db.connect()
    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ? AND passwd = ?", (username, password))
    db.disconnect()
    init = False
    for resultado in resultados:
        init = True

    if  init:
        session['username'] = username  
    return init