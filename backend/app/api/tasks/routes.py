from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.tasks import tasks_bp
from app.utils.decorators import active_challenge_required
from app.schemas.task_schema import tasks_schema


@tasks_bp.route("", methods=["GET"])
@jwt_required()
@active_challenge_required
def get_tasks(challenge):
    return jsonify(tasks_schema.dump(challenge.tasks)), 200
