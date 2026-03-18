from datetime import datetime, timezone
from app.extensions import db


class TaskCompletion(db.Model):
    __tablename__ = "task_completions"
    __table_args__ = (
        db.UniqueConstraint("daily_log_id", "task_id", name="uq_log_task"),
    )

    id = db.Column(db.Integer, primary_key=True)
    daily_log_id = db.Column(
        db.Integer, db.ForeignKey("daily_logs.id"), nullable=False, index=True
    )
    task_id = db.Column(
        db.Integer, db.ForeignKey("tasks.id"), nullable=False, index=True
    )
    is_completed = db.Column(db.Boolean, default=False)
    completed_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    daily_log = db.relationship("DailyLog", back_populates="task_completions")
    task = db.relationship("Task", back_populates="completions")
    proof = db.relationship(
        "Proof", back_populates="task_completion", uselist=False
    )

    def __repr__(self):
        status = "done" if self.is_completed else "pending"
        return f"<TaskCompletion task_id={self.task_id} {status}>"
