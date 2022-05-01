from marshmallow import Schema, fields, validate, ValidationError, post_load, validates_schema
from api.model.users import Users
from api.service.encryption import hash_password
from api.service.register_services import is_valid_username, get_rol_id

DEFAULT_USER_IMG = '/api/v1/images/default_img.jpg'
MAXIMUM_URL_LENGTH = 100
DEFAULT_ROL = 'regular'
DEFAULT_ROL_ID = 2
MINIMUM_ROL_ID = 1
MINIMUM_STR_LENGTH = 4
MAXIMUM_STR_LENGTH = 255


class RegisterBodyParamsSchema(Schema):
    __model__ = Users

    username = fields.Str(
        description='Username of the account',
        validate=validate.Length(
            min=MINIMUM_STR_LENGTH, max=MAXIMUM_STR_LENGTH),
        required=True)

    password = fields.Str(
        description='Password of the account',
        validate=validate.Length(
            min=MINIMUM_STR_LENGTH, max=MAXIMUM_STR_LENGTH),
        required=True)

    user_img = fields.Str(missing=DEFAULT_USER_IMG,
                          description='Url of the movie img',
                          validate=validate.Length(max=MAXIMUM_URL_LENGTH),
                          required=False)

    rol_id = fields.Int(
        missing=DEFAULT_ROL_ID,
        description='Rol id of the account',
        validate=validate.Range(min=MINIMUM_ROL_ID),
        required=False)

    rol = fields.Str(missing=DEFAULT_ROL,
                     description='Rol of the account',
                     validate=validate.OneOf(
                         choices=['admin', 'regular']),
                     required=False)

    @validates_schema
    def validate_username(self, data, **kwargs):
        if not is_valid_username(data['username']):
            raise ValidationError("A user with that username already exists.")

    @post_load
    def create_user(self, data, **kwargs):
        data['password'] = hash_password(data['password'])
        data['rol_id'] = get_rol_id(data['rol'])
        del data['rol']
        return self.__model__(**data)


register_body_schema = RegisterBodyParamsSchema()
