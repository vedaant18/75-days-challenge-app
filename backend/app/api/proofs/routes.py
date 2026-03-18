from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api.proofs import proofs_bp
from app.utils.decorators import active_challenge_required
from app.services.proof_service import ProofService
from app.schemas.proof_schema import proof_schema, proofs_schema


@proofs_bp.route("/upload", methods=["POST"])
@jwt_required()
@active_challenge_required
def upload_proof(challenge):
    file = request.files.get("image")
    task_completion_id = request.form.get("task_completion_id", type=int)
    caption = request.form.get("caption", "")

    proof = ProofService.upload_proof(
        challenge=challenge,
        file=file,
        task_completion_id=task_completion_id,
        caption=caption,
    )
    return jsonify(proof_schema.dump(proof)), 201


@proofs_bp.route("/day/<int:day_number>", methods=["GET"])
@jwt_required()
@active_challenge_required
def get_proofs_for_day(challenge, day_number):
    proofs = ProofService.get_proofs_for_day(challenge, day_number)
    return jsonify(proofs_schema.dump(proofs)), 200
