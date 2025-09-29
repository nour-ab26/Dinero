from flask import request, jsonify, render_template, redirect, url_for, flash
from app.main import bp
from app.main.forms import RegistrationForm, LoginForm, OnboardingForm, CreateGoalForm, AddToGoalForm
from app.models import User, Goal, Bill
from app import db
from app.schemas import user_schema, goal_schema, goals_schema, bill_schema, bills_schema
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_required, current_user, login_user, logout_user

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user:
        return jsonify({"msg": "Email already exists"}), 400

    user = User(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    
    return jsonify({"msg": "User created successfully"}), 201





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
    
    
@bp.route('/bills', methods=['GET'])
@jwt_required()
def get_bills():
    """Get all bills for the current user."""
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    # Order by due date so the most urgent are first
    user_bills = user.bills.order_by(Bill.due_date.asc()).all()
    return jsonify(bills_schema.dump(user_bills))

@bp.route('/bills', methods=['POST'])
@jwt_required()
def create_bill():
    """Create a new bill."""
    current_user_id = get_jwt_identity()
    data = request.get_json()

    try:
        new_bill = bill_schema.load(data)
    except Exception as e:
        return jsonify({"errors": str(e)}), 400

    new_bill.user_id = current_user_id
    db.session.add(new_bill)
    db.session.commit()
    
    return jsonify(bill_schema.dump(new_bill)), 201

@bp.route('/bills/<int:bill_id>/pay', methods=['PUT'])
@jwt_required()
def pay_bill(bill_id):
    """Mark a specific bill as paid."""
    current_user_id = get_jwt_identity()
    bill = Bill.query.filter_by(id=bill_id, user_id=current_user_id).first_or_404()

    if bill.is_paid:
        return jsonify({"msg": "Bill is already paid."}), 400

    bill.is_paid = True
    db.session.commit()

    return jsonify(bill_schema.dump(bill))

@bp.route('/bills/<int:bill_id>', methods=['DELETE'])
@jwt_required()
def delete_bill(bill_id):
    """Delete a specific bill."""
    current_user_id = get_jwt_identity()
    bill = Bill.query.filter_by(id=bill_id, user_id=current_user_id).first_or_404()
    
    db.session.delete(bill)
    db.session.commit()
    
    return '', 204 # 204 No Content is standard for a successful DELETE