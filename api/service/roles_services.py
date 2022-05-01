from api.model.database import db
from api.model.roles import Roles
from flask import current_app


def create_rol(name):
    try:
        verify_rol_name_not_used(name)
        rol = Roles(name=name)
        db.session.add(rol)
        db.session.commit()
    except BaseException as error:
        current_app.logger.error(
            'An exception occurred: {}'.format(error), exc_info=1)


def verify_rol_name_not_used(name):
    rol = Roles.query.filter_by(name=name).first()
    if rol is not None:
        raise ValueError('Rol name is already used')
