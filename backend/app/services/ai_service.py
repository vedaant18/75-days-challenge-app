from flask import current_app
from app.extensions import db
from app.models.ai_chat import AIConversation, AIMessage
from app.models.challenge import Challenge
from app.utils.enums import AIMessageRole
from app.utils.errors import NotFoundError, ValidationError

try:
    from google import genai
except ImportError:
    genai = None


SYSTEM_PROMPT = """You are a discipline coach for the 75-Day Challenge Tracker app.
Your role is to:
- Help users define meaningful daily tasks aligned with their goals
- Analyze their progress and provide actionable feedback
- Motivate without being overly positive — be honest and direct
- Suggest improvements based on patterns you see in their progress
- Remind users of the commitment they made

Keep responses concise and focused on action."""


class AIService:

    @staticmethod
    def chat(user_id, message, conversation_id=None, challenge_id=None):
        api_key = current_app.config.get("GEMINI_API_KEY")
        if not api_key:
            raise ValidationError("AI service not configured")

        # Get or create conversation
        if conversation_id:
            conversation = AIConversation.query.filter_by(
                id=conversation_id, user_id=user_id
            ).first()
            if not conversation:
                raise NotFoundError("Conversation not found")
        else:
            conversation = AIConversation(
                user_id=user_id,
                challenge_id=challenge_id,
                title=message[:100],
            )
            db.session.add(conversation)
            db.session.flush()

        # Save user message
        user_msg = AIMessage(
            conversation_id=conversation.id,
            role=AIMessageRole.USER,
            content=message,
        )
        db.session.add(user_msg)

        # Build message history for Gemini
        contents = []
        for msg in conversation.messages:
            role = "user" if msg.role == AIMessageRole.USER else "model"
            contents.append({"role": role, "parts": [{"text": msg.content}]})
        contents.append({"role": "user", "parts": [{"text": message}]})

        # Add challenge context if available
        context = ""
        cid = conversation.challenge_id or challenge_id
        if cid:
            challenge = Challenge.query.get(cid)
            if challenge:
                context = (
                    f"\nUser's challenge: {challenge.title}, "
                    f"Difficulty: {challenge.difficulty.value}, "
                    f"Day {challenge.current_day}/{challenge.total_days}, "
                    f"Failures: {challenge.failures_count}, "
                    f"Skips used: {challenge.skips_used}/{challenge.skips_allowed}"
                )

        # Call Gemini API
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
            config={
                "system_instruction": SYSTEM_PROMPT + context,
                "max_output_tokens": 1024,
            },
        )

        assistant_content = response.text
        tokens = (
            (response.usage_metadata.prompt_token_count or 0)
            + (response.usage_metadata.candidates_token_count or 0)
        ) if response.usage_metadata else None

        # Save assistant response
        assistant_msg = AIMessage(
            conversation_id=conversation.id,
            role=AIMessageRole.ASSISTANT,
            content=assistant_content,
            tokens_used=tokens,
        )
        db.session.add(assistant_msg)
        db.session.commit()

        return conversation

    @staticmethod
    def get_conversations(user_id):
        return AIConversation.query.filter_by(user_id=user_id).order_by(
            AIConversation.updated_at.desc()
        ).all()

    @staticmethod
    def get_conversation(user_id, conversation_id):
        conversation = AIConversation.query.filter_by(
            id=conversation_id, user_id=user_id
        ).first()
        if not conversation:
            raise NotFoundError("Conversation not found")
        return conversation
