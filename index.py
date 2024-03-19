from flask import Flask, redirect, render_template, request, session, url_for
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo
from flask import redirect, url_for

##########################################################################
##################################### SRC ################################
##########################################################################

from src.models.forms.registerForm import RegistrationForm
from src.database.dbcontroller import DBController
from src.services.createUser import CreateUser
from src.models.forms.loginForm import LoginForm
from src.services.loginUser import LoginUser

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


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

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        #Servicio login usuario
        LoginUser(username, password)

    return render_template('login.html', title='Login', form=form)

@app.route('/')
def dashboard():
    if not session.get('username'):
        return redirect(url_for('login'))
    return 'Hello, World!'



if __name__ == '__main__':
    app.run(debug=True)

