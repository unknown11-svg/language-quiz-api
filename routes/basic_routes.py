"""
Basic routes for the Language Learning Quiz API.

This module contains general API endpoints like health checks,
root endpoint, and error handlers.
"""
from flask import Blueprint, jsonify
import os

# Create blueprint for basic routes
basic_bp = Blueprint('basic', __name__)

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

@basic_bp.route('/')
def index():
    """
    Root endpoint providing API information and welcome message.
    
    Returns:
        JSON: API information and available endpoints
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    return jsonify({
        "message": "Welcome to the Language Learning Quiz API! 🎓",
        "description": "A comprehensive quiz engine for language learning platforms",
        "version": "1.0.0",
        "api_info": get_api_info(),
        "health": "OK",
        "documentation": {
            "note": "This API provides endpoints for creating and taking language learning quizzes",
            "features": [
                "Quiz creation and management for educators",
                "Student quiz-taking with real-time feedback", 
                "Multiple question types and difficulty levels",
                "Time limits and performance tracking",
                "Detailed scoring and explanations"
            ]
        }
    })

@basic_bp.route('/health')
def health_check():
    """
    Health check endpoint for monitoring and deployment.
    
    Returns:
        JSON: Health status information
    """
    config_name = os.getenv('FLASK_ENV', 'development')
    return jsonify({
        "status": "healthy",
        "service": "Language Learning Quiz API",
        "version": "1.0.0",
        "environment": config_name
    })

@basic_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors for this blueprint."""
    return jsonify({
        "success": False,
        "error": "Not found",
        "message": "The requested resource was not found",
        "available_endpoints": get_api_info()
    }), 404

@basic_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for this blueprint."""
    return jsonify({
        "success": False,
        "error": "Internal server error",
        "message": "An unexpected error occurred"
    }), 500