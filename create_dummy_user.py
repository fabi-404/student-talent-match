from app import app, db, User
from werkzeug.security import generate_password_hash

with app.app_context():
    if not User.query.filter_by(username='testuser').first():
        user = User(username='testuser', password_hash=generate_password_hash('password123', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        print("User 'testuser' created with password 'password123'")
    else:
        print("User 'testuser' already exists")
