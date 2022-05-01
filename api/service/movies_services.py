import datetime
from api.model.database import db
from api.model.genres import Genres
from api.model.movies import Movies, movies_likes
from sqlalchemy import or_, and_, desc
from flask import current_app
from api.service.common_services import APIError


def convert_string_to_date(date_text):
    try:
        return datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        raise ValueError('Incorrect data format, should be YYYY-MM-DD')


def get_genre_id(name):
    genre = Genres.query.filter_by(name=name).first()
    if genre is None:
        raise ValueError('Genre not found')
    return genre.genre_id


def create_movie(title, description, date_released, genre, budget, revenue, movie_img='/api/v1/images/default_img.jpg'):
    try:
        date = convert_string_to_date(date_released)
        genre_id = get_genre_id(genre)
        movie = Movies(title=title, description=description, date_released=date,
                       genre_id=genre_id, budget=budget, revenue=revenue, movie_img=movie_img)
        db.session.add(movie)
        db.session.commit()
    except BaseException as error:
        current_app.logger.error(
            'Failed to create movie: {}'.format(error), exc_info=1)


def get_all_movies_count():
    return db.session.query(Movies).count()


def get_movies_count(q):
    return db.session.query(Movies).filter(or_(
        Movies.title.like(f'%{q}%'),
        Movies.description.like(f'%{q}%')
    )
    ).count()


def get_movies(page, per_page, sort, q):
    offset = (page - 1) * per_page
    if sort[0] == '-':
        field = getattr(Movies, sort[1:])
        if q is None:
            movies = Movies.query.order_by(
                desc(field)).offset(offset).limit(per_page).all()
        else:
            movies = Movies.query.order_by(desc(field)).filter(or_(
                Movies.title.like(f'%{q}%'),
                Movies.description.like(f'%{q}%')
            )
            ).offset(offset).limit(per_page).all()
    else:
        field = getattr(Movies, sort)
        if q is None:
            movies = Movies.query.order_by(
                field).offset(offset).limit(per_page).all()
        else:
            movies = Movies.query.order_by(field).filter(or_(
                Movies.title.like(f'%{q}%'),
                Movies.description.like(f'%{q}%')
            )
            ).offset(offset).limit(per_page).all()
    return movies


def get_all_liked_movies_count(user_id):
    return db.session.query(movies_likes).filter_by(user_id=user_id).count()


def get_liked_movies_count(user_id, q):
    return Movies.query.filter(and_(Movies.likes.any(user_id=user_id), or_(
        Movies.title.like(f'%{q}%'),
        Movies.description.like(f'%{q}%')
    ))).count()


def get_liked_movies(page, per_page, sort, q, user_id):
    offset = (page - 1) * per_page
    if sort[0] == '-':
        field = getattr(Movies, sort[1:])
        if q is None:
            movies = Movies.query.order_by(
                desc(field)).filter(Movies.likes.any(user_id=user_id)).offset(offset).limit(per_page).all()
        else:
            movies = Movies.query.order_by(desc(field)).filter(and_(Movies.likes.any(user_id=user_id), or_(
                Movies.title.like(f'%{q}%'),
                Movies.description.like(f'%{q}%')
            ))).offset(offset).limit(per_page).all()
    else:
        field = getattr(Movies, sort)
        if q is None:
            movies = Movies.query.order_by(
                field).filter(Movies.likes.any(user_id=user_id)).offset(offset).limit(per_page).all()
        else:
            movies = Movies.query.order_by(field).filter(and_(Movies.likes.any(user_id=user_id), or_(
                Movies.title.like(f'%{q}%'),
                Movies.description.like(f'%{q}%')
            ))).offset(offset).limit(per_page).all()
    return movies


def get_movie(movie_id):
    movie = Movies.query.get(movie_id)
    if movie is None:
        raise APIError(error_code=404, message='Resource not found',
                       errors=['movie_id: Not Found'])
    return movie


def process_likes(movie_id):
    return db.session.query(movies_likes).filter_by(movie_id=movie_id).count()


def is_valid_title(title):
    return True if Movies.query.filter_by(title=title).first() is None else False


def post_like(user, movie):
    if user in movie.likes:
        raise APIError(error_code=400, message='Bad request error', errors=[
                       'like: You already have a like in this movie'])
    movie.likes.append(user)


def delete_like(user, movie):
    if not user in movie.likes:
        raise APIError(error_code=400, message='Bad request error', errors=[
                       "like: You don't have a like in this movie"])
    user.movies.remove(movie)
