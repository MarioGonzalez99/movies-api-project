from flask import request
from flask_restful import Resource
from api.schema.users_schema import user_schema
from api.schema.register_schema import register_body_schema
from api.model.database import db
from api.model.users import Users
from marshmallow import ValidationError
from api.service.common_services import APIError
from api.service.auth_services import authenticate_admin, check_if_user_banned


class Register(Resource):
    def post(self):
        try:
            user = register_body_schema.load(
                request.form)

            # If user is admin require valid authentication
            if user.rol_id == 1:
                access_token = request.headers.get('Authorization')
                agent = authenticate_admin(access_token)
                check_if_user_banned(agent)

            db.session.add(user)
            db.session.commit()
            created_user = Users.query.filter_by(
                username=user.username).first()
            user_json = user_schema.dump(created_user)
            return user_json, 201
        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code
