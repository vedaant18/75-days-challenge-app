from flask import Blueprint

proofs_bp = Blueprint("proofs", __name__)

from app.api.proofs import routes  # noqa: E402, F401
