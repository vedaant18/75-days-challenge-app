from datetime import datetime, timezone
from app.extensions import db
from app.utils.enums import TaskCategory


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    challenge_id = db.Column(
        db.Integer, db.ForeignKey("challenges.id"), nullable=False, index=True
    )
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum(TaskCategory), nullable=False)
    position = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    challenge = db.relationship("Challenge", back_populates="tasks")
    completions = db.relationship(
        "TaskCompletion", back_populates="task", lazy="dynamic"
    )

    def __repr__(self):
        return f"<Task {self.title}>"
