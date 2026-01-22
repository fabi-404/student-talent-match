from flask import Flask, request, redirect, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, StudentRegistrationForm, LoginForm, StudentProfileForm, EmployerProfileForm 
from database import get_db_connection
import sqlite3
from functools import wraps

app = Flask(__name__)
app.secret_key = 'super_secret_key'  # Notwendig für Sessions und Flash-Nachrichten##

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
        full_name = form.full_name.data

        hashed_pw = generate_password_hash(password)
     
        # Datenbank-Verbindung über die Funktion aus database.py
        conn = get_db_connection()
        try:
            #schreiben in die Tabelle Student
            conn.execute( 
                         "INSERT INTO Student (email, full_name, university,password_hash) VALUES (?,?,?,?)",
                         (email, full_name, university, hashed_pw))
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
        
        # Datenbank-Verbindung über die Funktion aus database.py
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
        
        # Datenbank-Verbindung über die Funktion aus database.py
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
        
        # Datenbank-Verbindung über die Funktion aus database.py
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
            
            # Skills Hinzufügen
            raw_skills = form.skills.data.split(',')
            skill_names = [s.strip() for s in raw_skills if s.strip()]
            
            for name in skill_names:
                #Prüfen, Skill schon vorhanden ?
                skill = conn.execute ("SELECT id FROM Skill Where name = ?", (name,)).fetchone()
                if skill:
                    skill_id = skill['id']
                else:
                    #der Skill ist neu!
                    cursor = conn.execute("INSERT INTO Skill (name) VALUES (?)", (name,))
                    skill_id = cursor.lastrowid
                
                conn.execute("INSERT OR IGNORE INTO Student_Skill (student_id, skill_id) VALUES (?, ?)",
                             (student_id, skill_id))
                
            conn.commit()
            flash('Profil erfolgreich aktualisiert!', 'success')
            return redirect(url_for('student_profile'))
        
        except Exception as e:
            conn.rollback() 
            flash(f'Fehler beim Speichern: {e}', 'error')
            
    
    # Wenn GET Request (Seite laden): Formular mit DB-Daten füllen
    elif request.method == 'GET':
        form.full_name.data = student['full_name']
        form.university.data = student['university']
        form.bio.data = student['bio']
        form.is_active.data = bool(student['is_active'])
        
        # Skills für die Anzeige im Textfeld laden
        skills_query = """
            SELECT s.name FROM Skill s
            JOIN Student_Skill ss ON s.id = ss.skill_id
            WHERE ss.student_id = ?
        """
        db_skills = conn.execute(skills_query, (student_id,)).fetchall()
        form.skills.data = ", ".join([s['name'] for s in db_skills])

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
    student_id = session.get('student_id')
    
    # Sicherstellung, dass nur Studenten zugreifen (optional, aber gut für Sicherheit)
    if not student_id:
        flash("Diese Seite ist nur für Studenten.", "warning")
        return redirect(url_for('index'))

    conn = get_db_connection()
    
    # Wir holen alle Interviews und verknüpfen (JOIN) sie mit der Arbeitgeber-Tabelle,
    # um den Firmennamen und die E-Mail anzuzeigen.
    query = """
        SELECT i.id, i.message, i.status, i.sent_at, 
               e.company_name, e.email, e.location
        FROM interviews i
        JOIN Employer e ON i.employer_id = e.id
        WHERE i.student_id = ?
        ORDER BY i.sent_at DESC
    """
    matches = conn.execute(query, (student_id,)).fetchall()
    conn.close()

    # Wir rendern ein neues Template und übergeben die Matches
    return render_template('student_matches.html', matches=matches)

# Arbeitgeber: Filter und Swipe

@app.route('/employer/filter', methods=['GET', 'POST'])
@login_required 
def employer_filter():
    conn = get_db_connection()

    if request.method == 'POST':
        # 1. Ausgewählte Skill-IDs aus dem Formular holen (Liste von Strings)
        selected_skills = request.form.getlist('skills') # HTML name="skills"
        
        # 2. Filter in der Session speichern (für die Swipe-Logik)
        if selected_skills:
            # Wir speichern die Liste der IDs
            session['filter_skills'] = selected_skills
            flash(f'{len(selected_skills)} Fähigkeiten als Filter gesetzt.', 'success')
        else:
            # Wenn keine ausgewählt sind, Filter entfernen (alle anzeigen)
            session.pop('filter_skills', None)
            flash('Filter zurückgesetzt. Zeige alle Studenten.', 'info')

        conn.close()
        # 3. Weiterleitung zum Swipen wenn eingerichtet 
        return redirect(url_for('employer_swipe'))
    
    # GET: Alle verfügbaren Skills laden, um sie im Formular anzuzeigen
    # damit werden nur die Skills geladen die Studenten sich auch eingetragen haben um leere swipe views zu vermeiden ##
    query = """
        SELECT DISTINCT s.id, s.name 
        FROM Skill s
        JOIN Student_Skill ss ON s.id = ss.skill_id
        ORDER BY s.name ASC
    """
    available_skills = conn.execute(query).fetchall()
    
    # Aktuell gesetzte Filter laden (um Checkboxen vorzubelegen)
    current_filters = session.get('filter_skills', []) # Gibt leere Liste zurück, wenn kein Filter gesetzt

    conn.close()
    return render_template('employer_filter.html', skills=available_skills, current_filters=current_filters)


