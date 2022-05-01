from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError
from api.schema.login_schema import login_schema, token_schema
from api.service.common_services import APIError
from api.service.login_services import verify_username_exists, verify_user_password
from api.service.auth_services import encode_auth_token

EXPIRE_IN_SECONDS = 86400
TOKEN_TYPE = 'Bearer'


class Login(Resource):
    def post(self):
        try:
            credentials = login_schema.load(request.form)
            user = verify_username_exists(credentials['username'])
            verify_user_password(user, credentials['password'])
            token = encode_auth_token(user.user_id, EXPIRE_IN_SECONDS)
            token_json = token_schema.dump(
                {'access_token': token, 'token_type': TOKEN_TYPE, 'expires_in': EXPIRE_IN_SECONDS})

            return token_json, 201

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code
