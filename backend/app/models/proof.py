from datetime import datetime, timezone
from app.extensions import db
from app.utils.enums import ProofStatus


class Proof(db.Model):
    __tablename__ = "proofs"

    id = db.Column(db.Integer, primary_key=True)
    daily_log_id = db.Column(
        db.Integer, db.ForeignKey("daily_logs.id"), nullable=False, index=True
    )
    task_completion_id = db.Column(
        db.Integer, db.ForeignKey("task_completions.id"), nullable=True, unique=True
    )
    image_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500), nullable=True)
    original_filename = db.Column(db.String(255), nullable=True)
    file_size_bytes = db.Column(db.Integer, nullable=True)
    mime_type = db.Column(db.String(50), nullable=True)
    caption = db.Column(db.String(500), nullable=True)
    status = db.Column(db.Enum(ProofStatus), default=ProofStatus.PENDING)
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    daily_log = db.relationship("DailyLog", back_populates="proofs")
    task_completion = db.relationship("TaskCompletion", back_populates="proof")

    def __repr__(self):
        return f"<Proof id={self.id} task_completion={self.task_completion_id}>"
