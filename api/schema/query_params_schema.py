from marshmallow import Schema, fields, validate

PAGINATION_PAGE_VALUE_DEFAULT = 1
PAGINATION_PAGE_VALUE_MIN = 1
PAGINATION_PER_PAGE_VALUE_MIN = 1
PAGINATION_PER_PAGE_VALUE_MAX = 100
PAGINATION_PER_PAGE_VALUE_DEFAULT = 1


class PaginationQueryParamsSchema(Schema):
    page = fields.Int(
        missing=PAGINATION_PAGE_VALUE_DEFAULT,
        description='Pagination page number, first page is 1.',
        validate=validate.Range(
            min=PAGINATION_PAGE_VALUE_MIN),
        required=False)
    per_page = fields.Int(
        missing=PAGINATION_PER_PAGE_VALUE_DEFAULT,
        description='Pagination items per page.',
        validate=validate.Range(
            min=PAGINATION_PER_PAGE_VALUE_MIN, max=PAGINATION_PER_PAGE_VALUE_MAX),
        required=False)


class NameFilterQueryParamsSchema(Schema):
    q = fields.Str(
        description='The (part of the) name to search for',
        validate=validate.Length(min=2, max=40),
        required=False)


class SortUsersQueryParamsSchema(Schema):
    sort = fields.Str(
        description='The field to sort by',
        validate=[validate.OneOf(
            choices=['user_id', 'username', 'rol', '-user_id', '-username', '-rol']), validate.Length(min=1)],
        required=False)


class SortMoviesQueryParamsSchema(Schema):
    sort = fields.Str(
        description='The field to sort by',
        validate=[validate.OneOf(
            choices=['movie_id', 'title', 'date_released', 'budget', 'revenue', '-movie_id', '-title', '-date_released', '-budget', '-revenue']),
            validate.Length(min=1)],
        required=False)
