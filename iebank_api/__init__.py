from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from applicationinsights.flask.ext import AppInsights
from werkzeug.security import generate_password_hash
import requests

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()

# Configure the environment based on the ENV variable
env = os.getenv('ENV', 'local')  
if env == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '76933d03-6c45-4cff-ae5e-bf66b8388b76'
elif env == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '76933d03-6c45-4cff-ae5e-bf66b8388b76'
elif env == 'ghci':
    print("Running in GitHub CI mode")
    app.config.from_object('config.GithubCIConfig')
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '76933d03-6c45-4cff-ae5e-bf66b8388b76'
elif env == 'uat':
    print("Running in UAT mode")
    app.config.from_object('config.UATConfig')
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '76933d03-6c45-4cff-ae5e-bf66b8388b76'
else:
    print("Running in production, aka local, mode for now!")
    app.config.from_object('config.LocalConfig')
    app.config['APPINSIGHTS_INSTRUMENTATIONKEY'] = '76933d03-6c45-4cff-ae5e-bf66b8388b76'

if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ie_bank.db')

# Set a secret key for session management and Flask-Login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aswin')  

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager.init_app(app)

# Set the login view and messages
login_manager.login_view = 'login'  
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
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "https://your-production-domain.com"}})

# Application Insights configuration
appinsights = AppInsights(app)

@app.after_request
def after_request(response):
    try:
        appinsights.flush()
    except Exception as e:
        app.logger.error(f"Error while flushing Application Insights: {e}")
    app.logger.info(f"{request.method} {request.url} - Status {response.status_code}")
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
        print("Admin user created.")
        
# Import routes to register endpoints
from iebank_api import routes
