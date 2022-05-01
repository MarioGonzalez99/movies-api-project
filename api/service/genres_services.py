from api.model.database import db
from api.model.genres import Genres
from flask import current_app


def create_genre(name):
    try:
        verify_genre_name_not_used(name)
        genre = Genres(name=name)
        db.session.add(genre)
        db.session.commit()
    except BaseException as error:
        current_app.logger.error(
            'An exception occurred: {}'.format(error), exc_info=1)


def verify_genre_name_not_used(name):
    genre = Genres.query.filter_by(name=name).first()
    if genre is not None:
        raise ValueError('Genre name is already used')
