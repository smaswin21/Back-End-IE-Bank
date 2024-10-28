""" 
Routes.py : User, Accounts & Transactions
"""
from flask import Flask, request, jsonify, abort, render_template
from flask_login import login_user, logout_user, login_required, current_user
from iebank_api import db, app, login_manager
from iebank_api.models import User, Account, Transaction, TransactionType
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from sqlalchemy import or_

@app.route('/')
def hello_world():
    return render_template('index.html')

# ---------- Admin Access Decorator ----------
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            return jsonify({'message': 'Admin access required'}), 403
        return fn(*args, **kwargs)
    return wrapper

# ---------- User Loader ----------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ---------- Authentication Routes ----------

# Register an User
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Hash the password
    hashed_password = generate_password_hash(password)
    
    # Create new user
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

# Login with User
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print("Data received in login:", data)

    email = data.get('email')
    password = data.get('password')
    print("Email received:", email)  # Debugging statement
    print("Password received:", password)  # Debugging statement

    # Find user by email
    user = User.query.filter_by(email=email).first()
    print("User found:", user)  # Debugging statement

    if user and check_password_hash(user.password, password) and user.status == "Active":
        login_user(user, remember=True)
        print("Login successful")  # Debugging statement
        return jsonify({'message': 'Login successful', 'is_admin': user.admin}), 200

    print("Login failed")  # Debugging statement
    return jsonify({'message': 'Invalid credentials'}), 401


# Logout with User
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200


# ---------- Admin User Management Routes ----------
@app.route('/users', methods=['GET'])
@admin_required
def get_users():
    users = User.query.all()
    return {'users': [format_user(user) for user in users if user.status == "Active"]}

@app.route('/users', methods=['POST'])
@admin_required
def create_user():
    data = request.json
    username = data['username']
    email = data['email']
    password = generate_password_hash(data['password'])
    admin = data['admin']
    
    new_user = User(username=username, email=email, password=password, admin=admin)
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/users/<int:id>', methods=['PUT'])
@admin_required
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.json
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    user.admin = data.get('admin', user.admin)
    
    db.session.commit()
    return format_user(user), 200

@app.route('/users/<int:id>', methods=['DELETE'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    user.status = "Inactive"
    db.session.commit()
    return jsonify({'message': 'User deactivated successfully'}), 204


# ---------- Account Management Routes ----------

@app.route('/accounts', methods=['POST'])
@login_required
def create_account():
    data = request.json
    name = data['name']
    currency = data['currency']
    country = data['country']
    
    # Create an account associated with the current user
    account = Account(name=name, currency=currency, country=country, user=current_user)
    db.session.add(account)
    db.session.commit()

    return format_account(account), 201

@app.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    # Admin sees all accounts, users see only their own
    if current_user.admin:
        accounts = Account.query.all()
    else:
        accounts = current_user.accounts

    return {'accounts': [format_account(account) for account in accounts if account.status == "Active"]}


@app.route('/accounts/<int:id>', methods=['GET'])
@login_required
def get_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id and not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403
    return format_account(account)

@app.route('/accounts/<int:id>', methods=['PUT'])
@login_required
def update_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id and not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    account.name = request.json.get('name', account.name)
    db.session.commit()
    return format_account(account), 200

@app.route('/accounts/<int:id>', methods=['DELETE'])
@login_required
def delete_account(id):
    account = Account.query.get_or_404(id)
    if account.user_id != current_user.id and not current_user.admin:
        return jsonify({'message': 'Unauthorized access'}), 403

    account.status = "Inactive"
    db.session.commit()
    return jsonify({'message': 'Account deactivated'}), 204

# ---------- Transfer Money Route ----------

@app.route('/transfer', methods=['POST'])
@login_required
def transfer_money():
    
    data = request.json
    
    try:
        source_account_id = data.get('source_account_id')
        
        destination_account_number = data.get('destination_account_number')
        
        amount = float(data.get('amount'))
        
        # Error Handling
        source_account = Account.query.get_or_404(source_account_id)
        destination_account = Account.query.filter_by(account_number=destination_account_number).first()
        
        if not destination_account:
            return jsonify({'message': 'Destination account not found'}), 404

        if source_account.user_id != current_user.id:
            return jsonify({'message': 'Unauthorized transaction'}), 403

        if source_account.balance < amount:
            return jsonify({'message': 'Insufficient funds'}), 400
        
        # Perform the transfer
        source_account.balance -= amount
        destination_account.balance += amount

        # Record transaction
        transaction = Transaction(
            amount=amount,
            currency=source_account.currency,
            account_id=source_account.id,
            sent_account_id=destination_account.id,
            transaction_type=TransactionType.TRANSFER
        )
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({'message': f'Transferred {amount} successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
        
# ---------- Helper Functions ----------------


def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'country': account.country,
        'status': account.status,
        'created_at': account.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'user_id': account.user_id
    }

def format_user(user):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'admin': user.admin,
        'status': user.status
    }

def format_transaction(transaction):
    return {
        'id': transaction.id,
        'amount': transaction.amount,
        'currency': transaction.currency,
        'created_at': transaction.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'account_id': transaction.account_id,
        'sent_account_id': transaction.sent_account_id
    }