# create flask models
from datetime import datetime
from api import db
from passlib.hash import pbkdf2_sha256
from sqlalchemy.ext.declarative import declared_attr


class ExtraMixin(object):
    @declared_attr
    def created_by(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def updated_by(cls):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


@db.event.listens_for(Role.__table__, 'after_create')
def insert_roles(target, connection, **kw):
    table = Role.__table__
    connection.execute(table.insert(), [
        {'id': 1, 'name': 'Admin'},
        {'id': 2, 'name': 'User'},
        {'id': 3, 'name': 'Guest'}
    ])


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone_number = db.Column(db.String(120), nullable=False)
    # Role is a foreign key from Roles table
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    # Role is a relationship from Roles table
    role = db.relationship('Role', backref=db.backref('users', lazy=True))


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls):
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)


@db.event.listens_for(User.__table__, 'after_create')
def insert_admin(target, connection, **kw):
    table = User.__table__
    connection.execute(table.insert(), [
        {'id': 1, 'username': 'admin', 'email': 'admin@safe-courier.ml',
            'password': User.generate_hash('admin'), 'first_name': 'Admin',
            'last_name': 'Admin', 'address': 'Admin', 'phone_number': 'Admin',
            'role_id': 1}
    ])


class Parcel(db.Model):
    __tablename__ = 'parcels'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    location = db.Column(db.String(120), nullable=False)
    destination = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(120), nullable=False)
    current_location = db.Column(db.String(120), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('parcels', lazy=True))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def update(cls):
        db.session.commit()


class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti=jti).first()
        return bool(query)