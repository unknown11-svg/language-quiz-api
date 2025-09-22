"""
Quiz management routes for the Language Learning Quiz API.

This module defines HTTP endpoints for quiz CRUD operations.
These routes are used by educators and administrators to manage quizzes.
"""
from flask import Blueprint, request
from controllers import QuizController

# Create the quiz blueprint
quiz_bp = Blueprint('quiz', __name__, url_prefix='/api/v1/quizzes')

@quiz_bp.route('', methods=['POST'])
def create_quiz():
    """
    Create a new quiz.
    
    Expected JSON payload:
    {
        "title": "Spanish Grammar Quiz",
        "description": "Test your Spanish grammar skills",
        "category": "Spanish",
        "difficulty_level": "beginner",
        "time_limit": 30,
        "questions": [
            {
                "text": "What is the Spanish word for 'hello'?",
                "question_type": "multiple_choice",
                "explanation": "Hola is the most common greeting",
                "points": 1,
                "answers": [
                    {"text": "Hola", "is_correct": true},
                    {"text": "Adiós", "is_correct": false},
                    {"text": "Gracias", "is_correct": false}
                ]
            }
        ]
    }
    
    Returns:
        JSON: Created quiz data with ID
    """
    data = request.get_json()
    
    if not data:
        return QuizController.error_response("Request body must be valid JSON", 400)
    
    # Extract creator info from headers if available (for future auth integration)
    created_by = request.headers.get('X-User-ID', 'anonymous')
    
    return QuizController.create_quiz(data, created_by)

@quiz_bp.route('', methods=['GET'])
def get_all_quizzes():
    """
    Get a paginated list of quizzes with optional filtering.
    
    Query parameters:
        page (int): Page number (default: 1)
        per_page (int): Items per page (default: 10, max: 100)
        category (str): Filter by category
        difficulty (str): Filter by difficulty level
        active_only (bool): Only show active quizzes (default: true)
    
    Returns:
        JSON: Paginated list of quizzes
    """
    # Get query parameters
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    active_only = request.args.get('active_only', 'true').lower() == 'true'
    
    return QuizController.get_all_quizzes(
        page=page,
        per_page=per_page,
        category=category,
        difficulty=difficulty,
        active_only=active_only
    )

@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """
    Get a specific quiz by ID.
    
    Query parameters:
        for_student (bool): If true, hides correct answers (default: false)
    
    Args:
        quiz_id (int): The quiz ID
    
    Returns:
        JSON: Quiz data with questions and answers
    """
    for_student = request.args.get('for_student', 'false').lower() == 'true'
    
    return QuizController.get_quiz(quiz_id, for_student=for_student)

@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
def update_quiz(quiz_id):
    """
    Update an existing quiz.
    
    Expected JSON payload (partial updates allowed):
    {
        "title": "Updated Quiz Title",
        "description": "Updated description",
        "category": "Updated Category",
        "difficulty_level": "intermediate",
        "time_limit": 45,
        "is_active": false
    }
    
    Args:
        quiz_id (int): The quiz ID to update
    
    Returns:
        JSON: Updated quiz data
    """
    data = request.get_json()
    
    if not data:
        return QuizController.error_response("Request body must be valid JSON", 400)
    
    # Extract updater info from headers if available
    updated_by = request.headers.get('X-User-ID', 'anonymous')
    
    return QuizController.update_quiz(quiz_id, data, updated_by)

@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
def delete_quiz(quiz_id):
    """
    Delete a quiz and all its questions/answers.
    
    Args:
        quiz_id (int): The quiz ID to delete
    
    Returns:
        JSON: Success confirmation
    """
    return QuizController.delete_quiz(quiz_id)

@quiz_bp.route('/categories', methods=['GET'])
def get_categories():
    """
    Get a list of all available quiz categories.
    Note: This is a placeholder - in a real app, you might query distinct categories.
    
    Returns:
        JSON: List of available categories
    """
    # This could be made dynamic by querying the database
    categories = [
        "Spanish", "French", "German", "Italian", "Portuguese",
        "English Grammar", "Vocabulary", "Pronunciation", "Conversation"
    ]
    
    return QuizController.success_response(
        data={"categories": categories},
        message="Categories retrieved successfully"
    )

@quiz_bp.route('/difficulty-levels', methods=['GET'])
def get_difficulty_levels():
    """
    Get a list of all available difficulty levels.
    
    Returns:
        JSON: List of difficulty levels
    """
    difficulty_levels = ["beginner", "intermediate", "advanced"]
    
    return QuizController.success_response(
        data={"difficulty_levels": difficulty_levels},
        message="Difficulty levels retrieved successfully"
    )

# Error handlers for this blueprint
@quiz_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors for quiz routes."""
    return QuizController.error_response("Quiz not found", 404)

@quiz_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for quiz routes."""
    return QuizController.error_response("Internal server error", 500)
