from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='default'):
    """
    Application factory pattern for creating Flask app instances.
    
    Args:
        config_name (str): The configuration to use ('development', 'production', 'testing')
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    CORS(app)  # Enable CORS for frontend integration
    
    # Import and initialize models
    from models import db as models_db, init_db, create_tables
    init_db(app)
    
    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)
    
    # Create tables
    with app.app_context():
        create_tables(app)
    
    return app