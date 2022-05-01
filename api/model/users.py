from api.model.database import db
from api.model.roles import Roles


class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), unique=True, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey(
        'roles.rol_id'), nullable=False)
    rol = db.relationship("Roles", backref="users")
    active = db.Column(db.Boolean, nullable=False, default=True)
    user_img = db.Column(
        db.String(255), default='/api/v1/images/default_img.jpg')
