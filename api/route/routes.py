from flask_restful import Api
from api.route.like_route import Like
from api.route.movies_route import Movies_Collection, Movie
from api.route.entry import Entry
from api.route.users_movies_route import Users_Movies
from api.route.users_route import Users_Collection, User
from api.route.register_route import Register
from api.route.login_route import Login

api = Api()


def initialize_routes(api):
    api.add_resource(Entry, '/')
    api.add_resource(Register, '/api/v1/register')
    api.add_resource(Login, '/api/v1/login')
    api.add_resource(Users_Collection, '/api/v1/users')
    api.add_resource(User, '/api/v1/users/<int:user_id>')
    api.add_resource(Users_Movies, '/api/v1/users/<int:user_id>/movies')
    api.add_resource(Movies_Collection, '/api/v1/movies')
    api.add_resource(Movie, '/api/v1/movies/<int:movie_id>')
    api.add_resource(Like, '/api/v1/movies/<int:movie_id>/like')
