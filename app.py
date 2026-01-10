from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash
from forms import RegistrationForm, StudentRegistrationForm

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Notwendig für Sessions und Flash-Nachrichten, muss noch erstellt werden todo FP ##



# Start

@app.route('/')
def landing():
    return render_template('landing.html')



# Registrierung

@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        university = form.university.data

        hashed_pw = generate_password_hash(password)

        # Hier: Logik zum Speichern in der DB ergänzen
        # database.add_student(email, hashed_pw, university)

        flash('Registrierung erfolgreich! Bitte anmelden.', 'success')
        return redirect(url_for('login_student'))
    return render_template('register_student.html', form=form)


@app.route('/register/employer', methods=['GET', 'POST'])
## Registrierung von Arbeitgebern mit WTForms.##
def register_employer():
    form = RegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        company = form.company.data

        # Passwort hashen
        hashed_pw = generate_password_hash(password)

        # Hier: Logik zum Speichern in der DB ergänzen
        # database.add_employer(email, hashed_pw, company) -> Beispiel

        flash('Registrierung erfolgreich! Bitte anmelden.', 'success')
        return redirect(url_for('login_employer'))
    return render_template('register_employer.html', form=form)
## Python Logik mit Flask sessions für die Registrierung und Anmeldung von Studenten und Arbeitgebern.##



# Login
@app.route('/login/student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        # später: Prüfung von Nutzerdaten
        return redirect(url_for('student_profile'))
    return render_template('login_student.html')


@app.route('/login/employer', methods=['GET', 'POST'])
def login_employer():
    if request.method == 'POST':
        return redirect(url_for('employer_filter'))
    return render_template('login_employer.html')



# Student

@app.route('/student/profile', methods=['GET', 'POST'])
def student_profile():
    if request.method == 'POST':
        # später: Profil aktualisieren
        return redirect(url_for('student_profile'))
    return render_template('student_profile.html')


@app.route('/student/matches')
def student_matches():
    # später: passende Einträge laden
    return render_template('student_matches.html')



# Arbeitgeber: Filter und Swipe

@app.route('/employer/filter', methods=['GET', 'POST'])
def employer_filter():
    if request.method == 'POST':
        return redirect(url_for('employer_swipe'))
    return render_template('employer_filter.html')


@app.route('/employer/swipe')
def employer_swipe():
    # später: ein Profil auswählen
    return render_template('swipe_view.html')


@app.route('/employer/swipe/<int:student_id>/<action>', methods=['POST'])
def swipe_action(student_id, action):
    # später: Swipe speichern
    return redirect(url_for('employer_swipe'))



# Arbeitgeber: Übersicht

@app.route('/employer/matches')
def employer_matches():
    return render_template('employer_matches.html')


@app.route('/employer/invite/<int:student_id>', methods=['POST'])
def send_invite(student_id):
    # später: Einladung hinterlegen
    return redirect(url_for('employer_matches'))


#
# Fehlerseiten
# 
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
