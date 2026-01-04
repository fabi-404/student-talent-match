from flask import Flask, request, redirect, url_for, render_template

app = Flask(__name__)


# Demo-Daten für Studenten (später durch Datenbank ersetzen)
STUDENT_DATA = [
    {
        'id': 1,
        'name': 'Max Müller',
        'age': 24,
        'university': 'TU München',
        'major': 'Informatik (B.Sc.)',
        'bio': 'Leidenschaftlicher Software-Entwickler mit Fokus auf Web-Technologien. Suche nach spannenden Projekten im Bereich KI und Machine Learning.',
        'skills': ['Python', 'JavaScript', 'React', 'TensorFlow', 'Docker'],
        'location': 'München, 5 km entfernt',
        'image': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=500&fit=crop'
    },
    {
        'id': 2,
        'name': 'Anna Schmidt',
        'age': 22,
        'university': 'LMU München',
        'major': 'Medieninformatik (B.A.)',
        'bio': 'UI/UX Design Enthusiastin mit starkem technischem Background. Interessiert an User-Centered Design und Frontend-Development.',
        'skills': ['Figma', 'HTML/CSS', 'Vue.js', 'TypeScript', 'Adobe XD'],
        'location': 'München, 3 km entfernt',
        'image': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400&h=500&fit=crop'
    },
    {
        'id': 3,
        'name': 'Leon Weber',
        'age': 25,
        'university': 'Hochschule München',
        'major': 'Wirtschaftsinformatik (M.Sc.)',
        'bio': 'Analytischer Denker mit Erfahrung in Business Intelligence und Data Science. Suche praktische Erfahrung in Datenanalyse-Projekten.',
        'skills': ['SQL', 'Power BI', 'Python', 'R', 'Excel'],
        'location': 'München, 8 km entfernt',
        'image': 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400&h=500&fit=crop'
    },
    {
        'id': 4,
        'name': 'Sophie Fischer',
        'age': 23,
        'university': 'TU München',
        'major': 'Elektrotechnik (B.Sc.)',
        'bio': 'Hardware-Entwicklung und IoT begeistern mich. Möchte praktische Erfahrung in embedded systems sammeln.',
        'skills': ['C/C++', 'Arduino', 'PCB Design', 'Python', 'MATLAB'],
        'location': 'München, 6 km entfernt',
        'image': 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400&h=500&fit=crop'
    },
    {
        'id': 5,
        'name': 'Tom Becker',
        'age': 26,
        'university': 'Hochschule München',
        'major': 'Informatik (M.Sc.)',
        'bio': 'Full-Stack Developer mit Startup-Erfahrung. Interessiert an innovativen Tech-Projekten und agiler Entwicklung.',
        'skills': ['Node.js', 'React', 'MongoDB', 'AWS', 'GraphQL'],
        'location': 'München, 4 km entfernt',
        'image': 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400&h=500&fit=crop'
    }
]

# Temporärer Speicher für Swipes (später durch Datenbank ersetzen)
swipes = []


def get_student_cards():
    """
    Gibt eine Liste von Studenten zurück, die noch nicht geswiped wurden.
    Später: Filtern basierend auf Arbeitgeber-Präferenzen und bereits gesehenen Profilen.
    """
    swiped_ids = [s['student_id'] for s in swipes]
    available_students = [s for s in STUDENT_DATA if s['id'] not in swiped_ids]
    return available_students


def save_swipe(student_id, liked):
    """
    Speichert eine Swipe-Entscheidung.
    Später: In Datenbank speichern mit Arbeitgeber-ID und Timestamp.
    """
    swipes.append({
        'student_id': student_id,
        'liked': liked
    })
    print(f"Swipe gespeichert: Student {student_id} - {'Like' if liked else 'Nope'}")



# Start

@app.route('/')
def landing():
    return render_template('landing.html')



# Registrierung

@app.route('/register/student', methods=['GET', 'POST'])
def register_student():
    if request.method == 'POST':
        # später: Daten speichern
        return redirect(url_for('login_student'))
    return render_template('register_student.html')


@app.route('/register/employer', methods=['GET', 'POST'])
def register_employer():
    if request.method == 'POST':
        return redirect(url_for('login_employer'))
    return render_template('register_employer.html')



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
    students = get_student_cards()
    return render_template('swipe_view.html', students=students)


@app.route('/employer/swipe/<int:student_id>/<action>', methods=['POST'])
def swipe_action(student_id, action):
    # später: Swipe in Datenbank speichern
    if action == 'like':
        save_swipe(student_id, liked=True)
    elif action == 'nope':
        save_swipe(student_id, liked=False)
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
