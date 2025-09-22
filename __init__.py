from flask import Flask
from flask_cors import CORS
from config import config

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
    from models import db  # Import the shared db instance
    db.init_app(app)
    CORS(app)  # Enable CORS for frontend integration
    
    # Import and initialize models (this registers them with SQLAlchemy)
    from models import Quiz, Question, Answer  # This ensures models are registered
    
    # Register blueprints
    from routes import register_blueprints
    register_blueprints(app)
    
    # Create tables (only if not testing with in-memory DB)
    if config_name != 'testing':
        with app.app_context():
            db.create_all()
    
    return app