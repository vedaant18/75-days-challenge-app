from flask import jsonify


class APIError(Exception):
    """Base API error."""
    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        return {"error": self.message, "status": self.status_code}


class NotFoundError(APIError):
    status_code = 404


class ConflictError(APIError):
    status_code = 409


class ForbiddenError(APIError):
    status_code = 403


class ValidationError(APIError):
    status_code = 422


def register_error_handlers(app):
    @app.errorhandler(APIError)
    def handle_api_error(error):
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found", "status": 404}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error", "status": 500}), 500
