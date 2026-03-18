from functools import wraps
from flask_jwt_extended import get_jwt_identity
from app.models.challenge import Challenge
from app.utils.enums import ChallengeStatus
from app.utils.errors import NotFoundError


def get_current_user_id():
    """Get current user ID from JWT, converting string identity to int."""
    return int(get_jwt_identity())


def active_challenge_required(f):
    """Decorator that loads the user's active challenge or returns 404."""
    @wraps(f)
    def decorated(*args, **kwargs):
        user_id = get_current_user_id()
        challenge = Challenge.query.filter_by(
            user_id=user_id, status=ChallengeStatus.ACTIVE
        ).first()
        if not challenge:
            raise NotFoundError("No active challenge found")
        kwargs["challenge"] = challenge
        return f(*args, **kwargs)
    return decorated
