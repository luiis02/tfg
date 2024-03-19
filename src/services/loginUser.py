from flask import redirect, session, url_for
from src.database.dbcontroller import DBController

def LoginUser(username, password):
    db = DBController()
    db.connect()
    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ? AND passwd = ?", (username, password))
    db.disconnect()
    init = False
    for resultado in resultados:
        init = True
        print(resultado)

    if  init:
        session['username'] = username  
    return init