"""
Quiz controller for the Language Learning Quiz API.

This module handles all business logic related to quiz management:
- Creating and editing quizzes
- Retrieving quiz information
- Managing quiz settings and metadata
- Validating quiz data
"""
from models import db, Quiz, Question, Answer
from .base_controller import BaseController
from datetime import datetime

class QuizController(BaseController):
    """
    Controller for managing quiz operations.
    
    This controller handles:
    - Quiz CRUD operations
    - Quiz validation
    - Quiz metadata management
    - Quiz filtering and searching
    """
    
    @staticmethod
    @BaseController.handle_database_error
    def create_quiz(data, created_by=None):
        """
        Create a new quiz with questions and answers.
        
        Args:
            data (dict): Quiz data including questions and answers
            created_by (str): ID or name of the creator
            
        Returns:
            tuple: (Flask response, status_code)
        """
        # Validate required fields
        required_fields = ['title', 'questions']
        validation_errors = BaseController.validate_required_fields(data, required_fields)
        
        if validation_errors:
            return BaseController.validation_error_response(validation_errors)
        
        # Validate questions
        if not data['questions'] or len(data['questions']) == 0:
            return BaseController.error_response("Quiz must have at least one question", 422)
        
        # Create the quiz
        new_quiz = Quiz(
            title=data['title'],
            description=data.get('description'),
            category=data.get('category'),
            difficulty_level=data.get('difficulty_level', 'beginner'),
            time_limit=data.get('time_limit'),
            created_by=created_by
        )
        
        db.session.add(new_quiz)
        db.session.flush()  # Get the quiz ID without committing
        
        # Add questions and answers
        for q_index, q_data in enumerate(data['questions']):
            question_errors = QuizController._validate_question_data(q_data)
            if question_errors:
                return BaseController.validation_error_response({
                    f"question_{q_index}": question_errors
                })
            
            new_question = Question(
                text=q_data['text'],
                question_type=q_data.get('question_type', 'multiple_choice'),
                explanation=q_data.get('explanation'),
                points=q_data.get('points', 1),
                order_index=q_index,
                quiz_id=new_quiz.id
            )
            
            db.session.add(new_question)
            db.session.flush()  # Get the question ID
            
            # Add answers
            correct_answer_count = 0
            for a_index, a_data in enumerate(q_data['answers']):
                answer_errors = QuizController._validate_answer_data(a_data)
                if answer_errors:
                    return BaseController.validation_error_response({
                        f"question_{q_index}_answer_{a_index}": answer_errors
                    })
                
                is_correct = a_data.get('is_correct', False)
                if is_correct:
                    correct_answer_count += 1
                
                new_answer = Answer(
                    text=a_data['text'],
                    is_correct=is_correct,
                    explanation=a_data.get('explanation'),
                    order_index=a_index,
                    question_id=new_question.id
                )
                
                db.session.add(new_answer)
            
            # Validate that each question has exactly one correct answer
            if correct_answer_count != 1:
                return BaseController.error_response(
                    f"Question {q_index + 1} must have exactly one correct answer", 
                    422
                )
        
        db.session.commit()
        
        return BaseController.success_response(
            data=new_quiz.to_dict(include_questions=True),
            message="Quiz created successfully!",
            status_code=201
        )
    
    @staticmethod
    def get_quiz(quiz_id, for_student=False):
        """
        Retrieve a quiz by ID.
        
        Args:
            quiz_id (int): The quiz ID
            for_student (bool): If True, hide correct answers
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        if not quiz.is_active:
            return BaseController.error_response("Quiz is not currently available", 403)
        
        if for_student:
            quiz_data = quiz.to_student_dict()
        else:
            quiz_data = quiz.to_dict(include_questions=True)
        
        return BaseController.success_response(
            data=quiz_data,
            message="Quiz retrieved successfully"
        )
    
    @staticmethod
    def get_all_quizzes(page=1, per_page=10, category=None, difficulty=None, active_only=True):
        """
        Get a paginated list of quizzes with optional filtering.
        
        Args:
            page (int): Page number
            per_page (int): Items per page
            category (str): Filter by category
            difficulty (str): Filter by difficulty level
            active_only (bool): Only show active quizzes
            
        Returns:
            tuple: (Flask response, status_code)
        """
        query = Quiz.query
        
        if active_only:
            query = query.filter(Quiz.is_active == True)
        
        if category:
            query = query.filter(Quiz.category == category)
        
        if difficulty:
            query = query.filter(Quiz.difficulty_level == difficulty)
        
        query = query.order_by(Quiz.created_at.desc())
        
        pagination_data = BaseController.paginate_query(query, page, per_page)
        
        # Convert quizzes to dictionary format
        quiz_list = [quiz.to_dict() for quiz in pagination_data['items']]
        
        response_data = {
            'quizzes': quiz_list,
            'pagination': {
                'total': pagination_data['total'],
                'pages': pagination_data['pages'],
                'current_page': pagination_data['current_page'],
                'per_page': pagination_data['per_page'],
                'has_next': pagination_data['has_next'],
                'has_prev': pagination_data['has_prev']
            }
        }
        
        return BaseController.success_response(
            data=response_data,
            message="Quizzes retrieved successfully"
        )
    
    @staticmethod
    @BaseController.handle_database_error
    def update_quiz(quiz_id, data, updated_by=None):
        """
        Update an existing quiz.
        
        Args:
            quiz_id (int): The quiz ID to update
            data (dict): Updated quiz data
            updated_by (str): ID or name of the updater
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        # Update basic quiz information
        if 'title' in data:
            quiz.title = data['title']
        if 'description' in data:
            quiz.description = data['description']
        if 'category' in data:
            quiz.category = data['category']
        if 'difficulty_level' in data:
            quiz.difficulty_level = data['difficulty_level']
        if 'time_limit' in data:
            quiz.time_limit = data['time_limit']
        if 'is_active' in data:
            quiz.is_active = data['is_active']
        
        quiz.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return BaseController.success_response(
            data=quiz.to_dict(include_questions=True),
            message="Quiz updated successfully"
        )
    
    @staticmethod
    @BaseController.handle_database_error
    def delete_quiz(quiz_id):
        """
        Delete a quiz and all its questions/answers.
        
        Args:
            quiz_id (int): The quiz ID to delete
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        db.session.delete(quiz)  # Cascade will delete questions and answers
        db.session.commit()
        
        return BaseController.success_response(
            message=f"Quiz '{quiz.title}' deleted successfully"
        )
    
    @staticmethod
    def _validate_question_data(question_data):
        """
        Validate question data structure.
        
        Args:
            question_data (dict): Question data to validate
            
        Returns:
            dict: Validation errors (empty if valid)
        """
        errors = {}
        
        if not question_data.get('text'):
            errors['text'] = "Question text is required"
        
        if not question_data.get('answers') or len(question_data['answers']) < 2:
            errors['answers'] = "Question must have at least 2 answer choices"
        
        question_type = question_data.get('question_type', 'multiple_choice')
        valid_types = ['multiple_choice', 'true_false', 'fill_blank']
        if question_type not in valid_types:
            errors['question_type'] = f"Question type must be one of: {', '.join(valid_types)}"
        
        return errors
    
    @staticmethod
    def _validate_answer_data(answer_data):
        """
        Validate answer data structure.
        
        Args:
            answer_data (dict): Answer data to validate
            
        Returns:
            dict: Validation errors (empty if valid)
        """
        errors = {}
        
        if not answer_data.get('text'):
            errors['text'] = "Answer text is required"
        
        return errors
