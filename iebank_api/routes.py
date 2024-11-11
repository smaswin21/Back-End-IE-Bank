from flask import Flask, request, jsonify, abort, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, LoginManager
from iebank_api import db, app
from iebank_api.models import User, Account, Transaction, TransactionType
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy.exc import SQLAlchemyError


# -------------- BANK ACCOUNT SYSTEM---------------------------------------


# -------------- Login Manager --------------------------------------------


# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------------- Home Route - index.html ----------------------------------

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Utility function to check if user is admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

# -------------- Route for Users ----------------------------------

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            # Check if any of the fields are empty
            if not (username and email and password):
                flash('Please fill in all fields.', 'danger')
                return redirect(url_for('register'))

            confirm_password = request.form.get('confirm_password')

            if User.query.filter_by(email=email).first():
                flash('An account with this email already exists. Please use a different email or log in.', 'danger')
                return redirect(url_for('register'))

            if password != confirm_password:
                flash('Passwords do not match!', 'danger')
                return redirect(url_for('register'))

            hashed_password = generate_password_hash(password) # hash type: scrypt:32768:8:1
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))

        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while registering. Please try again.', 'danger')
            return redirect(url_for('register'))

    return render_template('register.html')

# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            # Debug statements
            print("Is Authenticated after login:", current_user.is_authenticated)
            print("Current User ID after login:", current_user.get_id() if current_user.is_authenticated else "None")

            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route for user dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Debug statements
    print("Is Authenticated in /dashboard:", current_user.is_authenticated)
    print("Current User ID in /dashboard:", current_user.get_id() if current_user.is_authenticated else "None")

    try:
        user_accounts = Account.query.filter_by(user_id=current_user.id).all()
        return render_template('dashboard.html', accounts=user_accounts)
    except SQLAlchemyError:
        flash('An error occurred while loading your dashboard.', 'danger')
        return redirect(url_for('login'))

@app.route('/accounts', methods=['GET'])
@login_required
def view_accounts():
    # Debug statements
    print("Is Authenticated in /accounts:", current_user.is_authenticated)
    print("Current User ID in /accounts:", current_user.get_id() if current_user.is_authenticated else "None")

    try:

        user_accounts = Account.query.filter_by(user_id=current_user.id).all()
        print(f"The user is {user_accounts}")
        return render_template('accounts.html', accounts=user_accounts)
    except SQLAlchemyError:
        flash('An error occurred while retrieving accounts.', 'danger')
        return redirect(url_for('dashboard'))

# Route for initiating a transfer
@app.route('/transfer', methods=['GET', 'POST'])
@login_required
def transfer():
    if request.method == 'POST':
        try:
            from_account_id = request.form.get('from_account_id')
            to_account_number = request.form.get('to_account_number')
            amount = float(request.form.get('amount'))

            from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
            print("From Account:", from_account)  # Debugging line
            to_account = Account.query.filter_by(account_number=to_account_number).first()
            print("To Account:", to_account)  # Debugging line

            if not from_account or not to_account:
                flash('Invalid account details.', 'danger')
                return redirect(url_for('dashboard'))

            if from_account.balance < amount:
                flash('Insufficient balance.', 'danger')
                return redirect(url_for('dashboard'))

            from_account.balance -= amount
            to_account.balance += amount

            transaction = Transaction(
                amount=amount,
                currency=from_account.currency,
                account_id=from_account.id,
                transaction_type=TransactionType.TRANSFER,
                sent_account_id=to_account.id,
                user_id=current_user.id,
                description=f'Transfer to {to_account_number}'
            )
            db.session.add(transaction)
            db.session.commit()
            flash('Transfer successful!', 'success')
            return redirect(url_for('dashboard'))

        except ValueError:
            flash('Invalid amount entered.', 'danger')
            return redirect(url_for('transfer'))
        except SQLAlchemyError as e:
            db.session.rollback()
            print("Error:", e)  # Debugging line
            flash('An error occurred during the transfer. Please try again.', 'danger')
            return redirect(url_for('dashboard'))

    try:
        user_accounts = Account.query.filter_by(user_id=current_user.id).all()
        print("User Accounts:", user_accounts)  # Debugging line
        return render_template('transfer.html', accounts=user_accounts)
    except SQLAlchemyError as e:
        print("Error:", e)  # Debugging line
        flash('An error occurred while loading transfer data.', 'danger')
        return redirect(url_for('dashboard'))


# -------------- Route for Admin-Only  -------------------------------------

# Route for the admin dashboard or landing page
@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    return redirect(url_for('list_users'))

# 1. Route for listing all users (admin only)
@app.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    try:
        users = User.query.all()
        return render_template('admin_users.html', users=users)
    except SQLAlchemyError:
        flash('An error occurred while retrieving user data.', 'danger')
        return redirect(url_for('dashboard'))

# 2. Route for creating a new user (admin only)
@app.route('/admin/users', methods=['POST'])
@login_required
@admin_required
def create_user():
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    admin = request.form.get('admin') == 'on'  # Note the change here from is_admin to admin

    if password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('list_users'))

    hashed_password = generate_password_hash(password)

    try:
        # Pass admin instead of is_admin
        new_user = User(username=username, email=email, password=hashed_password, admin=admin)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while creating the user.', 'danger')

    return redirect(url_for('list_users'))

# Route for updating a user (admin only)
@app.route('/admin/users/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    user.username = request.form.get('username', user.username)
    user.email = request.form.get('email', user.email)
    user.admin = request.form.get('admin') == 'on'

    if request.form.get('password'):
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password == confirm_password:
            user.password = generate_password_hash(password)
        else:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('list_users'))

    try:
        db.session.commit()
        flash('User updated successfully!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while updating the user.', 'danger')

    return redirect(url_for('list_users'))

# Route for deleting a user (admin only)
@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except SQLAlchemyError:
        db.session.rollback()
        flash('An error occurred while deleting the user.', 'danger')

    return redirect(url_for('list_users'))


# -------------- Helps me with errors -----------------------------------------

# Error handlers
@app.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500
