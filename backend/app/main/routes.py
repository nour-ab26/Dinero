from app.main import bp
from flask import render_template, flash, redirect, url_for
from app.main.forms import LoginForm, RegistrationForm, OnboardingForm, CreateGoalForm, AddToGoalForm
from app.models import User, Goal
from app import db
from flask_login import current_user, login_user, logout_user, login_required

@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html', title='Home')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print("Login attempt:", form.email.data, "Found:", user is not None)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('main.login'))
        login_user(user)
        return redirect(url_for('main.dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.login'))
    return render_template('signup.html', title='Sign Up', form=form)

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = OnboardingForm()
    if not current_user.onboarding_complete and form.validate_on_submit():
        current_user.gender = form.gender.data
        current_user.job_title = form.job_title.data
        current_user.monthly_income = form.monthly_income.data
        current_user.tracking_period = form.tracking_period.data
        current_user.main_goal = form.main_goal.data
        current_user.onboarding_complete = True
        db.session.commit()
        flash('Your profile has been updated!')
        return redirect(url_for('main.dashboard'))
    
    return render_template('dashboard.html', title='Dashboard', form=form)

@bp.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    create_form = CreateGoalForm()
    add_form = AddToGoalForm()

    # Handle the "Create Goal" form submission
    if create_form.submit_create_goal.data and create_form.validate_on_submit():
        new_goal = Goal(
            name=create_form.name.data,
            target_amount=create_form.target_amount.data,
            author=current_user
        )
        db.session.add(new_goal)
        db.session.commit()
        flash('Your new goal has been created!')
        return redirect(url_for('main.goals'))

    # Handle the "Add to Goal" form submission
    if add_form.submit_add_to_goal.data and add_form.validate_on_submit():
        goal = Goal.query.filter_by(id=add_form.goal_id.data, user_id=current_user.id).first_or_404()
        goal.current_amount += add_form.amount.data
        db.session.commit()
        flash(f'Successfully added to your goal: {goal.name}!')
        return redirect(url_for('main.goals'))

    user_goals = Goal.query.filter_by(author=current_user).order_by(Goal.id.asc()).all()
    return render_template(
        'goals.html',
        title='Goals',
        user_goals=user_goals,
        create_form=create_form,
        add_form=add_form
    )