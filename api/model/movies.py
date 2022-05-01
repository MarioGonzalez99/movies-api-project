from api.model.database import db
from api.model.users import Users
from api.model.genres import Genres

movies_likes = db.Table('movies_likes',
                        db.Column('user_id', db.Integer, db.ForeignKey(
                            'users.user_id', ondelete='CASCADE'), primary_key=True),
                        db.Column('movie_id', db.Integer, db.ForeignKey(
                            'movies.movie_id', ondelete='CASCADE'), primary_key=True)
                        )


class Movies(db.Model):
    movie_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(1000))
    date_released = db.Column(db.Date, nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey(
        'genres.genre_id'), nullable=False)
    genre = db.relationship('Genres', backref='movies')
    budget = db.Column(db.Integer, nullable=False)
    revenue = db.Column(db.Integer, nullable=False)
    movie_img = db.Column(
        db.String(255), default='/api/v1/images/default_img.jpg')
    likes = db.relationship('Users', secondary=movies_likes, lazy='subquery',
                            backref=db.backref('movies', lazy=True))
