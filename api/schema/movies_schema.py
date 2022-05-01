from api.model.movies import Movies
from api.schema.schema import ma
from api.schema.genres_schema import GenresSchema
from api.schema.query_params_schema import PaginationQueryParamsSchema, SortMoviesQueryParamsSchema, NameFilterQueryParamsSchema
from api.service.movies_services import process_likes, is_valid_title, get_genre_id
from marshmallow import Schema, fields, validate, ValidationError, validates_schema, post_load

DEFAULT_MOVIE_IMG = '/api/v1/images/default_img.jpg'
MAXIMUM_URL_LENGTH = 100
MINIMUM_TITLE_LENGTH = 1
MAXIMUM_TITLE_LENGTH = 100
MAXIMUM_DESCRIPTION_LENGTH = 1000
MINIMUM_GENRE_ID = 1
MINIMUM_BUDGET = 0
MAXIMUM_BUDGET_REVENUE = 2_100_000_000


class MoviesSchema(ma.Schema):
    class Meta:
        fields = ('movie_id', 'title', 'description', 'date_released',
                  'genre', 'budget', 'revenue', 'movie_img', 'likes')

    genre = fields.Pluck(GenresSchema, 'name')
    likes = fields.Method('get_likes')

    def get_likes(self, obj):
        return process_likes(obj.movie_id)


class MoviesRequestQueryParamsSchema(PaginationQueryParamsSchema, SortMoviesQueryParamsSchema, NameFilterQueryParamsSchema):
    pass


class MovieBodyParamsSchema(Schema):
    __model__ = Movies

    title = fields.Str(
        description='Title of the movie',
        validate=validate.Length(
            min=MINIMUM_TITLE_LENGTH, max=MAXIMUM_TITLE_LENGTH),
        required=True)

    description = fields.Str(
        description='Description of the movie',
        validate=validate.Length(max=MAXIMUM_DESCRIPTION_LENGTH),
        required=True)

    date_released = fields.Date(
        description='Date released of the movie',
        required=False)

    genre_id = fields.Int(
        missing=MINIMUM_GENRE_ID,
        description='Genre id of the movie',
        validate=validate.Range(min=MINIMUM_GENRE_ID),
        required=False)

    budget = fields.Int(
        description='Budget of the movie',
        validate=validate.Range(
            min=MINIMUM_BUDGET, max=MAXIMUM_BUDGET_REVENUE),
        required=True)

    revenue = fields.Int(
        description='Revenue of the movie',
        validate=validate.Range(max=MAXIMUM_BUDGET_REVENUE),
        required=True)

    movie_img = fields.Str(missing=DEFAULT_MOVIE_IMG,
                           description='Url of the movie img',
                           validate=validate.Length(max=MAXIMUM_URL_LENGTH),
                           required=False)

    genre = fields.Str(description='Genre of the movie',
                       validate=validate.OneOf(
                           choices=['action', 'drama', 'comedy', 'romance', 'horror', 'thriller', 'fantasy', 'sci-fi']),
                       required=True)

    @validates_schema
    def validate_title(self, data, **kwargs):
        if not is_valid_title(data['title']):
            raise ValidationError("A movie with that title already exists.")

    @post_load
    def create_movie(self, data, **kwargs):
        data['genre_id'] = get_genre_id(data['genre'])
        del data['genre']
        return self.__model__(**data)


class MovieUpdateBodyParamsSchema(Schema):

    title = fields.Str(
        description='Title of the movie',
        validate=validate.Length(
            min=MINIMUM_TITLE_LENGTH, max=MAXIMUM_TITLE_LENGTH),
        required=False)

    description = fields.Str(
        description='Description of the movie',
        validate=validate.Length(max=MAXIMUM_DESCRIPTION_LENGTH),
        required=False)

    date_released = fields.Date(
        description='Date released of the movie',
        required=False)

    genre_id = fields.Int(
        missing=MINIMUM_GENRE_ID,
        description='Genre id of the movie',
        validate=validate.Range(min=MINIMUM_GENRE_ID),
        required=False)

    budget = fields.Int(
        description='Budget of the movie',
        validate=validate.Range(
            min=MINIMUM_BUDGET, max=MAXIMUM_BUDGET_REVENUE),
        required=False)

    revenue = fields.Int(
        description='Revenue of the movie',
        validate=validate.Range(max=MAXIMUM_BUDGET_REVENUE),
        required=False)

    movie_img = fields.Str(missing=DEFAULT_MOVIE_IMG,
                           description='Url of the movie img',
                           validate=validate.Length(max=MAXIMUM_URL_LENGTH),
                           required=False)

    genre = fields.Str(description='Genre of the movie',
                       validate=validate.OneOf(
                           choices=['action', 'drama', 'comedy', 'romance', 'horror', 'thriller', 'fantasy', 'sci-fi']),
                       required=False)

    @validates_schema
    def validate_title(self, data, **kwargs):
        if 'title' in data:
            if not is_valid_title(data['title']):
                raise ValidationError(
                    "A movie with that title already exists.")

    @post_load
    def create_movie(self, data, **kwargs):
        if 'genre' in data:
            data['genre_id'] = get_genre_id(data['genre'])
            del data['genre']
        return data


movie_schema = MoviesSchema()
movies_schema = MoviesSchema(many=True)
movies_query_schema = MoviesRequestQueryParamsSchema()
movie_body_schema = MovieBodyParamsSchema()
movie_update_schema = MovieUpdateBodyParamsSchema()
