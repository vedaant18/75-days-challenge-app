from app.extensions import ma
from app.models.task import Task


class TaskSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Task
        load_instance = True

    category = ma.String()


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
