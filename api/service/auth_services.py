import datetime
import jwt
from flask import current_app
from api.service.common_services import APIError
from api.service.users_services import get_user
from api.schema.auth_schema import auth_schema


def encode_auth_token(user_id, expires_in_seconds):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in_seconds),
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            current_app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except BaseException as err:
        raise APIError(error_code=400, message='Bad request error', errors=err)


def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            auth_token, current_app.config.get('SECRET_KEY'), algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise APIError(error_code=401, message='Authorization Required', errors=[
                       'Token: Signature expired. Please log in again.'])
    except jwt.InvalidTokenError:
        raise APIError(error_code=401, message='Authorization Required', errors=[
                       'Token: Invalid token. Please log in again.'])


def authenticate_user(auth_token):
    auth = auth_schema.load({'access_token': auth_token})
    token_parsed = auth['access_token'].split()[1]
    user_id = decode_auth_token(token_parsed)
    user = get_user(user_id)
    return user


def authenticate_admin(auth_token):
    user = authenticate_user(auth_token)
    rol = user.rol.name
    if rol != 'admin':
        raise APIError(error_code=403, message='Permission Denied', errors=[
                       "Rol: You don't have permission to access this resource"])
    return user


def check_if_user_banned(user):
    if not user.active:
        raise APIError(error_code=403, message='Permission Denied', errors=[
                       "active: Your account is banned"])
