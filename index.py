from glob import escape
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
        if LoginUser(username, password):
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return 'Hello, World! You are logged in as ' + session['username'] + '.<br><br><a href="/cierresesion">Cerrar sesión</a>'

@app.route('/cierresesion')
def cierresesion():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

