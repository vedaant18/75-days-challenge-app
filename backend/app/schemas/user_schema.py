from app.extensions import ma
from app.models.user import User, UserProfile


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ("password_hash",)
        load_instance = True

    profile = ma.Nested("UserProfileSchema")


class UserProfileSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserProfile
        exclude = ("user_id",)
        load_instance = True


class RegisterSchema(ma.Schema):
    email = ma.String(required=True)
    username = ma.String(required=True)
    password = ma.String(required=True, load_only=True)


class LoginSchema(ma.Schema):
    email = ma.String(required=True)
    password = ma.String(required=True, load_only=True)


user_schema = UserSchema()
user_profile_schema = UserProfileSchema()
register_schema = RegisterSchema()
login_schema = LoginSchema()
