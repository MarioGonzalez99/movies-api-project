from marshmallow import Schema, fields, validate

MINIMUM_STR_LENGTH = 4
MAXIMUM_STR_LENGTH = 255


class LoginBodyParamsSchema(Schema):
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


class TokenSchema(Schema):
    access_token = fields.Str(
        description='The access token issued by the authorization server',
        validate=validate.Length(max=MAXIMUM_STR_LENGTH),
        required=True)

    token_type = fields.Str(
        description='The type of the token issued',
        validate=validate.OneOf(choices=['Bearer', 'bearer']),
        required=True)

    expires_in = fields.Int(
        description="Lifetime in seconds of the access token",
        required=True
    )


login_schema = LoginBodyParamsSchema()
token_schema = TokenSchema()
