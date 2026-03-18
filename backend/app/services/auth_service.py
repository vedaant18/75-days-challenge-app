from app.extensions import db
from app.models.user import User, UserProfile
from app.models.token_blocklist import TokenBlocklist
from app.utils.errors import ConflictError, ValidationError, NotFoundError


class AuthService:

    @staticmethod
    def register(email, username, password):
        if User.query.filter_by(email=email).first():
            raise ConflictError("Email already registered")
        if User.query.filter_by(username=username).first():
            raise ConflictError("Username already taken")
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")

        user = User(email=email.lower().strip(), username=username.strip())
        user.set_password(password)

        profile = UserProfile(user=user)

        db.session.add(user)
        db.session.add(profile)
        db.session.commit()

        return user

    @staticmethod
    def login(email, password):
        user = User.query.filter_by(email=email.lower().strip()).first()
        if not user or not user.check_password(password):
            raise ValidationError("Invalid email or password")
        if not user.is_active:
            raise ValidationError("Account is deactivated")
        return user

    @staticmethod
    def logout(jti):
        blocked = TokenBlocklist(jti=jti)
        db.session.add(blocked)
        db.session.commit()

    @staticmethod
    def get_user(user_id):
        user = User.query.get(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
