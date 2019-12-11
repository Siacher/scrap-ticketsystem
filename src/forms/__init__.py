from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    passwort = PasswordField('passwort', validators=[DataRequired()])
    remember_me = BooleanField('eingeloggt bleiben')
    submit = SubmitField('Login')


class CreateTicketForm(FlaskForm):
    prios = []
    categorys = []

    header =  StringField('Überschrift')
    category = SelectField('Kategorie', choices=[(1, "eins"), (2, "zwei")])
    prio = SelectField('Priorität', choices=[(1, "eins"), (2, "zwei")])
    text = TextAreaField('Text')
    submit = SubmitField('Anlegen')