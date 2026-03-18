from app.extensions import ma
from app.models.social import SharedUpdate


class SharedUpdateSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SharedUpdate
        load_instance = True

    update_type = ma.String()
    user = ma.Nested("UserSchema", only=("id", "username"))


class CreateUpdateSchema(ma.Schema):
    content = ma.String()
    update_type = ma.String(required=True)
    challenge_id = ma.Integer()
    day_number = ma.Integer()


shared_update_schema = SharedUpdateSchema()
shared_updates_schema = SharedUpdateSchema(many=True)
create_update_schema = CreateUpdateSchema()
