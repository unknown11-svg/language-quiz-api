"""
Routes package initialization for the Language Learning Quiz API.

This module provides centralized access to all route blueprints
and sets up the URL structure for the API.
"""

from .quiz_routes import quiz_bp
from .quiz_session_routes import session_bp

# Make blueprints available when importing from routes package
__all__ = ['quiz_bp', 'session_bp']

def register_blueprints(app):
    """
    Register all blueprints with the Flask application.
    
    Args:
        app (Flask): The Flask application instance
    """
    app.register_blueprint(quiz_bp)
    app.register_blueprint(session_bp)

def get_api_info():
    """
    Get information about the API structure and available endpoints.
    
    Returns:
        dict: API structure information
    """
    return {
        "api_version": "v1",
        "base_url": "/api/v1",
        "endpoints": {
            "quiz_management": {
                "base_path": "/api/v1/quizzes",
                "description": "Endpoints for managing quizzes (educators)",
                "methods": {
                    "POST /api/v1/quizzes": "Create a new quiz",
                    "GET /api/v1/quizzes": "Get all quizzes (with pagination/filtering)",
                    "GET /api/v1/quizzes/{id}": "Get a specific quiz",
                    "PUT /api/v1/quizzes/{id}": "Update a quiz",
                    "DELETE /api/v1/quizzes/{id}": "Delete a quiz",
                    "GET /api/v1/quizzes/categories": "Get available categories",
                    "GET /api/v1/quizzes/difficulty-levels": "Get difficulty levels"
                }
            },
            "quiz_sessions": {
                "base_path": "/api/v1/quiz-sessions", 
                "description": "Endpoints for taking quizzes (students)",
                "methods": {
                    "POST /api/v1/quiz-sessions/start/{id}": "Start a quiz session",
                    "POST /api/v1/quiz-sessions/submit/{id}": "Submit quiz answers",
                    "GET /api/v1/quiz-sessions/preview/{id}": "Preview a quiz",
                    "GET /api/v1/quiz-sessions/stats/{id}": "Get quiz statistics",
                    "POST /api/v1/quiz-sessions/validate-answers": "Validate answer format",
                    "POST /api/v1/quiz-sessions/time-check/{id}": "Check remaining time"
                }
            }
        },
        "authentication": {
            "note": "Currently using optional headers for user identification",
            "headers": {
                "X-User-ID": "Educator/admin identifier (optional)",
                "X-Student-ID": "Student identifier (optional)"
            }
        },
        "response_format": {
            "success": {
                "success": True,
                "message": "Success message",
                "data": "Response data"
            },
            "error": {
                "success": False,
                "message": "Error message", 
                "error": "Error details (optional)"
            }
        }
    }
