from app import ma
from app.models import User, Goal

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        # Exclude sensitive data from being sent in the API response
        exclude = ("password_hash",)
        load_instance = True

class GoalSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Goal
        include_fk = True # Include foreign keys like user_id
        load_instance = True

# Instantiate the schemas
user_schema = UserSchema()
goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)