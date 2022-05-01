from api.model.database import db


class Roles(db.Model):
    rol_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
