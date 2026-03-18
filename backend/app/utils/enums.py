import enum


class DifficultyLevel(str, enum.Enum):
    HARD = "hard"
    MEDIUM = "medium"
    SOFT = "soft"


class ChallengeStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    STALE = "stale"


class TaskCategory(str, enum.Enum):
    HEALTH = "health"
    SPIRITUAL = "spiritual"
    CAREER = "career"
    RELATIONSHIPS = "relationships"
    SOCIAL_LIFE = "social_life"
    FINANCIAL = "financial"
    PERSONAL_GROWTH = "personal_growth"
    FAMILY = "family"


class DailyLogStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    MISSED = "missed"


class ProofStatus(str, enum.Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class AIMessageRole(str, enum.Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class SharedUpdateType(str, enum.Enum):
    MILESTONE = "milestone"
    DAILY_PROGRESS = "daily_progress"
    COMPLETION = "completion"


# Difficulty -> allowed skips mapping
DIFFICULTY_SKIPS = {
    DifficultyLevel.HARD: 0,
    DifficultyLevel.MEDIUM: 1,
    DifficultyLevel.SOFT: 3,
}

# Difficulty -> minimum proofs required per day
# For HARD, this will be set to total task count at challenge creation
DIFFICULTY_PROOF_MIN = {
    DifficultyLevel.HARD: None,  # All tasks — set dynamically
    DifficultyLevel.MEDIUM: 3,
    DifficultyLevel.SOFT: 1,
}
