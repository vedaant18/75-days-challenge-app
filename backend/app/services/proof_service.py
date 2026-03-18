from datetime import date
from app.extensions import db
from app.models.daily_log import DailyLog
from app.models.proof import Proof
from app.models.task_completion import TaskCompletion
from app.utils.file_upload import save_file_local
from app.utils.errors import NotFoundError, ValidationError


class ProofService:

    @staticmethod
    def upload_proof(challenge, file, task_completion_id=None, caption=""):
        today = date.today()
        daily_log = DailyLog.query.filter_by(
            challenge_id=challenge.id, date=today
        ).first()
        if not daily_log:
            raise NotFoundError("No daily log for today")

        # Validate task_completion belongs to this log
        if task_completion_id:
            tc = TaskCompletion.query.get(task_completion_id)
            if not tc or tc.daily_log_id != daily_log.id:
                raise ValidationError("Task completion not found for today")
            if tc.proof:
                raise ValidationError("Proof already uploaded for this task")

        image_url = save_file_local(file)

        proof = Proof(
            daily_log_id=daily_log.id,
            task_completion_id=task_completion_id,
            image_url=image_url,
            original_filename=file.filename,
            file_size_bytes=file.content_length,
            mime_type=file.content_type,
            caption=caption,
        )
        db.session.add(proof)

        # Update denormalized counter
        daily_log.proofs_submitted += 1

        db.session.commit()
        return proof

    @staticmethod
    def get_proofs_for_day(challenge, day_number):
        daily_log = DailyLog.query.filter_by(
            challenge_id=challenge.id, day_number=day_number
        ).first()
        if not daily_log:
            raise NotFoundError(f"No log found for day {day_number}")
        return daily_log.proofs
