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
| /api/v1/auth/register | Register a new user | POST | 201 | {'message': 'Registration successful'}



