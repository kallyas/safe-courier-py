from api import ma
from marshmallow_sqlalchemy import ModelSchema
from models import Parcel, User

class UserSchema(ModelSchema):
    class Meta:
        fields = ('id', 'username', 'email', 
                    'address', 'phone_number',
                    'first_name', 'last_name',
                    'role_id'
                    )


class ParcelSchema(ModelSchema):
    class Meta:
        fields = ('id', 'user_id', 'name', 'description', 'weight', 'price', 'status', 'location', 'destination', 'created_at', 'updated_at', 'current_location')
        model = Parcel

