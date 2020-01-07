from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    passwort = PasswordField('Passwort', validators=[DataRequired()])
    remember_me = BooleanField('Eingeloggt bleiben')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    first_name = StringField('Vorname', validators=[DataRequired()])
    last_name = StringField('Nachname', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    passwort = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')


class CreateTicketForm(FlaskForm):
    header =  StringField('Überschrift')
    category = SelectField('Kategorie')
    prio = SelectField('Priorität')
    text = TextAreaField('Text')
    submit = SubmitField('Anlegen')


class ManageUserForm(FlaskForm):
    first_name = StringField('Vorname')
    last_name = StringField('Nachname')
    email = StringField('Email')
    user_group = SelectField('User Gruppe')
    submit = SubmitField('Submit')