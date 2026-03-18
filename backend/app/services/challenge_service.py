from datetime import date, datetime, timedelta, timezone
from app.extensions import db
from app.models.challenge import Challenge
from app.models.task import Task
from app.models.daily_log import DailyLog
from app.models.task_completion import TaskCompletion
from app.utils.enums import (
    ChallengeStatus,
    DifficultyLevel,
    TaskCategory,
    DailyLogStatus,
    DIFFICULTY_SKIPS,
    DIFFICULTY_PROOF_MIN,
)
from app.utils.errors import ConflictError, ValidationError, NotFoundError


class ChallengeService:

    @staticmethod
    def create_challenge(user_id, data):
        # Check no active challenge exists
        existing = Challenge.query.filter_by(
            user_id=user_id, status=ChallengeStatus.ACTIVE
        ).first()
        if existing:
            raise ConflictError("You already have an active challenge")

        # Validate difficulty
        try:
            difficulty = DifficultyLevel(data["difficulty"].lower())
        except ValueError:
            raise ValidationError("Invalid difficulty. Choose: hard, medium, or soft")

        # Validate tasks
        tasks_data = data.get("tasks", [])
        if len(tasks_data) < 5 or len(tasks_data) > 8:
            raise ValidationError("You must define between 5 and 8 tasks")

        # Calculate settings based on difficulty
        skips_allowed = DIFFICULTY_SKIPS[difficulty]
        proof_min = DIFFICULTY_PROOF_MIN[difficulty]
        if proof_min is None:
            proof_min = len(tasks_data)  # HARD: proof for all tasks

        start = date.today()
        end = start + timedelta(days=74)

        challenge = Challenge(
            user_id=user_id,
            title=data["title"],
            description=data.get("description", ""),
            difficulty=difficulty,
            skips_allowed=skips_allowed,
            proof_min_required=proof_min,
            start_date=start,
            end_date=end,
        )
        db.session.add(challenge)
        db.session.flush()  # Get challenge.id

        # Create tasks
        for i, t in enumerate(tasks_data):
            try:
                category = TaskCategory(t["category"].lower())
            except (ValueError, KeyError):
                raise ValidationError(
                    f"Invalid category for task '{t.get('title', i)}'. "
                    f"Valid: {[c.value for c in TaskCategory]}"
                )
            task = Task(
                challenge_id=challenge.id,
                title=t["title"],
                description=t.get("description", ""),
                category=category,
                position=i,
            )
            db.session.add(task)

        db.session.flush()

        # Create Day 1 log
        ChallengeService._create_daily_log(challenge, 1, start)

        db.session.commit()
        return challenge

    @staticmethod
    def get_active_challenge(user_id):
        challenge = Challenge.query.filter_by(
            user_id=user_id, status=ChallengeStatus.ACTIVE
        ).first()
        if not challenge:
            raise NotFoundError("No active challenge found")
        return challenge

    @staticmethod
    def get_challenge(user_id, challenge_id):
        challenge = Challenge.query.filter_by(
            id=challenge_id, user_id=user_id
        ).first()
        if not challenge:
            raise NotFoundError("Challenge not found")
        return challenge

    @staticmethod
    def get_history(user_id):
        return Challenge.query.filter_by(user_id=user_id).order_by(
            Challenge.created_at.desc()
        ).all()

    @staticmethod
    def _create_daily_log(challenge, day_number, log_date):
        tasks_total = len(challenge.tasks)
        daily_log = DailyLog(
            challenge_id=challenge.id,
            day_number=day_number,
            date=log_date,
            tasks_total=tasks_total,
        )
        db.session.add(daily_log)
        db.session.flush()

        # Pre-create task completion records
        for task in challenge.tasks:
            tc = TaskCompletion(
                daily_log_id=daily_log.id,
                task_id=task.id,
            )
            db.session.add(tc)

        return daily_log
