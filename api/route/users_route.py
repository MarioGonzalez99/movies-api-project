from flask import jsonify, request
from flask_restful import Resource
from marshmallow import ValidationError
from api.model.users import Users
from api.service.pagination import pagination
from api.service.users_services import get_user
from api.service.common_services import APIError, update
from api.service.auth_services import authenticate_admin, authenticate_user, check_if_user_banned
from api.schema.users_schema import users_schema, user_schema, users_query_schema, user_update_schema
from api.model.database import db


class Users_Collection(Resource):
    def get(self):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            query_args = users_query_schema.load(request.args)
            results_info = pagination(query_args, Users)
            results = users_schema.dump(results_info['results'])
            return jsonify({
                'results': results,
                'pagination': {
                    'page': results_info['page'],
                    'per_page': results_info['per_page'],
                    'total_pages': results_info['total_pages'],
                    'total_results': results_info['total_results']
                }
            })

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code


class User(Resource):
    def get(self, user_id):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            if agent.user_id != user_id:
                authenticate_admin(access_token)

            user = get_user(user_id)
            user_json = user_schema.dump(user)

            return user_json

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code

    def patch(self, user_id):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            user = get_user(user_id)
            updated_args = user_update_schema.load(request.form)
            update(user, updated_args)
            db.session.commit()
            user_json = user_schema.dump(user)

            return user_json

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code

    def delete(self, user_id):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            user = get_user(user_id)
            db.session.delete(user)
            db.session.commit()

            return '', 204

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code
