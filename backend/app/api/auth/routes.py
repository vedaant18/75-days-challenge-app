from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app.api.auth import auth_bp
from app.services.auth_service import AuthService
from app.schemas.user_schema import register_schema, login_schema, user_schema
from app.utils.decorators import get_current_user_id


@auth_bp.route("/register", methods=["POST"])
def register():
    data = register_schema.load(request.get_json())
    user = AuthService.register(
        email=data["email"],
        username=data["username"],
        password=data["password"],
    )
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        "user": user_schema.dump(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = login_schema.load(request.get_json())
    user = AuthService.login(email=data["email"], password=data["password"])
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    return jsonify({
        "user": user_schema.dump(user),
        "access_token": access_token,
        "refresh_token": refresh_token,
    }), 200


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)
    return jsonify({"access_token": access_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    AuthService.logout(jti)
    return jsonify({"message": "Logged out successfully"}), 200


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_current_user_id()
    user = AuthService.get_user(user_id)
    return jsonify(user_schema.dump(user)), 200
