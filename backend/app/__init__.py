import os
from flask import Flask
from config import config_by_name
from app.extensions import db, migrate, jwt, ma, cors, limiter
from app.models.token_blocklist import TokenBlocklist
from app.utils.errors import register_error_handlers


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    ma.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)

    # JWT token blocklist check
    @jwt.token_in_blocklist_loader
    def check_token_blocklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return TokenBlocklist.query.filter_by(jti=jti).first() is not None

    # Register blueprints
    from app.api import register_blueprints
    register_blueprints(app)

    # Register error handlers
    register_error_handlers(app)

    # Import models so Alembic can see them
    from app import models  # noqa: F401

    # Serve uploaded files in development
    if app.config.get("DEBUG"):
        from flask import send_from_directory

        @app.route("/uploads/<path:filename>")
        def uploaded_file(filename):
            return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    return app
