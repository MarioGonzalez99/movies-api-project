from api.model.users import Users
from api.service.common_services import APIError
from api.service.encryption import verify_password


def verify_username_exists(username):
    user = Users.query.filter_by(username=username).first()
    if Users.query.filter_by(username=username).first() is None:
        raise APIError(error_code=401, message='Authorization Required',
                       errors=['credentials: You have entered an invalid username or password'])
    return user


def verify_user_password(user, password):
    isValid = verify_password(user.password, password)
    if not isValid:
        raise APIError(error_code=401, message='Authorization Required', errors=[
                       'credentials: You have entered an invalid username or password'])
