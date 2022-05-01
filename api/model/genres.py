from api.model.database import db


class Genres(db.Model):
    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
