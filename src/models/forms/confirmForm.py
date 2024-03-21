
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo 
from flask_wtf import FlaskForm

class ConfirmForm(FlaskForm):
    codigo = StringField('codigo', validators=[DataRequired()])
    