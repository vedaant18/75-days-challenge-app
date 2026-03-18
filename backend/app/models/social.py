from datetime import datetime, timezone
from app.extensions import db
from app.utils.enums import SharedUpdateType


class Follow(db.Model):
    __tablename__ = "follows"
    __table_args__ = (
        db.CheckConstraint("follower_id != followed_id", name="ck_no_self_follow"),
    )

    follower_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )
    followed_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), primary_key=True
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    follower = db.relationship(
        "User", foreign_keys=[follower_id], back_populates="following"
    )
    followed = db.relationship(
        "User", foreign_keys=[followed_id], back_populates="followers"
    )

    def __repr__(self):
        return f"<Follow {self.follower_id} -> {self.followed_id}>"


class SharedUpdate(db.Model):
    __tablename__ = "shared_updates"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=True
    )
    update_type = db.Column(db.Enum(SharedUpdateType), nullable=False)
    content = db.Column(db.Text, nullable=True)
    day_number = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", back_populates="shared_updates")
    challenge = db.relationship("Challenge")

    def __repr__(self):
        return f"<SharedUpdate {self.update_type.value} by user {self.user_id}>"
