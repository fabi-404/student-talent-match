from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Email, Length
## Formular für die Registrierung von Arbeitgebern mit WTForms.##
class RegistrationForm(FlaskForm):
    company = StringField('Firma', validators=[DataRequired()])
    full_name = StringField('Vollständiger Name', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

## Formular für Login von Studenten und Arbeitgebern mit WTForms.##
class LoginForm(FlaskForm):
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Anmelden')

## Formular für die Registrierung von Studenten mit WTForms.##
class StudentRegistrationForm(FlaskForm):
    university = StringField('Aktuelle Universität', validators=[DataRequired()])
    full_name = StringField('Vollständiger Name', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')

## Formular für das Profil von Studenten mit WTForms.##
class StudentProfileForm(FlaskForm):
    full_name = StringField('Vollständiger Name', validators=[DataRequired()])
    university = StringField('Universität', validators=[DataRequired()])
    bio = TextAreaField('Über mich', validators=[Length(max=500)])
    skills = StringField('Fähigkeiten (Komma getrennt)') 
    is_active = BooleanField('Profil sichtbar für Arbeitgeber')
    submit = SubmitField('Speichern')


## Formular für das Profil von Arbeitgebern mit WTForms.##
class EmployerProfileForm(FlaskForm):
    company_name = StringField('Firmenname', validators=[DataRequired()])
    location = StringField('Standort')
    description = TextAreaField('Beschreibung', validators=[Length(max=1000)])
    submit = SubmitField('Speichern')

