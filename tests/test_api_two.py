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

parcel = {
    'name': 'Test Parcel',
    'description': 'test description',
    'weight': 2,
    'price': 200,
    'location': 'test location',
    'destination': 'test destination',
    'status': 'pending',
    'current_location': 'test current location'
}

headers = {'Content-Type': 'application/json'}

expired_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2NDc1MjE0NTksIm5iZiI6MTY0NzUyMTQ1OSwianRpIjoiNDZlNDViYjYtNWQ1Zi00OGE2LTk2ZmYtNjUzMDI4NzE0OWFhIiwiZXhwIjoxNjQ3NjA3ODU5LCJpZGVudGl0eSI6eyJpZCI6MSwicm9sZSI6MX0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyIsInVzZXJfY2xhaW1zIjp7ImlkIjoxLCJyb2xlIjoxfX0.4qUyKkfLuBVTR2hkliMSCt5b-nELyYn3SDHMwD-OVlY'


class APITests(BaseCase):
    def register_user(self):
        response = self.app.\
            post('/api/v1/auth/register',
                 data=json.dumps(user),
                 headers=headers)

    def login_user(self):
        response = self.app.\
            post('/api/v1/auth/login', 
                    data=json.dumps({
                        "email": "test@gmail.com",
                        "password": "test"
                    }), headers=headers)
                    
        return json.loads(response.data)['access_token']

    def test_register_success(self):
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
                 headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', str(response.data))

    def test_login_fail_no_email_or_password(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({}),
                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_login_fail_no_email(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'password': 'test'
                 }),
                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_login_fail_no_password(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'test@gmail.com'
                 }),
                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_login_fail_wrong_email(self):
        self.register_user()
        response = self.app.\
            post('/api/v1/auth/login',
                 data=json.dumps({
                     'email': 'tes@gmail.com',
                     'password': 'test'
                 }),
                 headers=headers)
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
                 headers=headers)
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', str(response.data))

    def test_register_fail_missing_data(self):
        response = self.app.\
            post('/api/v1/auth/register',
                 data=json.dumps({}),
                 headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_success(self):
        self.register_user()
        self.access_token = self.login_user()
        headers['Authorization'] = 'Bearer ' + self.access_token
        response = self.app.\
            post('/api/v1/parcels/create',
                data=json.dumps(parcel),
                headers=headers
            )
        self.assertEqual(response.status_code, 201)
        self.assertIn('Parcel created successfully', str(response.data))

    def test_create_parcel_fail_missing_data(self):
        self.register_user()
        self.access_token = self.login_user()
        headers['Authorization'] = 'Bearer ' + self.access_token
        response = self.app.\
            post('/api/v1/parcels/create',
                data=json.dumps({}),
                headers=headers
            )
        self.assertEqual(response.status_code, 400)

    def test_create_parcel_fail_no_token(self):
        headers['Authorization'] = ''
        response = self.app.\
            post('/api/v1/parcels/create',
                data=json.dumps(parcel),
                headers=headers
            )
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', str(response.data))

    def test_create_parcel_fail_wrong_token(self):
        headers['Authorization'] = 'Bearer ' + 'wrong token'
        response = self.app.\
            post('/api/v1/parcels/create',
                data=json.dumps(parcel),
                headers=headers
            )
        self.assertEqual(response.status_code, 422)
        self.assertIn('Bad Authorization header', str(response.data))

    def test_create_parcel_fail_expired_token(self):
        headers['Authorization'] = 'Bearer ' + expired_token
        response = self.app.\
            post('/api/v1/parcels/create',
                data=json.dumps(parcel),
                headers=headers
            )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token has expired', str(response.data))

    def test_get_all_parcels_success(self):
        self.register_user()
        self.access_token = self.login_user()
        headers['Authorization'] = 'Bearer ' + self.access_token
        response = self.app.\
            get('/api/v1/parcels',
                headers=headers
            )
        self.assertEqual(response.status_code, 200)
        self.assertListEqual(json.loads(response.data)['parcels'], [])

    def test_get_all_parcels_fail_no_token(self):
        headers['Authorization'] = ''
        response = self.app.\
            get('/api/v1/parcels',
                headers=headers
            )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Missing Authorization Header', str(response.data))

    def test_get_all_parcels_fail_wrong_token(self):
        headers['Authorization'] = 'Bearer ' + 'wrong token'
        response = self.app.\
            get('/api/v1/parcels',
                headers=headers
            )
        self.assertEqual(response.status_code, 422)
        self.assertIn('Bad Authorization header', str(response.data))

    def test_get_all_parcels_fail_expired_token(self):
        headers['Authorization'] = 'Bearer ' + expired_token
        response = self.app.\
            get('/api/v1/parcels',
                headers=headers
            )
        self.assertEqual(response.status_code, 401)
        self.assertIn('Token has expired', str(response.data))