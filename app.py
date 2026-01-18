from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, StudentRegistrationForm, LoginForm, StudentProfileForm, EmployerProfileForm 
from database import get_db_connection
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Notwendig für Sessions und Flash-Nachrichten, muss noch erstellt werden todo FP ##

## Login Sicherheit damit man nur auf bestimmte Seiten zugreifen kann wenn man eingeloggt ist##

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'student_id' not in session and 'employer_id' not in session: ## prüft ob student oder arbeitgeber eingeloggt ist ##
            flash('Bitte zuerst anmelden um diese Seite zu sehen.', 'warning')
            return redirect(url_for('index')) ##hier könnte man auch zur login seite weiterleiten ##
        return f(*args, **kwargs)
    return decorated_function

# Start

@app.route('/')
def index():
    return render_template('frontpage.html')

# Registrierung

@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    form = StudentRegistrationForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        university = form.university.data

        hashed_pw = generate_password_hash(password)
     
        # Datenbank-Verbindung über die Funktion aus database.py
        conn = get_db_connection()
        try:
            #schreiben in die Tabelle Student
            conn.execute( 
                         "INSERT INTO Student (email, full_name, university,password_hash) VALUES (?,?,?,?)",
                         (email, email, university, hashed_pw))
            conn.commit()
            
            #Erfolg, User zur Login-Seite weiterleiten
            flash('Registrierung erfolgreich! Bitte anmelden.', 'success')
            return redirect(url_for('login_student'))
        
        except Exception as e:
            print(f"KRITISCHER FEHLER: {e}")
            flash("Fehler bei der Registrierung.")
        finally:
            conn.close()
        

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
        
        conn = get_db_connection()
        try:
            conn.execute(
                "INSERT INTO Employer (email, company_name, password_hash) VALUES (?,?,?)",
                (email, company, hashed_pw))
            
            conn.commit()
            
            flash('Registrierung vom Arbeitgeber erfolgreich! Bitte anmelden.', 'success')
            return redirect(url_for('login_employer'))
        
        except Exception as e:
            flash("Fehler bei der Registrierung.")
        finally:
            conn.close()
  
    return render_template('register_employer.html', form=form)
## Python Logik mit Flask sessions für die Registrierung und Anmeldung von Studenten und Arbeitgebern.##



