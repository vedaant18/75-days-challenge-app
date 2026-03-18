from app.api.auth import auth_bp
from app.api.challenges import challenges_bp
from app.api.tasks import tasks_bp
from app.api.progress import progress_bp
from app.api.proofs import proofs_bp
from app.api.ai import ai_bp
from app.api.social import social_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(challenges_bp, url_prefix="/api/challenges")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(proofs_bp, url_prefix="/api/proofs")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")
    app.register_blueprint(social_bp, url_prefix="/api/social")
