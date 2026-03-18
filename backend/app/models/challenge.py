from datetime import datetime, timezone
from app.extensions import db
from app.utils.enums import DifficultyLevel, ChallengeStatus


class Challenge(db.Model):
    __tablename__ = "challenges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Enum(DifficultyLevel), nullable=False)
    status = db.Column(
        db.Enum(ChallengeStatus), nullable=False, default=ChallengeStatus.ACTIVE
    )
    total_days = db.Column(db.Integer, nullable=False, default=75)
    current_day = db.Column(db.Integer, nullable=False, default=1)
    skips_allowed = db.Column(db.Integer, nullable=False)
    skips_used = db.Column(db.Integer, nullable=False, default=0)
    failures_count = db.Column(db.Integer, nullable=False, default=0)
    proof_min_required = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    completed_at = db.Column(db.DateTime, nullable=True)
    failed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    user = db.relationship("User", back_populates="challenges")
    tasks = db.relationship("Task", back_populates="challenge", cascade="all, delete-orphan")
    daily_logs = db.relationship(
        "DailyLog", back_populates="challenge", cascade="all, delete-orphan", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Challenge {self.title} - Day {self.current_day}/{self.total_days}>"
