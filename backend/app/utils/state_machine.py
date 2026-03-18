from app.utils.enums import ChallengeStatus


def evaluate_challenge_state(challenge):
    """
    Evaluate and return the new status for a challenge.
    Returns None if no state transition is needed.

    Rules:
    - FAILED: failures_count > skips_allowed
    - STALE: failures_count >= 3 (universal cutoff)
    - COMPLETED: current_day > total_days and day is completed
    """
    if challenge.status != ChallengeStatus.ACTIVE:
        return None

    # Check failure conditions
    if challenge.failures_count > challenge.skips_allowed:
        return ChallengeStatus.FAILED

    if challenge.failures_count >= 3:
        return ChallengeStatus.STALE

    # Check completion
    if challenge.current_day > challenge.total_days:
        return ChallengeStatus.COMPLETED

    return None
