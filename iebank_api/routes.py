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
@app.route('/register', methods=['POST'])
def register():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate input data
        if not username or not email or not password or not confirm_password:
            return jsonify({"error": "All fields are required."}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "An account with this email already exists. Please use a different email or log in."}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400

        # Create and save the new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        # Create a new default account for the user
        new_account = Account(name="Default Account", currency="EUR", country="Spain", user_id=new_user.id)
        db.session.add(new_account)
        db.session.commit()

        return jsonify({"message": "Registration successful! Please log in."}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error during registration:", e)  # Debugging line
        return jsonify({"error": "An error occurred while registering. Please try again."}), 500
    

# Route for user 

@app.route('/login', methods=['POST'])
def login():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Check if the user exists
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            print("Is Authenticated after login:", current_user.is_authenticated)
            print("Current User ID after login:", current_user.get_id() if current_user.is_authenticated else "None")

            # Return JSON response for the frontend
            if user.admin:
                return jsonify({"message": "Login successful", "redirect": "admin"}), 200
            else:
                return jsonify({"message": "Login successful", "redirect": "dashboard"}), 200
        else:
            return jsonify({"error": "Invalid username or password"}), 401
    except Exception as e:
        print(f"Login Error: {e}")
        return jsonify({"error": "An error occurred during login"}), 500

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    print("Logout route accessed.")  # Debug print
    print(f"Current user: {current_user}")  # Check who is logging out
    try:
        logout_user()
        print("User logged out successfully.")  # Confirm user logout
        flash('You have been logged out.', 'info')
        return jsonify({"message": "Logout successful"}), 200
    except Exception as e:
        print(f"Error during logout: {e}")  # Print any errors
        return jsonify({"error": "Logout failed"}), 500

# Route for creating a new accounts
@app.route('/create_account', methods=['GET', 'POST'])
@login_required
def create_account():
    if request.method == 'POST':
        try:
            account_name = request.form.get('account_name')
            currency = request.form.get('currency')
            country = request.form.get('country')
            # Create a new account for the logged-in user
            new_account = Account(name=account_name, currency=currency, country=country, user_id=current_user.id)
            db.session.add(new_account)
            db.session.commit()
            flash('New account created successfully.', 'success')
            return redirect(url_for('dashboard'))
        except SQLAlchemyError as e:
            db.session.rollback()
            flash('An error occurred while creating the account. Please try again.', 'danger')
            return redirect(url_for('create_account'))
    return render_template('create_account.html')

# Route for user dashboard
@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    try:
        if current_user.admin:  # Check if the user is an admin
            return jsonify({
                "username": current_user.username,
                "is_admin": True,
                "accounts": [],
                "transactions": [],
                "message": "Admin users do not have associated accounts or transactions."
            }), 200

        # Fetch accounts for the current user
        user_accounts = Account.query.filter_by(user_id=current_user.id).all()
        print(f"User ID: {current_user.id}, User Accounts: {user_accounts}")

        if not user_accounts:
            return jsonify({
                "username": current_user.username,
                "is_admin": False,
                "accounts": [],
                "transactions": [],
                "message": "No accounts found for this user."
            }), 200

        # Fetch transactions where the user is either the sender or recipient
        user_account_ids = [account.id for account in user_accounts]
        transactions = Transaction.query.filter(
            (Transaction.account_id.in_(user_account_ids)) |
            (Transaction.sent_account_id.in_(user_account_ids))
        ).order_by(Transaction.created_at.desc()).all()

        # Build response data
        accounts_data = [
            {
                "id": account.id,
                "name": account.name,
                "account_number": account.account_number,
                "balance": account.balance,
                "currency": account.currency,
            }
            for account in user_accounts
        ]

        transactions_data = [
            {
                "id": transaction.id,
                "created_at": transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "transaction_type": transaction.transaction_type.value,
                "account_id": transaction.account_id,
                "sent_account_id": transaction.sent_account_id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "description": transaction.description,
            }
            for transaction in transactions
        ]

        return jsonify({
            "username": current_user.username,
            "is_admin": False,
            "accounts": accounts_data,
            "transactions": transactions_data,
        }), 200

    except SQLAlchemyError as e:
        print("Error:", e)
        return jsonify({"error": "An error occurred while loading your dashboard."}), 500


# Route for viewing user transactions
@app.route('/transactions', methods=['GET'])
@login_required
def view_transactions():
    try:
        # Get the IDs of the user's accounts
        user_account_ids = [account.id for account in current_user.accounts]

        # Fetch transactions where the user is either the sender or recipient
        transactions = Transaction.query.filter(
            (Transaction.account_id.in_(user_account_ids)) |
            (Transaction.sent_account_id.in_(user_account_ids))
        ).order_by(Transaction.created_at.desc()).all()

        # Structure the transactions into JSON format
        transactions_data = [
            {
                "id": transaction.id,
                "created_at": transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                "transaction_type": transaction.transaction_type.value,
                "account_id": transaction.account_id,
                "sent_account_id": transaction.sent_account_id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                "description": transaction.description,
            }
            for transaction in transactions
        ]

        return jsonify({"transactions": transactions_data}), 200

    except Exception as e:
        print(f"Error fetching transactions: {e}")
        return jsonify({"error": "An error occurred while fetching transactions."}), 500

# Route for initiating a transfer

@app.route('/transfer', methods=['POST'])
@login_required
def transfer():
    try:
        # Parse JSON data from the request
        data = request.get_json()
        from_account_id = data.get('from_account_id')
        to_account_number = data.get('to_account_number')
        amount = float(data.get('amount'))

        # Fetch the accounts involved in the transaction
        from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
        to_account = Account.query.filter_by(account_number=to_account_number).first()

        # Debug statements
        print(f"From Account Query Result: {from_account}")
        print(f"To Account Query Result: {to_account}")

        if not from_account or not to_account:
            return jsonify({"error": "Invalid account details."}), 400

        if from_account.balance < amount:
            return jsonify({"error": "Insufficient balance."}), 400

        # Perform the transfer
        from_account.balance -= amount
        to_account.balance += amount
        db.session.commit()

        # Log the transaction
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

        return jsonify({"message": "Transfer successful!"}), 200
    except ValueError:
        return jsonify({"error": "Invalid amount entered."}), 400
    except SQLAlchemyError as e:
        db.session.rollback()
        print("Error:", e)  # Debugging line
        return jsonify({"error": "An error occurred during the transfer. Please try again."}), 500


# -------------- Route for Admin-Only  -------------------------------------

# Route for the admin dashboard or landing page

@app.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_portal():
    if request.method == 'POST':
        action = request.json.get('action')  # Accessing JSON data from request
        if action == 'manage_users':
            return jsonify({"redirect": "/admin/users"}), 200
        elif action == 'manage_accounts':
            return jsonify({"redirect": "/dashboard"}), 200
    return jsonify({"message": "Admin portal loaded"}), 200


# 1. Route for listing all users (admin only)
@app.route('/admin/users', methods=['GET'])
@login_required
@admin_required
def list_users():
    try:
        users = User.query.all()
        users_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "admin": user.admin,
                "accounts": [account.account_number for account in user.accounts]  # Add account numbers
            }
            for user in users
        ]
        return jsonify(users=users_data), 200
    except SQLAlchemyError as e:
        print(f"Error fetching users: {e}")  # Debugging statement
        return jsonify({"error": "An error occurred while retrieving user data."}), 500