@app.route('/employer/swipe')
@login_required 
def employer_swipe():
    employer_id = session.get('employer_id')
    conn = get_db_connection()
    
    # 1. Filter laden
    filter_skills = session.get('filter_skills', [])

    # 2. Query bauen
    query = """
        SELECT s.* FROM Student s
        WHERE s.is_active = 1
        AND s.id NOT IN (SELECT student_id FROM Swipe WHERE employer_id = ?)
    """
    params = [employer_id]
## dynamische Abfrage der Studentenprofile basierend auf den ausgewählten Fähigkeiten des Arbeitgebers.##
    if filter_skills:
        placeholders = ','.join(['?'] * len(filter_skills))
        query += f" AND s.id IN (SELECT student_id FROM Student_Skill WHERE skill_id IN ({placeholders}))"
        params.extend(filter_skills)

    query += " ORDER BY RANDOM() LIMIT 1"
    
    row = conn.execute(query, params).fetchone()
    
    # Hier erstellen wir ein NEUES, sauberes Dictionary für das Template
    candidate_data = None
    
    if row:
        # Wir greifen auf die Spalten der DB zu (via Index oder Name)
        # und speichern sie sicher in einem neuen Objekt
        candidate_data = {
            'id': row['id'],
            # Fallback: Falls 'full_name' leer ist, nutze "Unbekannt"
            'name': row['full_name'] if row['full_name'] else "Unbekannt",
            'major': row['university'] if row['university'] else "Keine Angabe",
            'bio': row['bio'] if row.keys().__contains__('bio') and row['bio'] else "Keine Beschreibung verfügbar.",
        }

        # Skills laden
        skills_rows = conn.execute("""
            SELECT name FROM Skill 
            JOIN Student_Skill ON Skill.id = Student_Skill.skill_id 
            WHERE student_id = ?
        """, (row['id'],)).fetchall()
        
        if skills_rows:
            skill_list = [s['name'] for s in skills_rows]
            candidate_data['skills'] = ", ".join(skill_list)
        else:
            candidate_data['skills'] = "Neu dabei" 

        # Match Score berechnen
        candidate_data['match_score'] = 95 

    conn.close()
    
    # Wir übergeben 'candidate_data' an das Template
    return render_template('card_view_swipe.html', candidate=candidate_data)


@app.route('/employer/action/<int:student_id>/<action>', methods=['POST'])
@login_required
def action_candidate(student_id, action):
    employer_id = session.get('employer_id')
    
    # Mapping: Action aus URL zu Datenbank-Wert
    # invite -> 1 (Like/Einladung)
    # ignore -> 0 (Dislike/Ignorieren)
    direction = 1 if action == 'invite' else 0
    
    conn = get_db_connection()
    try:
        # In die Swipe Tabelle eintragen, damit der Student nicht nochmal angezeigt wird
        conn.execute(
            "INSERT INTO Swipe (employer_id, student_id, direction) VALUES (?, ?, ?)",
            (employer_id, student_id, direction)
        )
        
        # 2. Wenn es ein Like (Invite) ist -> Direkt Einladung erstellen
        if direction == 1:
            # Wir nutzen INSERT OR IGNORE, falls man versehentlich doppelt klickt
            # (obwohl Swipe constraint das meist verhindert)
            conn.execute("""
                INSERT INTO interviews (student_id, employer_id, message, status) 
                VALUES (?, ?, ?, 'pending')
            """, (student_id, employer_id, "Wir würden Sie gerne kennenlernen!"))
            
            flash("Kandidat wurde eingeladen! Einladung gesendet.", "success")
        conn.commit()
    except Exception as e:
        print(f"Swipe Fehler: {e}")
        # Passiert z.B. wenn man doppelt klickt (Unique Constraint), ignorieren wir hier
    finally:
        conn.close()
        
    # Sofort weiter zum nächsten Kandidaten
    return redirect(url_for('employer_swipe'))

@app.route('/debug/reset_swipes') ## route um die swipes zurückzusetzen##
@login_required
def reset_swipes():
    conn = get_db_connection()
    # Löscht ALLE Swipes des aktuell eingeloggten Arbeitgebers
    conn.execute("DELETE FROM Swipe WHERE employer_id = ?", (session.get('employer_id'),))
    conn.commit()
    conn.close()
    flash("Swipe-Historie zurückgesetzt. Alle Kandidaten sind wieder verfügbar.", "info")
    return redirect(url_for('employer_swipe'))



@app.route('/debug/interviews')
def debug_interviews():
    conn = get_db_connection()
    interviews = conn.execute("SELECT * FROM interviews").fetchall()
    conn.close()
    # Listet alle Interviews roh auf
    return str([dict(i) for i in interviews])

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


