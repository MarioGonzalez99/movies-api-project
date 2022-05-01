from api.schema.schema import ma
from api.schema.roles_schema import RolesSchema
from api.schema.query_params_schema import PaginationQueryParamsSchema, SortUsersQueryParamsSchema, NameFilterQueryParamsSchema
from api.service.register_services import is_valid_username, get_rol_id
from api.service.encryption import hash_password
from marshmallow import Schema, fields, validate, validates_schema, post_load, ValidationError

DEFAULT_USER_IMG = '/api/v1/images/default_img.jpg'
MAXIMUM_URL_LENGTH = 100
MINIMUM_ROL_ID = 1
MINIMUM_STR_LENGTH = 4
MAXIMUM_STR_LENGTH = 255


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'username', 'rol', 'active', 'user_img')

    rol = fields.Pluck(RolesSchema, 'name')


class UsersRequestQueryParamsSchema(PaginationQueryParamsSchema, SortUsersQueryParamsSchema, NameFilterQueryParamsSchema):
    pass


class UserUpdateBodyParamsSchema(Schema):

    username = fields.Str(
        description='Username of the account',
        validate=validate.Length(
            min=MINIMUM_STR_LENGTH, max=MAXIMUM_STR_LENGTH),
        required=False)

    password = fields.Str(
        description='Password of the account',
        validate=validate.Length(
            min=MINIMUM_STR_LENGTH, max=MAXIMUM_STR_LENGTH),
        required=False)

    active = fields.Bool(
        description='State of the account',
        required=False
    )

    rol_id = fields.Int(
        description='Rol id of the account',
        validate=validate.Range(min=MINIMUM_ROL_ID),
        required=False)

    user_img = fields.Str(missing=DEFAULT_USER_IMG,
                           description='Url of the movie img',
                          validate=validate.Length(max=MAXIMUM_URL_LENGTH),
                           required=False)

    rol = fields.Str(description='Rol of the account',
                     validate=validate.OneOf(
                         choices=['admin', 'regular']),
                     required=False)

    @validates_schema
    def validate_username(self, data, **kwargs):
        if 'username' in data:
            if not is_valid_username(data['username']):
                raise ValidationError(
                    "A user with that username already exists.")

    @post_load
    def create_user(self, data, **kwargs):
        if 'password' in data:
            data['password'] = hash_password(data['password'])
        if 'rol' in data:
            data['rol_id'] = get_rol_id(data['rol'])
            del data['rol']
        return data


user_schema = UsersSchema()
users_schema = UsersSchema(many=True)
users_query_schema = UsersRequestQueryParamsSchema()
user_update_schema = UserUpdateBodyParamsSchema()
