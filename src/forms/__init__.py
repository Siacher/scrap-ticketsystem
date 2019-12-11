from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    passwort = StringField('passwort', validators=[DataRequired()])
    remember_me = BooleanField('eingeloggt bleiben', validators=[DataRequired()])
    submit = SubmitField('Login', validators=[DataRequired()])