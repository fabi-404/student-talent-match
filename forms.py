from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
## Formular für die Registrierung von Arbeitgebern mit WTForms.##
class RegistrationForm(FlaskForm):
    company = StringField('Firma', validators=[DataRequired()])
    email = StringField('E-Mail', validators=[DataRequired(), Email()])
    password = PasswordField('Passwort', validators=[DataRequired()])
    submit = SubmitField('Registrieren')
