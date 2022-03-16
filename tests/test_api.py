# API tests
import unittest
import json
import requests


class TestAPI(unittest.TestCase):
    def setUp(self):
        self.base_url = 'http://localhost:5000/api/v1'
        self.headers = {'Content-Type': 'application/json'}
        self.token = self.auth_user()


    def auth_user(self):
        data = {'email': 'admin@safe-courier.ml', 'password': 'admin'}
        response = requests.post(self.base_url + '/auth/login', data=json.dumps(data), headers=self.headers)
        print(response.json())
        return response.json()['access_token']

    def test_get_all_users(self):
        response = requests.get(self.base_url + '/users', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id(self):
        response = requests.get(self.base_url + '/users/1', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_get_user_by_id_not_found(self):
        response = requests.get(self.base_url + '/users/100', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 404)

    def test_get_all_parcels(self):
        response = requests.get(self.base_url + '/parcels', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_by_id(self):
        response = requests.get(self.base_url + '/parcels/1', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_by_id_not_found(self):
        response = requests.get(self.base_url + '/parcels/100', headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 404)

    def test_create_parcel(self):
        data = {
            "user_id": 1,
            "destination": "Nairobi",
            "pickup_location": "Kisumu",
            "weight": "2",
            "price": "2000",
            "status": "pending"
        }
        response = requests.post(self.base_url + '/parcels/create', data=json.dumps(data), headers=self.headers, authorization='Bearer ' + self.token)
        self.assertEqual(response.status_code, 201)

    


if __name__ == '__main__':
    unittest.main()