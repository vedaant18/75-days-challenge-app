from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.api.progress import progress_bp
from app.utils.decorators import active_challenge_required
from app.services.progress_service import ProgressService
from app.schemas.daily_log_schema import daily_log_schema, daily_logs_schema


@progress_bp.route("/today", methods=["GET"])
@jwt_required()
@active_challenge_required
def get_today(challenge):
    daily_log = ProgressService.get_or_create_today(challenge)
    return jsonify(daily_log_schema.dump(daily_log)), 200


@progress_bp.route("/complete-task", methods=["POST"])
@jwt_required()
@active_challenge_required
def complete_task(challenge):
    data = request.get_json()
    task_completion_id = data.get("task_completion_id")
    daily_log = ProgressService.complete_task(challenge, task_completion_id)
    return jsonify(daily_log_schema.dump(daily_log)), 200


@progress_bp.route("/skip", methods=["POST"])
@jwt_required()
@active_challenge_required
def skip_day(challenge):
    daily_log = ProgressService.skip_day(challenge)
    return jsonify(daily_log_schema.dump(daily_log)), 200


@progress_bp.route("/dashboard", methods=["GET"])
@jwt_required()
@active_challenge_required
def dashboard(challenge):
    data = ProgressService.get_dashboard(challenge)
    return jsonify(data), 200


@progress_bp.route("/history", methods=["GET"])
@jwt_required()
@active_challenge_required
def get_history(challenge):
    logs = ProgressService.get_all_logs(challenge)
    return jsonify(daily_logs_schema.dump(logs)), 200
