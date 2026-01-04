import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    skills_json = db.Column(db.Text, default='[]')

    def get_skills(self):
        try:
            return json.loads(self.skills_json)
        except:
            return []

    def set_skills(self, skills_list):
        self.skills_json = json.dumps(skills_list)

class JobProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_skills_json = db.Column(db.Text, default='[]')

    def get_required_skills(self):
        try:
            return json.loads(self.required_skills_json)
        except:
            return []

    def set_required_skills(self, skills_list):
        self.required_skills_json = json.dumps(skills_list)
