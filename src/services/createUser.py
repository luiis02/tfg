from flask import redirect, url_for
from src.database.dbcontroller import DBController

def CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono):
    db = DBController()
    db.connect()
    db.execute_query("CREATE TABLE IF NOT EXISTS usuario (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT, apellido TEXT, establecimiento TEXT, provincia TEXT, email TEXT, passwd TEXT, usuario TEXT, telefono TEXT)")

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
