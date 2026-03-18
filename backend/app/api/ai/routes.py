from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api.ai import ai_bp
from app.services.ai_service import AIService
from app.schemas.ai_chat_schema import (
    ai_conversation_schema,
    ai_conversations_schema,
    chat_input_schema,
)
from app.extensions import limiter
from app.utils.decorators import get_current_user_id


@ai_bp.route("/chat", methods=["POST"])
@jwt_required()
@limiter.limit("20 per hour")
def chat():
    user_id = get_current_user_id()
    data = chat_input_schema.load(request.get_json())
    conversation = AIService.chat(
        user_id=user_id,
        message=data["message"],
        conversation_id=data.get("conversation_id"),
        challenge_id=data.get("challenge_id"),
    )
    return jsonify(ai_conversation_schema.dump(conversation)), 200


@ai_bp.route("/conversations", methods=["GET"])
@jwt_required()
def list_conversations():
    user_id = get_current_user_id()
    conversations = AIService.get_conversations(user_id)
    return jsonify(ai_conversations_schema.dump(conversations)), 200


@ai_bp.route("/conversations/<int:conversation_id>", methods=["GET"])
@jwt_required()
def get_conversation(conversation_id):
    user_id = get_current_user_id()
    conversation = AIService.get_conversation(user_id, conversation_id)
    return jsonify(ai_conversation_schema.dump(conversation)), 200
