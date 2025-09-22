"""
Routes package initialization for the Language Learning Quiz API.

This module provides centralized access to all route blueprints
and sets up the URL structure for the API.
"""

from .quiz_routes import quiz_bp
from .quiz_session_routes import session_bp
from .basic_routes import basic_bp, get_api_info

# Make blueprints available when importing from routes package
__all__ = ['quiz_bp', 'session_bp', 'basic_bp', 'get_api_info']

def register_blueprints(app):
    """
    Register all blueprints with the Flask application.
    
    Args:
        app (Flask): The Flask application instance
    """
    app.register_blueprint(basic_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(session_bp)
