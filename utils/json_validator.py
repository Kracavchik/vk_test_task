from functools import wraps

from flask import request, jsonify
from jsonschema import Draft7Validator


class JsonValidator:
    """
    Validate json from request
    """
    def __init__(self, schema):
        self.schema = schema
        self.validator = Draft7Validator(self.schema)

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if hasattr(request, 'json'):
                if request.json:
                    json = request.get_json()
                    validation_errors = self.validator.iter_errors(json)
                    error_message = {}
                    try:
                        #  use while to trigger error if generator is empty from start
                        while True:
                            error = next(validation_errors)
                            error_message[error.path[0]] = f"{error.message}"
                    except StopIteration:
                        if error_message:
                            #  Found error(s) in json
                            return jsonify(error_message)
                        #  OK
                        return func(*args, **kwargs)
            else:
                return jsonify({'JsonError': 'Json is empty or not exist'})
        return wrapper
