from flask import Flask, render_template, session, url_for
from flask import url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
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
from src.services.funcionalidadesAPI import funcionalidades_routes
from src.services.chatbot_soporteAPI import chatbot_routes
from src.services.userAPI import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
login_manager = LoginManager(app)

app.register_blueprint(secciones_routes)
app.register_blueprint(cartas_routes)
app.register_blueprint(user_routes)
app.register_blueprint(mail_routes)
app.register_blueprint(platos_routes)
app.register_blueprint(qr_routes)
app.register_blueprint(clientes_routes)
app.register_blueprint(gestion_routes)
app.register_blueprint(funcionalidades_routes)
app.register_blueprint(chatbot_routes)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/')
def index():
    return render_template('landing.html',)

@app.route('/dashboard')
@login_required
def dashboard():
    
    # Hacer la solicitud y manejar la respuesta
    response = requests.get(url_for('cartas_routes.getCartas', _external=True), cookies={'auth': session.get('username')})
    response2 = requests.get(url_for('funcionalidades_routes.getfuncionalidades', _external=True),cookies={'auth': session.get('username')})
    
    ahp = False
    if response2.status_code == 200:
        data = response2.json()
        for funcionalidad in data:
            if funcionalidad[2] == 'ahp':
                ahp = True

    session['ahp'] = ahp    

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

        return render_template('dashboard.html',establecimiento= data.get('establecimiento',0),count_menus= data.get('num_secciones',0),count_platos= data.get('num_platos',0), username=session.get("username"), count_cartas=count_cartas, cartas=cartas_vector, ahp=ahp)
    else:
        # Manejar el caso donde la solicitud no fue exitosa
        return "Error al obtener las cartas", 500  # Puedes personalizar el mensaje de error y el código de estado según sea necesario

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)

