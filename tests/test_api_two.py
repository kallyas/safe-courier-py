from tests.BaseCase import BaseCase
import json

user = {
    'username': 'test',
    'email': 'test@gmail.com',
    'password': 'test',
    'first_name': 'test',
    'last_name': 'test',
    'phone': '0712345678',
    'address': 'test'
}


class TestAuth(BaseCase):
    def register_user(self):
        headers = {'Content-Type': 'application/json'}
        response = self.app.\
            post('/api/v1/auth/register',
                 data=json.dumps(user),
                 headers=headers)

    def test_register_success(self):
        headers = {'Content-Type': 'application/json'}
        response = self.app.\
            post('/api/v1/auth/register', data=json.dumps(user), headers=headers)
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', str(response.data))

    def test_login_success(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'test@gmail.com',
                     'password': 'test'
                 }),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', str(response.data))

    def test_login_fail_no_email_or_password(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({}),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_login_fail_no_email(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'password': 'test'
                 }),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_login_fail_no_password(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'test@gmail.com'
                 }),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)

    def test_login_fail_wrong_email(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'tes@gmail.com',
                     'password': 'test'
                 }),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 404)
        self.assertIn('User by tes@gmail.com not found', str(response.data))

    def test_login_fail_wrong_password(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'test@gmail.com',
                     'password': 'test1'
                 }),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', str(response.data))

    def test_register_fail_missing_data(self):
        response = self.app.\
            post('/api/v1/auth/register',
                 data=json.dumps({}),
                 headers={'Content-Type': 'application/json'})
        self.assertEqual(response.status_code, 400)
