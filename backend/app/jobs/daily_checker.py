"""
Daily checker job — runs at end of day to evaluate incomplete logs
and advance challenges to the next day.
"""
from datetime import date, datetime, timedelta, timezone
from app.extensions import db
from app.models.challenge import Challenge
from app.models.daily_log import DailyLog
from app.models.task_completion import TaskCompletion
from app.utils.enums import ChallengeStatus, DailyLogStatus
from app.utils.state_machine import evaluate_challenge_state


def run_daily_check(app):
    """Evaluate all active challenges for yesterday's completion."""
    with app.app_context():
        yesterday = date.today() - timedelta(days=1)
        active_challenges = Challenge.query.filter_by(
            status=ChallengeStatus.ACTIVE
        ).all()

        for challenge in active_challenges:
            _evaluate_challenge_day(challenge, yesterday)

        db.session.commit()


def _evaluate_challenge_day(challenge, check_date):
    daily_log = DailyLog.query.filter_by(
        challenge_id=challenge.id, date=check_date
    ).first()

    if not daily_log:
        return

    # If still pending, mark as missed
    if daily_log.status == DailyLogStatus.PENDING:
        daily_log.status = DailyLogStatus.MISSED
        challenge.failures_count += 1

        # Check state transitions
        new_state = evaluate_challenge_state(challenge)
        if new_state:
            challenge.status = new_state
            if new_state == ChallengeStatus.COMPLETED:
                challenge.completed_at = datetime.now(timezone.utc)
            else:
                challenge.failed_at = datetime.now(timezone.utc)
        else:
            # Advance to next day if still active
            challenge.current_day += 1
            next_date = check_date + timedelta(days=1)
            _create_next_day_log(challenge, next_date)


def _create_next_day_log(challenge, log_date):
    tasks_total = len(challenge.tasks)
    daily_log = DailyLog(
        challenge_id=challenge.id,
        day_number=challenge.current_day,
        date=log_date,
        tasks_total=tasks_total,
    )
    db.session.add(daily_log)
    db.session.flush()

    for task in challenge.tasks:
        tc = TaskCompletion(
            daily_log_id=daily_log.id,
            task_id=task.id,
        )
        db.session.add(tc)
