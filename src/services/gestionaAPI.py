
from flask import redirect, render_template, request, session, url_for
from flask import redirect, url_for
from flask import request
from src.models.gestiona import marcaPedido, obtenpedidos
##############################################################################################
##############################################################################################
##############################################################################################
from flask import Blueprint, redirect, url_for, session, request
gestion_routes = Blueprint("gestion_routes", __name__)
##############################################################################################
##############################################################################################
##############################################################################################
@gestion_routes.route('/gestion', methods=['GET', 'POST'])
def Gestion():
    if 'username' not in session or session['rol'] != 'admin':
        return redirect(url_for('user_routes.login'))
    
    if request.method == 'POST':
        data = request.get_json()
        estado = data.get('estado')
        marcaPedido(estado, data)
    resultados_serializables, categorias_carta = obtenpedidos(session.get('username'))
    print(resultados_serializables)
    
    return render_template('gestion.html', pedidos=resultados_serializables, username=session.get('username'), establecimiento=session.get('establecimiento'), categorias=categorias_carta)



