from flask_restful import Resource
from flask import jsonify, request
from marshmallow import ValidationError
from api.schema.movies_schema import movies_schema, movie_schema, movies_query_schema, movie_body_schema, movie_update_schema
from api.service.common_services import APIError, update
from api.service.pagination import pagination
from api.service.movies_services import get_movie
from api.service.auth_services import authenticate_admin, authenticate_user, check_if_user_banned
from api.model.database import db
from api.model.movies import Movies


class Movies_Collection(Resource):
    def get(self):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            query_args = movies_query_schema.load(request.args)
            results_info = pagination(query_args, Movies)
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

    def post(self):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            movie = movie_body_schema.load(request.form)
            db.session.add(movie)
            db.session.commit()
            created_movie = Movies.query.filter_by(title=movie.title).first()
            movie_json = movie_schema.dump(created_movie)

            return movie_json, 201

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code


class Movie(Resource):
    def get(self, movie_id):
        try:
            # Authenticate registered users
            access_token = request.headers.get('Authorization')
            agent = authenticate_user(access_token)
            check_if_user_banned(agent)

            movie = get_movie(movie_id=movie_id)
            movie_json = movie_schema.dump(movie)

            return movie_json

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code

    def patch(self, movie_id):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            movie = get_movie(movie_id=movie_id)
            updated_args = movie_update_schema.load(request.form)
            update(movie, updated_args)
            db.session.commit()
            movie_json = movie_schema.dump(movie)

            return movie_json

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code

    def delete(self, movie_id):
        try:
            # Authenticate admin users
            access_token = request.headers.get('Authorization')
            agent = authenticate_admin(access_token)
            check_if_user_banned(agent)

            movie = get_movie(movie_id=movie_id)
            db.session.delete(movie)
            db.session.commit()

            return '', 204

        except APIError as err:
            return err.__dict__, err.error_code
        except ValidationError as err:
            exception = APIError(
                error_code=400, message='Bad request error', errors=err.messages)
            return exception.__dict__, exception.error_code
