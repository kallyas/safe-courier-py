# safe-courier-py
safe courier api Python version (Flask Restful)


### Usage
```bash
# create virtual environment
$ virtualenv venv

# or
$ python -m venv venv

# activate virtual environment
$ source venv/bin/activate

# install dependencies
$ pip install -r requirements.txt

# run application
$ python app.py

# run tests
$ python -m unittest discover
```

### Endpoints
|Endpoint | Description | Method | Status | Response
|---------|-------------|--------|--------|---------|
| /api/v1/auth/login | Login to the application | POST | 200 | {'acccess_token': '<token>', 'refresh_token': '<token>'...}
| /api/v1/auth/refresh | Refresh access token | POST | 200 | {'acccess_token': '<token>', 'refresh_token': '<token>'...}
| /api/v1/auth/logout | Logout from the application | POST | 200 | {'message': 'Logout successful'}
| /api/v1/auth/logout/refresh | Revoke refresh token | POST | 200 | {'message': 'Successfully logged out'}
| /api/v1/auth/register | Register a new user | POST | 201 | {'message': 'Registration successful'}
| /api/v1/parcels/create | create a parcel | POST | 201 | {'message': 'Parcel created successfully'}
| /api/v1/parcels/<int: percel_id> | Get Parcel by ID | GET | 200 | {...}
| /api/v1/parcels/ | Get Parcels (curent user) | GET | 200 | [{...}, {...}, {...}]
| /api/v1/parcels/<int: percel_id> | Update Parcel | PUT | 200 | {'message': 'Parcel updated successfully'}
| /api/v1/parcels/<int: percel_id> | Delete Parcel | DELETE | 200 | {'message': 'Parcel deleted successfully'}
| /api/v1/users/<int:user_id>/parcels | Get parcels by user id | GET | 200 | [{...}, {...}, {...}]
| /api/v1/users/<int:user_id>/parcels/<int: percel_id> | Get parcel by user id and parcel id | GET | 200 | {...}
| /api/v1/admin/parcels/<int:parcel_id> | Update parcel status, current location (admin only) | PUT | 200 | {...}
| /api/v1/admin/parcels | Get all parcels (admin only) | GET | 200 | [{...}, {...}, {...}]


### API Documentation
[API Documentation](http://api-v3.safe-courier.ml/docs)


### Author
[Kallyas](https://github.com/kallyas)


### License
[MIT](./LIcense)

### Contributing
To contribute to this project, please fork the repository and make a pull request.



