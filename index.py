from flask import Flask, redirect, render_template, session, url_for
from flask import redirect, url_for

import requests
##########################################################################
##################################### SRC ################################
##########################################################################
from src.services.seccionesAPI import secciones_routes
from src.services.cartasAPI import cartas_routes
from src.services.userAPI import user_routes
from src.services.mailAPI import mail_routes
from src.services.platosAPI import platos_routes
from src.services.qrAPI import qr_routes
from src.services.clienteAPI import clientes_routes
from src.services.gestionaAPI import gestion_routes

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'





app.register_blueprint(secciones_routes)
app.register_blueprint(cartas_routes)
app.register_blueprint(user_routes)
app.register_blueprint(mail_routes)
app.register_blueprint(platos_routes)
app.register_blueprint(qr_routes)
app.register_blueprint(clientes_routes)
app.register_blueprint(gestion_routes)



@app.route('/dashboard')

def dashboard():
    if 'username' not in session:
        return redirect(url_for('user_routes.login'))
    
    # Hacer la solicitud y manejar la respuesta
    response = requests.get(url_for('cartas_routes.getCartas', _external=True), cookies={'auth': session.get('username')})
    
    if response.status_code == 200:  # Verificar si la solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON en un diccionario
        
        count_cartas = data.get('num_cartas', 0)  # Obtener el número de cartas, si está disponible
        cartas = data.get('cartas', [])  # Obtener la lista de cartas, si está disponible
        session['establecimiento'] = data.get('establecimiento', '')  # Obtener el nombre del establecimiento, si está disponible
        cartas_vector = []
        for carta in cartas:
            nombre_carta = carta['nombre']
            indice_carta = carta['indice']
            status_carta = "Inactiva" if carta['status'] == 0 else "Activa"
            cartas_vector.append((nombre_carta, indice_carta, status_carta))

        return render_template('dashboard.html',establecimiento= data.get('establecimiento',0),count_menus= data.get('num_secciones',0),count_platos= data.get('num_platos',0), username=session.get("username"), count_cartas=count_cartas, cartas=cartas_vector)
    else:
        # Manejar el caso donde la solicitud no fue exitosa
        return "Error al obtener las cartas", 500  # Puedes personalizar el mensaje de error y el código de estado según sea necesario







if __name__ == '__main__':
    app.run(debug=True)

