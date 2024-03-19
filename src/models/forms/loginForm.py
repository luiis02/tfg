
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo 
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    