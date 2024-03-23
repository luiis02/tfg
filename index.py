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
from src.models.forms.loginForm import LoginForm
from src.models.forms.confirmForm import ConfirmForm
from src.services.getCartasAPI import getCartasAPI
from src.services.manageUser import CreateUser, LoginUser, ConfirmUser


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'




@app.route('/register', methods=['GET', 'POST'])
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
        CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono)
        return redirect(url_for('confirm', username=username) + '?cdg=1')
    
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        #Servicio login usuario
        if LoginUser(username, password):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)



@app.route('/confirm/<username>', methods=['GET', 'POST'])
def confirm(username):
    form = ConfirmForm()
    if form.validate_on_submit():
        codigo = form.codigo.data
        estado= ConfirmUser(username, codigo)
        if estado==0:
            return redirect(url_for('login')+ '?cdg=1')
        else:
            return redirect(url_for('confirm', username=username))
    return render_template('confirm.html', title='Confirm', form=form, username=username)


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    ###############################################################################
    ################################# Obtener las cartas ##########################
    ###############################################################################

    variable = json.loads(getCartas())
    count_cartas = variable['num_cartas']
    # Obtener las cartas
    cartas = variable['cartas']

    cartas_vector = []
    # Iterar sobre las cartas e imprimir su contenido
    for carta in cartas:
        nombre_carta = carta['nombre']
        indice_carta = carta['indice']
        if carta['status'] == 0:
            status_carta = "Inactiva"
        else:
            status_carta = "Activa"
        cartas_vector.append((nombre_carta, indice_carta, status_carta))
        

    return render_template('dashboard.html', username=session["username"], count_cartas=count_cartas, cartas=cartas_vector)



@app.route('/getCartas', methods=['GET'])
def getCartas():
    return getCartasAPI()

@app.route('/removeCarta', methods=['POST'])
def remove_carta():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
        
        data = request.get_json()  
        carta = data.get('cartaId') 
        bd = DBController()
        bd.connect()
        bd.execute_query("DELETE FROM cartas WHERE nombre = ? AND usuario = ?", (carta,session["username"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta eliminada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/createCarta', methods=['POST'])
def create_carta():
    try:
        nombre_carta = request.form.get('nombre_carta')
        indice_carta = request.form.get('indice')
        status_carta = request.form.get('estado')
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO cartas (nombre, indice, status, usuario) VALUES (?,?,?,?)", (nombre_carta, indice_carta, status_carta, session["username"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Datos recibidos correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/editCarta', methods=['POST'])
def edit_carta():
    try:
        nombre_anterior = request.form.get('edita')
        nombre_carta = request.form.get('nombre_carta_editar')
        indice_carta = request.form.get('indice_editar')
        status_carta = request.form.get('estado_editar')
        print(nombre_anterior, nombre_carta, indice_carta, status_carta)
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.execute_query("UPDATE cartas SET nombre = ?, indice = ?, status = ? WHERE nombre = ? AND usuario = ?", (nombre_carta, indice_carta, status_carta, nombre_anterior, session["username"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta editada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/cierresesion')
def cierresesion():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

