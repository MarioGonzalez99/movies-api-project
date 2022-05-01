from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from api.service.common_services import APIError
from api.service.auth_services import authenticate_user, authenticate_admin, check_if_user_banned
from api.service.pagination import pagination_liked_movies
from api.schema.movies_schema import movies_schema, movies_query_schema
from api.model.movies import Movies


class Users_Movies(Resource):
    def get(self, user_id):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            if agent.user_id != user_id:
                authenticate_admin(access_token)

            query_args = movies_query_schema.load(request.args)
            results_info = pagination_liked_movies(query_args, agent.user_id)
            results = movies_schema.dump(results_info['results'])

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
