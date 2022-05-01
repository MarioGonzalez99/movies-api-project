from api.model.database import db
from api.model.users import Users
from api.model.roles import Roles
from api.service.encryption import hash_password


def is_valid_username(username):
    return True if Users.query.filter_by(username=username).first() is None else False


def is_valid_rol(rol):
    return True if Roles.query.filter_by(name=rol).first() is not None else False


def get_rol_id(rol_name):
    return Roles.query.filter_by(name=rol_name).first().rol_id


def create_user(username, password, rol, active=True, user_img='/api/v1/images/default_img.jpg'):
    password_hash = hash_password(password)
    rol_id = get_rol_id(rol)
    user = Users(username=username, password=password_hash,
                 rol_id=rol_id, active=active, user_img=user_img)
    db.session.add(user)
    db.session.commit()
