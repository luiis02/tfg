
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo 
from flask_wtf import FlaskForm

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    nombre = StringField('Nombre', validators=[DataRequired()])
    apellido = StringField('Apellido', validators=[DataRequired()])
    provincia = StringField('Provincia', validators=[DataRequired()])
    establecimiento = StringField('Establecimiento', validators=[DataRequired()])
    telefono = StringField('Telefono', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    