import os
import json

configPath = os.path.join(os.path.dirname(__file__), 'api_config.json')

with open(configPath) as config_file:
	config = json.load(config_file)

basedir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.dirname('uploads'))

class BaseConfig(object):
    """Base configuration."""
    
    CORS_HEADERS = 'Content-Type'
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']
    DEBUG = False
    UPLOAD_FOLDER=UPLOAD_FOLDER
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    
class LocalConfig(BaseConfig):
    """LOcal configurations."""
    SECRET_KEY = 'be457000f1ea8be89a234d38d8c96ebc752aabe0'
    JWT_SECRET_KEY = 'be457000f1ea8be89a234d38d8c96ebc752aabe0'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    SMS_USERNAME = os.environ.get('SMS_USERNAME')
    SMS_KEY = os.environ.get('SMS_KEY')

class DevelopmentConfig(LocalConfig):
    """Development configuration."""
    DEBUG = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/flask_api'
    DEBUG_TB_ENABLED = True


class TestingConfig(LocalConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/safe_courier_test'
    DEBUG_TB_ENABLED = False


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SECRET_KEY = config.get('SECRET_KEY')
    JWT_SECRET_KEY = config.get('JWT_SECRET_KEY')
    MAIL_USERNAME = config.get('MAIL_USERNAME')
    MAIL_PASSWORD = config.get('MAIL_PASSWORD')
    SMS_USERNAME = config.get('SMS_USERNAME')
    SMS_KEY = config.get('SMS_KEY')
    SQLALCHEMY_DATABASE_URI = config.get('SQLALCHEMY_DATABASE_URI')
    DEBUG = False
    DEBUG_TB_ENABLED = False
    PROPAGATE_EXCEPTIONS = True

"""keys: development, testing, production """
env_config = dict(
    development = DevelopmentConfig,
    testing = TestingConfig,
    production = ProductionConfig
)