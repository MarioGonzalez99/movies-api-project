class APIError(Exception):
    """A API Error Exception"""

    def __init__(self, errors, error_code, message, ):
        self.error_code = error_code
        self.message = message
        self.errors = errors


def update(object, updated_args):
    for key, value in updated_args.items():
        setattr(object, key, value)
