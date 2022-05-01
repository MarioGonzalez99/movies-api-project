from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def hash_password(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def verify_password(password_hash, password):
    return bcrypt.check_password_hash(password_hash, password)