# 2. Route for creating a new user (admin only)
@app.route('/admin/users/create', methods=['POST'])
@login_required
@admin_required
def create_user():
    try:
        data = request.get_json()  # Ensure JSON data is received
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        admin = data.get('admin', False)

        # Validate the input fields
        if not username or not email or not password or not confirm_password:
            return jsonify({"error": "All fields are required."}), 400

        if password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"error": "A user with this email already exists."}), 400

        # Hash the password and create a new user
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, admin=admin)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully."}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error creating user: {e}")
        return jsonify({"error": "An error occurred while creating the user."}), 500

# get user info for the edit form(admin only)
@app.route('/admin/users/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    try:
        # Return user details in JSON format
        return jsonify({
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "admin": user.admin,
            }
        }), 200
    except SQLAlchemyError as e:
        print(f"Error fetching user data: {e}")
        return jsonify({"error": "An error occurred while fetching user data."}), 500


# Route for updating a user (admin only)
@app.route('/admin/users/<int:user_id>/edit', methods=['PUT'])
@login_required
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    # Ensure JSON payload
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data."}), 400

    # Update user fields
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.admin = data.get('admin', user.admin)

    # Handle password update (if provided)
    if data.get('password'):
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if password != confirm_password:
            return jsonify({"error": "Passwords do not match."}), 400
        user.password = generate_password_hash(password)

    try:
        # Commit changes to the database
        db.session.commit()
        return jsonify({"message": "User updated successfully."}), 200
    except SQLAlchemyError as e:
        # Rollback and return error on failure
        db.session.rollback()
        print(f"Error updating user: {e}")
        return jsonify({"error": "An error occurred while updating the user."}), 500
    

# Route for deleting a user (admin only)
@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    try:
        # Attempt to find the user
        user = User.query.get_or_404(user_id)
        print(f"Attempting to delete user: {user.username}")

        # Delete the user
        db.session.delete(user)
        db.session.commit()
        print("User deleted successfully.")
        return jsonify({"message": "User deleted successfully."}), 200
    except SQLAlchemyError as e:
        print(f"Error deleting user: {e}")  # Print the error to the console
        db.session.rollback()
        return jsonify({"error": "An error occurred while deleting the user."}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Unexpected error occurred. Please try again."}), 500



# -------------- Helps me with errors -----------------------------------------

# Error handlers
@app.errorhandler(403)
def forbidden(e):
    if request.is_json:  # Check if the client expects a JSON response
        return jsonify({"error": "Forbidden: You do not have permission to access this resource."}), 403
    return render_template('403.html'), 403

@app.errorhandler(404)
def not_found(e):
    if request.is_json:
        return jsonify({"error": "Not Found: The requested resource could not be found."}), 404
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    if request.is_json:
        return jsonify({"error": "Server Error: An internal server error occurred."}), 500
    return render_template('500.html'), 500

