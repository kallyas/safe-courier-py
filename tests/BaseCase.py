import unittest
from app import app, db


class BaseCase(unittest.TestCase):
    import unittest
from app import app, db


class BaseCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sample.db'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()
        db.create_all(app=app)

    def tearDown(self):
        db.session.remove()
        db.drop_all(app=app)
