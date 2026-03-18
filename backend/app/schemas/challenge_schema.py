from app.extensions import ma
from app.models.challenge import Challenge
from app.schemas.task_schema import TaskSchema


class ChallengeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Challenge
        load_instance = True

    tasks = ma.Nested(TaskSchema, many=True)
    difficulty = ma.String()
    status = ma.String()


class CreateChallengeSchema(ma.Schema):
    title = ma.String(required=True)
    description = ma.String()
    difficulty = ma.String(required=True)
    tasks = ma.List(ma.Dict(), required=True)


challenge_schema = ChallengeSchema()
challenges_schema = ChallengeSchema(many=True)
create_challenge_schema = CreateChallengeSchema()
