from flask import Blueprint

ai_bp = Blueprint("ai", __name__)

from app.api.ai import routes  # noqa: E402, F401
