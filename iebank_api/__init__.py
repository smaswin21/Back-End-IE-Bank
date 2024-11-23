from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from werkzeug.security import generate_password_hash
from logging import INFO, getLogger
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry.instrumentation.flask import FlaskInstrumentor

# Load environment variables
load_dotenv()

# Initialize Flask App
app = Flask(__name__)
login_manager = LoginManager()

# Configure the environment based on the ENV variable
env = os.getenv('ENV', 'local')
if env == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif env == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif env == 'ghci':
    print("Running in GitHub CI mode")
    app.config.from_object('config.GithubCIConfig')
elif env == 'uat':
    print("Running in UAT mode")
    app.config.from_object('config.UATConfig')
else:
    print("Running in production, aka local, mode for now!")
    app.config.from_object('config.LocalConfig')

# Set a secret key for session management and Flask-Login
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'aswin')

# Application Insights Configuration using Connection String
connection_string = os.getenv("APPINSIGHTS_CONNECTION_STRING")
if connection_string:
    print("Configuring Azure Monitor", connection_string)
    configure_azure_monitor(connection_string=connection_string)
    FlaskInstrumentor().instrument_app(app)

# Configure Azure Monitor Logging
logger = getLogger("my_application_logger")
logger.setLevel(INFO)

# Child logger to demonstrate hierarchy tracking
logger_child = getLogger("my_application_logger.module")
logger_child.setLevel(INFO)
print("Logger name:", logger_child.name)

# Example of logging statements to verify the setup
logger.info("Application started - info log")
logger.warning("Application started - warning log")
logger.error("Application started - error log")

# Logger that will not be tracked by Azure Monitor
logger_not_tracked = getLogger("not_my_application_logger")
logger_not_tracked.setLevel(INFO)

logger_not_tracked.info("Info log - will not be tracked")
logger_not_tracked.warning("Warning log - will not be tracked")
logger_not_tracked.error("Error log - will not be tracked")

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
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})

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
