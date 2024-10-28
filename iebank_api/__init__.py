from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from applicationinsights.flask.ext import AppInsights

load_dotenv()

app = Flask(__name__)
login_manager = LoginManager()

# Select environment based on the ENV environment variable
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
    print("Running in production mode")
    app.config.from_object('config.LocalConfig')

# Ensure SQLAlchemy is configured with a database URI
if not app.config.get('SQLALCHEMY_DATABASE_URI'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ie_bank.db')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import the models to ensure they are registered
from iebank_api.models import Account, User

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()
    
    # Create an Admin user
    admin = User.query.filter_by(username="admin").first()
    if not admin:
        admin = User("admin", "admin@example.com", "admin_password", True)
        db.session.add(admin)
        db.session.commit()
    
    login_manager.login_view = '/login'
    login_manager.init_app(app)

# Handle unauthorized access
@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({"error": "Unauthorized", "message": "Authentication required"}), 401

# Enable (CORS)
CORS(app, supports_credentials=True, samesite="None")

appinsights = AppInsights(app)

@app.after_request
def after_request(response):
    appinsights.flush() 
    return response

# Import routes to register endpoints
from iebank_api import routes