# Login
@app.route('/login/student', methods=['GET', 'POST'])
def login_student():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        conn = get_db_connection()
        #.fetchone() holt einen einzelnen Datensatz aus der Db.
        user = conn.execute("SELECT * FROM Student WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password_hash'], password):
            
            session['student_email'] = email
            session['student_id'] = user['id']
            session['role'] = 'student'
            
            flash('Erfolgreich eingeloggt!', 'success')
            
            return redirect(url_for('student_profile'))
    
        else:
            # Falls Student nicht gefunden oder Passwort falsch
            flash('E-Mail oder Passwort falsch.', 'error')

        
    return render_template('login_student.html', form=form)


@app.route('/login/employer', methods=['GET', 'POST'])
def login_employer():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        conn = get_db_connection()
        employer = conn.execute("SELECT * FROM Employer WHERE email = ?", (email,)).fetchone()
        conn.close()
        
        if employer and check_password_hash(employer['password_hash'], password):

            session.clear()  # Vorherige Session-Daten löschen
            
            session['employer_name'] = employer['company_name']
            session['employer_id'] = employer['id']
            session['role'] = 'employer'
            
            flash('Erfolgreich eingeloggt!', 'success')
            
            return redirect(url_for('employer_profile'))
    
        else:
            # Falls Arbeitgeber nicht gefunden oder Passwort falsch
            flash('E-Mail oder Passwort falsch.', 'error')
        
        
    return render_template('login_employer.html', form=form)

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('Erfolgreich ausgeloggt.', 'success')
    return redirect(url_for('index'))

# Student

@app.route('/student/profile', methods=['GET', 'POST'])
@login_required 
def student_profile():
    conn = get_db_connection()
    student_id = session.get('student_id')
    
    # Aktuelle Daten laden
    student = conn.execute("SELECT * FROM Student WHERE id = ?", (student_id,)).fetchone()
    
    if student is None:
        conn.close()
        flash("Benutzer nicht gefunden", "error")
        return redirect(url_for('logout'))

    # Formular initialisieren
    form = StudentProfileForm()

    if form.validate_on_submit():
        # Daten speichern (UPDATE)
        is_active_val = 1 if form.is_active.data else 0
        try:
            conn.execute("""
                UPDATE Student 
                SET full_name = ?, university = ?, bio = ?, is_active = ?
                WHERE id = ?
            """, (form.full_name.data, form.university.data, form.bio.data, is_active_val, student_id))
            conn.commit()
            flash('Profil erfolgreich aktualisiert!', 'success')
            return redirect(url_for('student_profile'))
        except Exception as e:
            flash(f'Fehler beim Speichern: {e}', 'error')
    
    # Wenn GET Request (Seite laden): Formular mit DB-Daten füllen
    elif request.method == 'GET':
        form.full_name.data = student['full_name']
        form.university.data = student['university']
        form.bio.data = student['bio']
        form.is_active.data = bool(student['is_active'])

    conn.close()
    return render_template('student_profile.html', form=form)

## Arbeitgeber Profil analog dem Studentenprofil##
@app.route('/employer/profile', methods=['GET', 'POST'])
@login_required 
def employer_profile():
    # 1. Sicherstellen, dass es ein Arbeitgeber ist
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("Nur für Arbeitgeber.", "warning")
        return redirect(url_for('index'))

    conn = get_db_connection()
    
    # 2. Bestehende Daten laden
    employer = conn.execute("SELECT * FROM Employer WHERE id = ?", (employer_id,)).fetchone()
    
    if not employer:
        conn.close()
        return redirect(url_for('logout'))

    form = EmployerProfileForm()

    # 3. Speichern (POST Request)
    if form.validate_on_submit():
        try:
            conn.execute("""
                UPDATE Employer 
                SET company_name = ?, location = ?, description = ?
                WHERE id = ?
            """, (form.company_name.data, form.location.data, 
                  form.description.data, employer_id))
            conn.commit()
            
            # Session Name aktualisieren, falls Firmenname geändert wurde
            session['employer_name'] = form.company_name.data
            
            flash('Unternehmensprofil erfolgreich aktualisiert!', 'success')
            return redirect(url_for('employer_profile'))
        except Exception as e:
            flash(f'Fehler beim Speichern: {e}', 'error')

    # 4. Formular befüllen (GET Request)
    elif request.method == 'GET':
        form.company_name.data = employer['company_name']
        
        # Sicherer Zugriff, falls Felder in DB NULL sind oder Spalten noch fehlen
        # (Dictionary Get method erlaubt default value falls key fehlt)
        form.location.data = employer['location'] if 'location' in employer.keys() else ''
        form.description.data = employer['description'] if 'description' in employer.keys() else ''

    conn.close()
    return render_template('employer_profile.html', form=form)

@app.route('/student/matches')
@login_required ## login requird decorator##
def student_matches():
    # später: passende Einträge laden
    return render_template('student_matches.html')



# Arbeitgeber: Filter und Swipe

@app.route('/employer/filter', methods=['GET', 'POST'])
@login_required ## login requird decorator##
def employer_filter():
    if request.method == 'POST':
        return redirect(url_for('employer_swipe'))
    return render_template('employer_filter.html')


@app.route('/employer/swipe')
@login_required ## login requird decorator##
def employer_swipe():
    # später: ein Profil auswählen
    return render_template('swipe_view.html')


@app.route('/employer/swipe/<int:student_id>/<action>', methods=['POST'])
def swipe_action(student_id, action):
    # später: Swipe speichern
    return redirect(url_for('employer_swipe'))

# Arbeitgeber: Übersicht

@app.route('/employer/matches')
@login_required ## login requird decorator##    
def employer_matches():
    return render_template('employer_matches.html')


@app.route('/employer/invite/<int:student_id>', methods=['POST'])
@login_required ## login requird decorator##
def send_invite(student_id):
    # später: Einladung hinterlegen
    return redirect(url_for('employer_matches'))


#
# Fehlerseiten
# 
@app.errorhandler(404)
def not_found(e):
    return "Seite nicht gefunden (Fehler 404). Bitte prüfen Sie die URL.", 404

@app.errorhandler(500)
def server_error(e):
    # Zeigt den echten Fehler direkt im Browser an
    return f"Ein interner Fehler ist aufgetreten: {e}", 500


