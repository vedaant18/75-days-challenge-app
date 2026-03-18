from app.extensions import ma
from app.models.daily_log import DailyLog
from app.models.task_completion import TaskCompletion


class TaskCompletionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TaskCompletion
        load_instance = True

    task = ma.Nested("TaskSchema", only=("id", "title", "category"))


class DailyLogSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DailyLog
        load_instance = True

    status = ma.String()
    task_completions = ma.Nested(TaskCompletionSchema, many=True)


daily_log_schema = DailyLogSchema()
daily_logs_schema = DailyLogSchema(many=True)
task_completion_schema = TaskCompletionSchema()
