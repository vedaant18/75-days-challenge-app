from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api.challenges import challenges_bp
from app.services.challenge_service import ChallengeService
from app.schemas.challenge_schema import (
    challenge_schema,
    challenges_schema,
    create_challenge_schema,
)
from app.utils.decorators import get_current_user_id


@challenges_bp.route("", methods=["POST"])
@jwt_required()
def create_challenge():
    user_id = get_current_user_id()
    data = create_challenge_schema.load(request.get_json())
    challenge = ChallengeService.create_challenge(user_id, data)
    return jsonify(challenge_schema.dump(challenge)), 201


@challenges_bp.route("/active", methods=["GET"])
@jwt_required()
def get_active_challenge():
    user_id = get_current_user_id()
    challenge = ChallengeService.get_active_challenge(user_id)
    return jsonify(challenge_schema.dump(challenge)), 200


@challenges_bp.route("/<int:challenge_id>", methods=["GET"])
@jwt_required()
def get_challenge(challenge_id):
    user_id = get_current_user_id()
    challenge = ChallengeService.get_challenge(user_id, challenge_id)
    return jsonify(challenge_schema.dump(challenge)), 200


@challenges_bp.route("/history", methods=["GET"])
@jwt_required()
def get_challenge_history():
    user_id = get_current_user_id()
    challenges = ChallengeService.get_history(user_id)
    return jsonify(challenges_schema.dump(challenges)), 200
