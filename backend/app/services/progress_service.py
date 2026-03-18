from datetime import date, datetime, timezone
from app.extensions import db
from app.models.daily_log import DailyLog
from app.models.task_completion import TaskCompletion
from app.utils.enums import DailyLogStatus, ChallengeStatus
from app.utils.state_machine import evaluate_challenge_state
from app.utils.errors import NotFoundError, ValidationError, ConflictError


class ProgressService:

    @staticmethod
    def get_or_create_today(challenge):
        today = date.today()
        daily_log = DailyLog.query.filter_by(
            challenge_id=challenge.id, date=today
        ).first()

        if not daily_log:
            daily_log = DailyLog(
                challenge_id=challenge.id,
                day_number=challenge.current_day,
                date=today,
                tasks_total=len(challenge.tasks),
            )
            db.session.add(daily_log)
            db.session.flush()

            for task in challenge.tasks:
                tc = TaskCompletion(
                    daily_log_id=daily_log.id,
                    task_id=task.id,
                )
                db.session.add(tc)
            db.session.commit()

        return daily_log

    @staticmethod
    def complete_task(challenge, task_completion_id):
        tc = TaskCompletion.query.get(task_completion_id)
        if not tc:
            raise NotFoundError("Task completion not found")

        # Verify it belongs to this challenge's active day
        daily_log = tc.daily_log
        if daily_log.challenge_id != challenge.id:
            raise ValidationError("Task does not belong to your active challenge")
        if daily_log.date != date.today():
            raise ValidationError("Can only complete tasks for today")
        if tc.is_completed:
            raise ConflictError("Task already completed")

        tc.is_completed = True
        tc.completed_at = datetime.now(timezone.utc)

        # Update denormalized counter
        daily_log.tasks_completed += 1

        # Check if all tasks done and proofs met
        ProgressService._check_day_completion(challenge, daily_log)

        db.session.commit()
        return daily_log

    @staticmethod
    def skip_day(challenge):
        if challenge.skips_used >= challenge.skips_allowed:
            raise ValidationError("No skips remaining")

        today = date.today()
        daily_log = DailyLog.query.filter_by(
            challenge_id=challenge.id, date=today
        ).first()

        if not daily_log:
            raise NotFoundError("No daily log for today")
        if daily_log.status == DailyLogStatus.COMPLETED:
            raise ConflictError("Day already completed")

        daily_log.is_skip = True
        daily_log.status = DailyLogStatus.COMPLETED
        daily_log.completed_at = datetime.now(timezone.utc)
        challenge.skips_used += 1

        # Advance day
        ProgressService._advance_day(challenge)

        db.session.commit()
        return daily_log

    @staticmethod
    def get_dashboard(challenge):
        today_log = DailyLog.query.filter_by(
            challenge_id=challenge.id, date=date.today()
        ).first()

        completed_days = DailyLog.query.filter_by(
            challenge_id=challenge.id, status=DailyLogStatus.COMPLETED
        ).count()

        # Calculate streak
        streak = 0
        logs = DailyLog.query.filter_by(
            challenge_id=challenge.id
        ).order_by(DailyLog.day_number.desc()).all()

        for log in logs:
            if log.status == DailyLogStatus.COMPLETED:
                streak += 1
            else:
                break

        return {
            "challenge_id": challenge.id,
            "title": challenge.title,
            "difficulty": challenge.difficulty.value,
            "status": challenge.status.value,
            "current_day": challenge.current_day,
            "total_days": challenge.total_days,
            "completed_days": completed_days,
            "progress_pct": round((completed_days / challenge.total_days) * 100, 1),
            "streak": streak,
            "skips_used": challenge.skips_used,
            "skips_allowed": challenge.skips_allowed,
            "failures_count": challenge.failures_count,
            "today": {
                "day_number": today_log.day_number if today_log else None,
                "status": today_log.status.value if today_log else None,
                "tasks_completed": today_log.tasks_completed if today_log else 0,
                "tasks_total": today_log.tasks_total if today_log else 0,
                "proofs_submitted": today_log.proofs_submitted if today_log else 0,
            } if today_log else None,
        }

    @staticmethod
    def get_all_logs(challenge):
        return DailyLog.query.filter_by(
            challenge_id=challenge.id
        ).order_by(DailyLog.day_number.asc()).all()

    @staticmethod
    def _check_day_completion(challenge, daily_log):
        all_done = daily_log.tasks_completed >= daily_log.tasks_total
        proofs_met = daily_log.proofs_submitted >= challenge.proof_min_required

        if all_done and proofs_met:
            daily_log.status = DailyLogStatus.COMPLETED
            daily_log.completed_at = datetime.now(timezone.utc)
            ProgressService._advance_day(challenge)

    @staticmethod
    def _advance_day(challenge):
        challenge.current_day += 1
        new_state = evaluate_challenge_state(challenge)
        if new_state:
            challenge.status = new_state
            if new_state == ChallengeStatus.COMPLETED:
                challenge.completed_at = datetime.now(timezone.utc)
            else:
                challenge.failed_at = datetime.now(timezone.utc)
