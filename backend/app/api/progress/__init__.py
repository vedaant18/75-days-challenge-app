from flask import Blueprint

progress_bp = Blueprint("progress", __name__)

from app.api.progress import routes  # noqa: E402, F401
