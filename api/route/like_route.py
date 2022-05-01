from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from api.service.common_services import APIError
from api.service.auth_services import authenticate_user, check_if_user_banned
from api.service.movies_services import get_movie, post_like, delete_like
from api.schema.movies_schema import movie_schema
from api.model.database import db


class Like(Resource):
    def post(self, movie_id):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            movie = get_movie(movie_id=movie_id)
            post_like(agent, movie)
            db.session.commit()
            movie_json = movie_schema.dump(movie)

            return movie_json, 201
        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code

    def delete(self, movie_id):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            movie = get_movie(movie_id=movie_id)
            delete_like(agent, movie)
            db.session.commit()

            return '', 204
        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code
