from api.model.database import db
from api.model.users import Users
from sqlalchemy import desc
from api.service.common_services import APIError


def get_all_users():
    return Users.query.all()


def get_all_users_count():
    return db.session.query(Users).count()


def get_users_count(q):
    return db.session.query(Users).filter(
        Users.username.like(f'%{q}%')).count()


def get_users(page, per_page, sort, q):
    offset = (page - 1) * per_page
    if sort[0] == '-':
        field = getattr(Users, sort[1:])
        if q is None:
            users = Users.query.order_by(
                desc(field)).offset(offset).limit(per_page).all()
        else:
            users = Users.query.order_by(desc(field)).filter(
                Users.username.like(f'%{q}%')).offset(offset).limit(per_page).all()
    else:
        field = getattr(Users, sort)
        if q is None:
            users = Users.query.order_by(field).offset(
                offset).limit(per_page).all()
        else:
            users = Users.query.order_by(field).filter(
                Users.username.like(f'%{q}%')).offset(offset).limit(per_page).all()
    return users


def get_user(user_id):
    user = Users.query.get(user_id)
    if user is None:
        raise APIError(error_code=404, message='Resource not found',
                       errors=['user_id: Not Found'])
    return user
