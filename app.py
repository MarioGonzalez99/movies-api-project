from flask import Flask
import os


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL').replace("://", "ql://", 1),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        FLASK_DB_SEEDS_PATH="migrations/seeds.py",
        JSONIFY_PRETTYPRINT_REGULAR=True
    )

    from api.model.database import db
    db.init_app(app)

    from api.schema.schema import ma
    ma.init_app(app)

    from api.route.routes import api, initialize_routes
    initialize_routes(api)
    api.init_app(app)

    from api.service.encryption import bcrypt
    bcrypt.init_app(app)

    return app
