from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
## Formular für die Registrierung von Arbeitgebern mit WTForms.##
class RegistrationForm(FlaskForm):
    company = StringField('Firma', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

## Formular für die Registrierung von Studenten mit WTForms.##
class StudentRegistrationForm(FlaskForm):
    university = StringField('Aktuelle Universität', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

## Formular für Login von Studenten und Arbeitgebern mit WTForms.##
class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')
