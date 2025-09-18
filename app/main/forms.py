from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, DecimalField, TextAreaField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional, NumberRange
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class OnboardingForm(FlaskForm):
    gender = SelectField('Gender', choices=[('', 'Select...'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Prefer not to say', 'Prefer not to say')], validators=[DataRequired()])
    job_title = StringField('Job Title', validators=[DataRequired()])
    monthly_income = DecimalField('Income', places=2, validators=[DataRequired(message="Please enter your estimated monthly income.")])
    tracking_period = SelectField('Tracking Per', choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly')], validators=[DataRequired()])
    main_goal = TextAreaField('Goal of using the app', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class CreateGoalForm(FlaskForm):
    name = StringField('What is your goal', validators=[DataRequired()])
    target_amount = DecimalField('Amount needed', places=2, validators=[
        DataRequired(), NumberRange(min=1, message="Amount must be positive.")
    ])
    submit_create_goal = SubmitField('Submit')


class AddToGoalForm(FlaskForm):
    amount = DecimalField('Amount', places=2, validators=[
        DataRequired(), NumberRange(min=0.01, message="Amount must be positive.")
    ])
    goal_id = HiddenField() # This will be set by JavaScript
    submit_add_to_goal = SubmitField('Submit')