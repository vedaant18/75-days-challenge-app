from flask import request, jsonify
from flask_jwt_extended import jwt_required
from app.api.social import social_bp
from app.services.social_service import SocialService
from app.schemas.social_schema import (
    shared_update_schema,
    shared_updates_schema,
    create_update_schema,
)
from app.schemas.user_schema import user_schema
from app.utils.decorators import get_current_user_id


@social_bp.route("/profile/<string:username>", methods=["GET"])
def get_profile(username):
    data = SocialService.get_full_profile(username)
    return jsonify(data), 200


@social_bp.route("/share", methods=["POST"])
@jwt_required()
def share_update():
    user_id = get_current_user_id()
    data = create_update_schema.load(request.get_json())
    update = SocialService.create_update(user_id, data)
    return jsonify(shared_update_schema.dump(update)), 201


@social_bp.route("/feed", methods=["GET"])
@jwt_required()
def get_feed():
    user_id = get_current_user_id()
    page = request.args.get("page", 1, type=int)
    updates = SocialService.get_feed(user_id, page)
    return jsonify(shared_updates_schema.dump(updates)), 200


@social_bp.route("/follow/<int:target_user_id>", methods=["POST"])
@jwt_required()
def follow_user(target_user_id):
    user_id = get_current_user_id()
    SocialService.follow(user_id, target_user_id)
    return jsonify({"message": "Followed successfully"}), 200


@social_bp.route("/unfollow/<int:target_user_id>", methods=["POST"])
@jwt_required()
def unfollow_user(target_user_id):
    user_id = get_current_user_id()
    SocialService.unfollow(user_id, target_user_id)
    return jsonify({"message": "Unfollowed successfully"}), 200
