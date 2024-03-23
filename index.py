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
from src.mail.send_email import sendEmail
from src.services.getCartasAPI import getCartasAPI
from src.services.manageUser import CreateUser, LoginUser, ConfirmUser
import requests
from flask import request


app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'



'''
    - Ruta: register
    - Método: GET, POST
    - Descripción: Permite el registro de un usuario en la aplicación. Crea un formulario 
      y en funcion del estado devuelto por el servicio redirige o muestra un error.
'''
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
        status = CreateUser(nombre, apellido, establecimiento, provincia, email, password, username, telefono)
        if( status == 0):
            return redirect(url_for('confirm', username=username) + '?cdg=1')
        else: 
            return redirect(url_for('register') + '?err=' + str(status))
    
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
            return redirect(url_for('login')+ '?err=1')

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
            return redirect(url_for('confirm', username=username) + '?err=1')
    return render_template('confirm.html', title='Confirm', form=form, username=username)


@app.route('/mail', methods=['POST'])
def mail():
    cookies = request.cookies
    print(cookies)
    if cookies.get('auth') != 'True':
        return jsonify({"error": "No autorizado"})
    else:
        data = request.get_json()
        asunto = data.get('asunto')
        msg = data.get('msg')
        destinatario = data.get('destinatario')
        clave = data.get('clave')
        sendEmail(asunto, msg, destinatario)
        return jsonify({"message": "Correo enviado correctamente"})



@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # Hacer la solicitud y manejar la respuesta
    response = requests.get(url_for('getCartas', _external=True), cookies={'auth': session.get('username')})
    
    if response.status_code == 200:  # Verificar si la solicitud fue exitosa
        data = response.json()  # Convertir la respuesta JSON en un diccionario
        
        count_cartas = data.get('num_cartas', 0)  # Obtener el número de cartas, si está disponible
        cartas = data.get('cartas', [])  # Obtener la lista de cartas, si está disponible
        
        cartas_vector = []
        for carta in cartas:
            nombre_carta = carta['nombre']
            indice_carta = carta['indice']
            status_carta = "Inactiva" if carta['status'] == 0 else "Activa"
            cartas_vector.append((nombre_carta, indice_carta, status_carta))

        return render_template('dashboard.html', username=session.get("username"), count_cartas=count_cartas, cartas=cartas_vector)
    else:
        # Manejar el caso donde la solicitud no fue exitosa
        return "Error al obtener las cartas", 500  # Puedes personalizar el mensaje de error y el código de estado según sea necesario


@app.route('/getCartas', methods=['GET'])
def getCartas():
    cookie_value = request.cookies.get('auth')
    session['username'] = cookie_value
    print(session['username'])
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
        if 'username' not in session:
            return redirect(url_for('login'))
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

@app.route('/carta/<nombre>', methods=['GET', 'POST'])
def carta(nombre):
    ###########################ESTE ES EL SERVICIO GETCARTA######################################
    ###########################EN EL DASHBOARD NO SE HACE ASI PORQUE EN EL TIENEN QUE IR ########
    ###########################PÁGINAS, PERO EN ESTE NO############################################
    if 'username' not in session:
        return redirect(url_for('login'))
    bd = DBController()
    bd.connect()
    existe = bd.fetch_data("SELECT COUNT(*) FROM cartas WHERE nombre = ? AND usuario = ?", (nombre, session['username']))
    if existe[0][0] == 0:
        return redirect(url_for('dashboard'))
    session['carta'] = nombre
    existe_seccion = bd.fetch_data("SELECT COUNT(*) FROM seccion WHERE carta = ? AND usuario = ?", (nombre, session['username']))
    contador = existe_seccion[0][0] if existe_seccion else 0
    secciones_vector = []
    if contador > 0:
        secciones = bd.fetch_data("SELECT nombre, indice, status FROM seccion WHERE carta = ? AND usuario = ? ORDER BY indice", (nombre, session['username']))
        for seccion in secciones:
            nombre_seccion = seccion[0]
            indice_seccion = seccion[1]
            status_seccion = "Inactiva" if seccion[2] == 0 else "Activa"
            secciones_vector.append((nombre_seccion, indice_seccion, status_seccion))
    bd.disconnect()
    return render_template('carta.html', nombre=nombre,count_secciones=contador,secciones=secciones_vector)


@app.route('/createSeccion', methods=['POST'])
def create_seccion():
    try:
        nombre_seccion = request.form.get('nombre_seccion')
        indice_seccion = request.form.get('indice')
        status_seccion = request.form.get('estado')
        if status_seccion == 'on':
            status_seccion = True
        else:
            status_seccion = False
        bd = DBController()
        bd.connect()
        bd.execute_query("INSERT INTO seccion (nombre, indice, status, usuario, carta) VALUES (?,?,?,?,?)", (nombre_seccion, indice_seccion, status_seccion, session["username"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()

        return jsonify({"message": "Datos recibidos correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/removeSeccion', methods=['POST'])
def remove_Seccion():
    
    print("entra")
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
            
        data = request.get_json()  
        carta = data.get('cartaId') 
        bd = DBController()
        bd.connect()
        print(carta, session["username"], session["carta"])
        bd.execute_query("DELETE FROM seccion WHERE nombre = ? AND usuario = ? AND carta = ?", (carta, session["username"], session["carta"]))
        bd.connection.commit()
        bd.disconnect()
        return jsonify({"message": "Carta eliminada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/editSeccion', methods=['POST'])
def edita_Seccion():
    try:
        if 'username' not in session:
            return redirect(url_for('login'))
        nombre_anterior = request.form.get('edita')
        nombre_seccion = request.form.get('nombre_seccion_editar')
        indice_seccion = request.form.get('indice_editar')
        status_seccion = request.form.get('estado_editar')
        print(nombre_anterior, nombre_seccion, indice_seccion, status_seccion)
        if status_carta == 'on':
            status_carta = True
        else:
            status_carta = False
        bd = DBController()
        bd.connect()
        bd.disconnect()
        return jsonify({"message": "Carta editada correctamente"})
    except Exception as e:
        return jsonify({"error": str(e)})

    

if __name__ == '__main__':
    app.run(debug=True)

