from datetime import datetime, timezone
from app.extensions import db
from app.utils.enums import DailyLogStatus


class DailyLog(db.Model):
    __tablename__ = "daily_logs"
    __table_args__ = (
        db.UniqueConstraint("challenge_id", "day_number", name="uq_challenge_day"),
        db.UniqueConstraint("challenge_id", "date", name="uq_challenge_date"),
    )

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False, index=True
    )
    day_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(
        db.Enum(DailyLogStatus), nullable=False, default=DailyLogStatus.PENDING
    )
    is_skip = db.Column(db.Boolean, default=False)
    tasks_completed = db.Column(db.Integer, default=0)
    tasks_total = db.Column(db.Integer, nullable=False)
    proofs_submitted = db.Column(db.Integer, default=0)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    challenge = db.relationship("Challenge", back_populates="daily_logs")
    task_completions = db.relationship(
        "TaskCompletion", back_populates="daily_log", cascade="all, delete-orphan"
    )
    proofs = db.relationship(
        "Proof", back_populates="daily_log", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<DailyLog Day {self.day_number} - {self.status.value}>"
