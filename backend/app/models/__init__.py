# Import all models so Alembic can discover them
from app.models.user import User, UserProfile
from app.models.challenge import Challenge
from app.models.task import Task
from app.models.daily_log import DailyLog
from app.models.task_completion import TaskCompletion
from app.models.proof import Proof
from app.models.ai_chat import AIConversation, AIMessage
from app.models.social import Follow, SharedUpdate
from app.models.token_blocklist import TokenBlocklist

__all__ = [
    "User", "UserProfile", "Challenge", "Task", "DailyLog",
    "TaskCompletion", "Proof", "AIConversation", "AIMessage",
    "Follow", "SharedUpdate", "TokenBlocklist",
]
