from app.extensions import ma
from app.models.ai_chat import AIConversation, AIMessage


class AIMessageSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AIMessage
        load_instance = True

    role = ma.String()


class AIConversationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = AIConversation
        load_instance = True

    messages = ma.Nested(AIMessageSchema, many=True)


class ChatInputSchema(ma.Schema):
    message = ma.String(required=True)
    conversation_id = ma.Integer(load_default=None, allow_none=True)
    challenge_id = ma.Integer(load_default=None, allow_none=True)


ai_conversation_schema = AIConversationSchema()
ai_conversations_schema = AIConversationSchema(many=True, exclude=("messages",))
ai_message_schema = AIMessageSchema()
chat_input_schema = ChatInputSchema()
