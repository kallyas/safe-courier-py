from sqlalchemy import MetaData
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from .config import env_config
from flask_migrate import Migrate
from flask_cors import CORS
import logging

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
ma = Marshmallow()
api = Api()
jwt = JWTManager()
cors = CORS()

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

def create_app(config_name='testing'):
    app = Flask(__name__)
    app.config.from_object(env_config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    api.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    from .errors.handlers import errors
    app.register_blueprint(errors)

    from models import RevokedToken

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return RevokedToken.is_jti_blacklisted(jti)

    
    @jwt.user_claims_loader
    def add_claims_to_access_token(identity):
        return {
            'id': identity.id,
            'role': identity.role
        }

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id

    from .auth import auth_routes

    auth_routes(api)

        
    return app