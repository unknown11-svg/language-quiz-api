"""
Controllers package initialization for the Language Learning Quiz API.

This module provides centralized access to all controller classes
and common functionality.
"""

from .base_controller import BaseController
from .quiz_controller import QuizController  
from .quiz_session_controller import QuizSessionController

# Make controllers available when importing from controllers package
__all__ = [
    'BaseController',
    'QuizController', 
    'QuizSessionController'
]

# You can add package-level functions or constants here if needed
# For example:

# Default pagination settings
DEFAULT_PAGE_SIZE = 10
MAX_PAGE_SIZE = 100

# Common validation patterns
DIFFICULTY_LEVELS = ['beginner', 'intermediate', 'advanced']
QUESTION_TYPES = ['multiple_choice', 'true_false', 'fill_blank']

def get_controller_info():
    """
    Get information about available controllers.
    
    Returns:
        dict: Information about controllers and their methods
    """
    return {
        'QuizController': {
            'description': 'Handles quiz CRUD operations and management',
            'methods': ['create_quiz', 'get_quiz', 'get_all_quizzes', 'update_quiz', 'delete_quiz']
        },
        'QuizSessionController': {
            'description': 'Manages quiz sessions, submissions, and scoring',
            'methods': ['start_quiz_session', 'submit_quiz', 'get_quiz_statistics']
        },
        'BaseController': {
            'description': 'Provides common functionality for all controllers',
            'methods': ['success_response', 'error_response', 'validation_error_response']
        }
    }
