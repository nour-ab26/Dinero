from app import ma
from app.models import User, Goal, Bill 
from marshmallow import fields

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


class BillSchema(ma.SQLAlchemyAutoSchema):
    # Enforce a specific date format for API consistency
    due_date = fields.Date(format='%Y-%m-%d')

    class Meta:
        model = Bill
        include_fk = True
        load_instance = True
# Instantiate the schemas
user_schema = UserSchema()
goal_schema = GoalSchema()
goals_schema = GoalSchema(many=True)
bill_schema = BillSchema()
bills_schema = BillSchema(many=True)