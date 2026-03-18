from flask import Blueprint

challenges_bp = Blueprint("challenges", __name__)

from app.api.challenges import routes  # noqa: E402, F401
