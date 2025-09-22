"""
Database initialization module for the Quiz API.

This module sets up SQLAlchemy and provides the database instance
that will be used across all models.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

def init_db(app):
    """
    Initialize the database with the Flask application.
    
    Args:
        app (Flask): The Flask application instance
    """
    db.init_app(app)
    
def create_tables(app):
    """
    Create all database tables.
    
    Args:
        app (Flask): The Flask application instance
    """
    with app.app_context():
        db.create_all()

# Import all models to ensure they're registered with SQLAlchemy
from .quiz import Quiz
from .question import Question  
from .answer import Answer

# Make models available when importing from models package
__all__ = ['db', 'Quiz', 'Question', 'Answer', 'init_db', 'create_tables']
