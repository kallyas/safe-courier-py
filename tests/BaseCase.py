import unittest
from app import app, db
import os


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # create all tables
        db.create_all(app=app)

    def tearDown(self):
        # remove all tables
        db.session.remove()
        db.drop_all(app=app)

