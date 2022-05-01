from marshmallow import Schema, fields, validate

REGEX_VALIDATOR = r'^(?i)Bearer (.*)'


class AuthSchema(Schema):
    access_token = fields.Str(
        description='Access token to authenticate user',
        validate=validate.Regexp(regex=REGEX_VALIDATOR),
        required=True
    )


auth_schema = AuthSchema()
