import unittest
from app import app, db, User, JobProfile

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_creation(self):
        with app.app_context():
            u = User(username='test', password_hash='hash')
            db.session.add(u)
            db.session.commit()
            user = User.query.filter_by(username='test').first()
            self.assertIsNotNone(user)

    def test_skill_storage(self):
        with app.app_context():
            u = User(username='test', password_hash='hash')
            u.set_skills(['Python', 'SQL'])
            db.session.add(u)
            db.session.commit()
            
            user = User.query.filter_by(username='test').first()
            self.assertEqual(user.get_skills(), ['Python', 'SQL'])

    def test_job_matching(self):
        with app.app_context():
            # Create user with skills
            u = User(username='student', password_hash='hash')
            u.set_skills(['Python', 'Flask'])
            db.session.add(u)
            
            # Create job with requirements
            j1 = JobProfile(title='Python Dev', description='Desc')
            j1.set_required_skills(['Python', 'Flask', 'SQL']) # 2/3 match = 66%
            db.session.add(j1)
            
            j2 = JobProfile(title='Java Dev', description='Desc')
            j2.set_required_skills(['Java', 'Spring']) # 0/2 match = 0%
            db.session.add(j2)
            
            db.session.commit()
            
            # Test matching logic directly
            user_skills = set(s.lower() for s in u.get_skills())
            job_skills = j1.get_required_skills()
            match_count = sum(1 for s in job_skills if s.lower() in user_skills)
            score = int((match_count / len(job_skills)) * 100)
            
            self.assertEqual(score, 66)

if __name__ == '__main__':
    unittest.main()
