from flask import redirect, session, url_for
from src.database.dbcontroller import DBController

def LoginUser(username, password):
    db = DBController()
    db.connect()
    resultados = db.fetch_data("SELECT * FROM usuario WHERE usuario = ? AND passwd = ?", (username, password))
    if not resultados:
        db.disconnect()
        return redirect(url_for('login'))
    db.disconnect()
    session['username'] = username  
    return redirect(url_for('dashboard'))