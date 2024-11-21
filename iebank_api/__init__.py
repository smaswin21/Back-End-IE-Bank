from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from applicationinsights.flask.ext import AppInsights
from werkzeug.security import generate_password_hash

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()

# Configure the environment based on the ENV variable
if os.getenv('ENV') == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif os.getenv('ENV') == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif os.getenv('ENV') == 'ghci':
    print("Running in GitHub CI mode")
    app.config.from_object('config.GithubCIConfig')
elif os.getenv('ENV') == 'uat':
    print("Running in UAT mode")
    app.config.from_object('config.UATConfig')  
else:
    print("Running in production, aka local, mode for now!")
    app.config.from_object('config.LocalConfig')

if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ie_bank.db')

# Set a secret key for session management and Flask-Login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aswin')  

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

# Set the login view and messages
login_manager.login_view = 'login'  # Ensure this matches the route in routes.py
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Unauthorized handler for JSON response
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# Application Insights configuration
appinsights = AppInsights(app)

@app.after_request
def after_request(response):
    appinsights.flush() 
    return response

# Import models to register them with SQLAlchemy
from iebank_api.models import Account, User, TransactionType, Transaction

# Initialize database and create tables if they don't exist
with app.app_context():
    db.create_all()
    # Create an admin user if none exists
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User("admin", "admin@example.com", generate_password_hash("admin_password"), True)
        db.session.add(admin)
        db.session.commit()

# Import routes to register endpoints
from iebank_api import routes

