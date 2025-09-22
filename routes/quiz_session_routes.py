"""
Quiz session routes for the Language Learning Quiz API.

This module defines HTTP endpoints for quiz-taking functionality.
These routes are used by students to take quizzes and receive feedback.
"""
from flask import Blueprint, request
from controllers import QuizSessionController

# Create the quiz session blueprint
session_bp = Blueprint('quiz_session', __name__, url_prefix='/api/v1/quiz-sessions')

@session_bp.route('/start/<int:quiz_id>', methods=['POST'])
def start_quiz_session(quiz_id):
    """
    Start a new quiz session for a student.
    
    Expected JSON payload (optional):
    {
        "student_id": "student123",
        "student_name": "John Doe"
    }
    
    Args:
        quiz_id (int): The quiz ID to start
    
    Returns:
        JSON: Quiz data for student (without correct answers) and session info
    """
    data = request.get_json() or {}
    
    # Extract student info from payload or headers
    student_id = data.get('student_id') or request.headers.get('X-Student-ID')
    
    return QuizSessionController.start_quiz_session(quiz_id, student_id)

@session_bp.route('/submit/<int:quiz_id>', methods=['POST'])
def submit_quiz(quiz_id):
    """
    Submit answers for a quiz and get detailed results.
    
    Expected JSON payload:
    {
        "started_at": "2023-09-22T10:30:00Z",  // Optional, for time validation
        "answers": [
            {
                "question_id": 1,
                "answer_id": 3
            },
            {
                "question_id": 2,
                "answer_id": 7
            }
        ]
    }
    
    Args:
        quiz_id (int): The quiz ID being submitted
    
    Returns:
        JSON: Detailed quiz results with scoring and feedback
    """
    data = request.get_json()
    
    if not data:
        return QuizSessionController.error_response("Request body must be valid JSON", 400)
    
    # Extract student info from headers if available
    student_id = request.headers.get('X-Student-ID')
    
    return QuizSessionController.submit_quiz(quiz_id, data, student_id)

@session_bp.route('/preview/<int:quiz_id>', methods=['GET'])
def preview_quiz(quiz_id):
    """
    Get a preview of a quiz for students (without starting a session).
    This shows basic quiz info and question count without starting the timer.
    
    Args:
        quiz_id (int): The quiz ID to preview
    
    Returns:
        JSON: Quiz preview information
    """
    # This reuses the get_quiz method with student flag
    from controllers import QuizController
    return QuizController.get_quiz(quiz_id, for_student=True)

@session_bp.route('/stats/<int:quiz_id>', methods=['GET'])
def get_quiz_statistics(quiz_id):
    """
    Get statistics about quiz performance (for educators).
    
    Args:
        quiz_id (int): The quiz ID
    
    Returns:
        JSON: Quiz performance statistics
    """
    return QuizSessionController.get_quiz_statistics(quiz_id)

# Additional helper endpoints

@session_bp.route('/validate-answers', methods=['POST'])
def validate_answers_format():
    """
    Validate the format of answer submission without actually submitting.
    Useful for frontend validation.
    
    Expected JSON payload:
    {
        "answers": [
            {"question_id": 1, "answer_id": 3},
            {"question_id": 2, "answer_id": 7}
        ]
    }
    
    Returns:
        JSON: Validation results
    """
    data = request.get_json()
    
    if not data:
        return QuizSessionController.error_response("Request body must be valid JSON", 400)
    
    if 'answers' not in data:
        return QuizSessionController.error_response("Missing 'answers' field", 422)
    
    answers = data['answers']
    errors = []
    
    for i, answer in enumerate(answers):
        if not isinstance(answer, dict):
            errors.append(f"Answer {i} must be an object")
            continue
            
        if 'question_id' not in answer:
            errors.append(f"Answer {i} missing 'question_id'")
            
        if 'answer_id' not in answer:
            errors.append(f"Answer {i} missing 'answer_id'")
            
        # Validate that IDs are integers
        try:
            int(answer.get('question_id', 0))
            int(answer.get('answer_id', 0))
        except (ValueError, TypeError):
            errors.append(f"Answer {i} IDs must be integers")
    
    if errors:
        return QuizSessionController.validation_error_response({"format_errors": errors})
    
    return QuizSessionController.success_response(
        data={"valid": True, "answer_count": len(answers)},
        message="Answer format is valid"
    )

@session_bp.route('/time-check/<int:quiz_id>', methods=['POST'])
def check_time_remaining(quiz_id):
    """
    Check remaining time for a quiz session.
    
    Expected JSON payload:
    {
        "started_at": "2023-09-22T10:30:00Z"
    }
    
    Args:
        quiz_id (int): The quiz ID
    
    Returns:
        JSON: Time remaining information
    """
    data = request.get_json()
    
    if not data or 'started_at' not in data:
        return QuizSessionController.error_response("Missing 'started_at' field", 422)
    
    from models import Quiz
    from datetime import datetime, timedelta
    
    quiz = Quiz.query.get(quiz_id)
    
    if not quiz:
        return QuizSessionController.error_response("Quiz not found", 404)
    
    if not quiz.time_limit:
        return QuizSessionController.success_response(
            data={"unlimited": True},
            message="This quiz has no time limit"
        )
    
    try:
        started_at = datetime.fromisoformat(data['started_at'].replace('Z', '+00:00'))
        elapsed_minutes = (datetime.utcnow() - started_at).total_seconds() / 60
        remaining_minutes = max(0, quiz.time_limit - elapsed_minutes)
        
        return QuizSessionController.success_response(
            data={
                "time_limit_minutes": quiz.time_limit,
                "elapsed_minutes": round(elapsed_minutes, 2),
                "remaining_minutes": round(remaining_minutes, 2),
                "is_expired": remaining_minutes <= 0
            },
            message="Time check completed"
        )
        
    except (ValueError, TypeError):
        return QuizSessionController.error_response("Invalid 'started_at' format", 422)

# Error handlers for this blueprint
@session_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors for session routes."""
    return QuizSessionController.error_response("Quiz session not found", 404)

@session_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors for session routes."""
    return QuizSessionController.error_response("Internal server error", 500)