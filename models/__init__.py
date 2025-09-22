"""
Database initialization module for the Quiz API.

This module sets up SQLAlchemy and provides the database instance
that will be used across all models.
"""
from flask_sqlalchemy import SQLAlchemy

# Initialize the database instance
db = SQLAlchemy()

# Import all models to ensure they're registered with SQLAlchemy
from .quiz import Quiz
from .question import Question  
from .answer import Answer

# Make models available when importing from models package
__all__ = ['db', 'Quiz', 'Question', 'Answer']
