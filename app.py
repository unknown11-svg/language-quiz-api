"""
Main application entry point for the Language Learning Quiz API.

This file creates and runs the Flask application using the application factory pattern.
"""
import os
from flask import jsonify
from __init__ import create_app
from routes import get_api_info

# Determine configuration based on environment
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

@app.route('/')
def index():
    """
    Root endpoint providing API information and welcome message.
    
    Returns:
        JSON: API information and available endpoints
    """
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

@app.route('/health')
def health_check():
    """
    Health check endpoint for monitoring and deployment.
    
    Returns:
        JSON: Health status information
    """
    return jsonify({
        "status": "healthy",
        "service": "Language Learning Quiz API",
        "version": "1.0.0",
        "environment": config_name
    })

@app.errorhandler(404)
def not_found(error):
    """Global 404 error handler."""
    return jsonify({
        "success": False,
        "message": "Endpoint not found",
        "error": "The requested URL was not found on the server"
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """Global 405 error handler."""
    return jsonify({
        "success": False,
        "message": "Method not allowed",
        "error": "The method is not allowed for the requested URL"
    }), 405

@app.errorhandler(500)
def internal_error(error):
    """Global 500 error handler."""
    return jsonify({
        "success": False,
        "message": "Internal server error",
        "error": "An unexpected error occurred"
    }), 500

if __name__ == '__main__':
    # Only run directly if this file is executed (not imported)
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'True').lower() == 'true'
    
    print(f"🚀 Starting Language Learning Quiz API...")
    print(f"📊 Environment: {config_name}")
    print(f"🌐 Port: {port}")
    print(f"🔧 Debug mode: {debug}")
    print(f"📚 API Documentation: http://localhost:{port}/")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )