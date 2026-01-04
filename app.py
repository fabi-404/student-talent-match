import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import db, User, JobProfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key' # Change this for production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_talent_match.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Ensure database exists
with app.app_context():
    db.create_all()

# Routes will be implemented here

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            # Simple admin check for now - in real app would be a role field
            session['is_admin'] = (user.username == 'admin') 
            return redirect(url_for('dashboard'))
        
        flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    user_skills = set(s.lower() for s in user.get_skills())
    
    jobs = JobProfile.query.all()
    matches = []
    
    for job in jobs:
        job_skills = job.get_required_skills()
        if not job_skills:
            score = 0
        else:
            match_count = sum(1 for s in job_skills if s.lower() in user_skills)
            score = int((match_count / len(job_skills)) * 100)
        
        matches.append({
            'job': job,
            'score': score
        })
    
    # Sort by score descending
    matches.sort(key=lambda x: x['score'], reverse=True)
    
    return render_template('dashboard.html', user=user, matches=matches)

@app.route('/job/<int:job_id>')
def job_detail(job_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
        
    user = User.query.get(session['user_id'])
    job = JobProfile.query.get_or_404(job_id)
    
    user_skills = set(s.lower() for s in user.get_skills())
    job_skills = job.get_required_skills()
    
    analysis = []
    match_count = 0
    
    for skill in job_skills:
        is_matched = skill.lower() in user_skills
        if is_matched:
            match_count += 1
        analysis.append({
            'skill': skill,
            'matched': is_matched
        })
        
    score = 0
    if job_skills:
        score = int((match_count / len(job_skills)) * 100)
        
    return render_template('job_detail.html', job=job, analysis=analysis, score=score)

@app.route('/skills', methods=['GET', 'POST'])
def skills():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        skills_input = request.form['skills']
        # Split by comma and strip whitespace
        skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        
        user.set_skills(skills_list)
        db.session.commit()
        
        flash('Skills updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    
    current_skills = ', '.join(user.get_skills())
    return render_template('skills.html', current_skills=current_skills)

@app.route('/admin/jobs', methods=['GET', 'POST'])
def admin_jobs():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # In a real app, check if user is admin
    # if not session.get('is_admin'):
    #     flash('Access denied', 'error')
    #     return redirect(url_for('dashboard'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        skills_input = request.form['required_skills']
        
        skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
        
        new_job = JobProfile(
            title=title,
            description=description
        )
        new_job.set_required_skills(skills_list)
        
        db.session.add(new_job)
        db.session.commit()
        
        flash('Job created successfully!', 'success')
        return redirect(url_for('admin_jobs'))
    
    jobs = JobProfile.query.all()
    return render_template('admin_jobs.html', jobs=jobs)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
