from iebank_api import db
from datetime import datetime, timezone
import string
import random
import enum
from flask_login import UserMixin

# -------------- USER REGISTRATION & LOGIN ------------------

class User(db.Model, UserMixin):
    """
    User Model
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)  # Increase length for secure hash
    created_at = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    admin = db.Column(db.Boolean, nullable=False, default=False)
    status = db.Column(db.String(10), nullable=False, default="Active")
    
    # Relationship with Account
    accounts = db.relationship('Account', backref='user', lazy=True)
    # Relationship with Transaction 
    transactions = db.relationship('Transaction', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def __init__(self, username, email, password, admin=False):
        self.username = username
        self.email = email
        self.password = password  # Make sure to hash the password before storing
        self.admin = admin
        self.status = "Active"
    
    def deactivate(self):
        """
        Deactivates the user account by setting the status to 'Inactive'.
        """
        self.status = "Inactive"
        return self.status

    def get_id(self):
        return str(self.id)  # Ensure ID is returned as a string


# -------------- BANK ACCOUNT SYSTEM---------------------------------------

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(3), nullable=False, default="€")
    country = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(10), nullable=False, default="Active")
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Foreign key to User
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Account {self.account_number}>'
  
    def deactivate(self):
        self.status = "Inactive"
        return self.status
    
    def __init__(self, name, currency, country, user_id, balance=0.0):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.country = country
        self.balance = balance
        self.status = "Active"
        self.user_id = user_id


class TransactionType(enum.Enum):
    DEPOSIT = 'deposit'
    WITHDRAW = 'withdraw'
    TRANSFER = 'transfer'


# -------------- TRANSACTION SYSTEM---------------------------------------

class Transaction(db.Model):
    """
    Transaction model
    """
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    sent_account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=True)
    transaction_type = db.Column(db.Enum(TransactionType), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False, default="€")
    description = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Define relationships
    account = db.relationship('Account', foreign_keys=[account_id], backref='transactions')
    destination_account = db.relationship('Account', foreign_keys=[sent_account_id], backref='received_transactions')

    def __repr__(self):
        return f'<Transaction {self.id}: {self.transaction_type.value} {self.amount} {self.currency} from Account {self.account_id} to Account {self.sent_account_id}>'

    def __init__(self, amount, currency, account_id, transaction_type, sent_account_id=None, user_id=None, description=None):
        self.amount = amount
        self.currency = currency
        self.account_id = account_id
        self.transaction_type = transaction_type
        self.sent_account_id = sent_account_id
        self.description = description
        self.user_id = user_id
