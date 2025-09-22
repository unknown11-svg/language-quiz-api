"""
Quiz session controller for the Language Learning Quiz API.

This module handles quiz-taking sessions, including:
- Starting quiz sessions
- Submitting answers
- Calculating scores
- Providing feedback
"""
from models import db, Quiz, Question, Answer
from .base_controller import BaseController
from datetime import datetime, timedelta
import json

class QuizSessionController(BaseController):
    """
    Controller for managing quiz sessions and student interactions.
    
    This controller handles:
    - Quiz session management
    - Answer submission and validation
    - Score calculation
    - Feedback generation
    """
    
    @staticmethod
    def start_quiz_session(quiz_id, student_id=None):
        """
        Start a new quiz session for a student.
        
        Args:
            quiz_id (int): The quiz ID
            student_id (str): Optional student identifier
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        if not quiz.is_active:
            return BaseController.error_response("Quiz is not currently available", 403)
        
        # Calculate session end time if there's a time limit
        session_data = {
            'quiz': quiz.to_student_dict(),
            'session_info': {
                'started_at': datetime.utcnow().isoformat(),
                'student_id': student_id,
                'time_limit_minutes': quiz.time_limit
            }
        }
        
        # Add deadline if time limit is set
        if quiz.time_limit:
            deadline = datetime.utcnow() + timedelta(minutes=quiz.time_limit)
            session_data['session_info']['deadline'] = deadline.isoformat()
        
        return BaseController.success_response(
            data=session_data,
            message="Quiz session started successfully"
        )
    
    @staticmethod
    def submit_quiz(quiz_id, submission_data, student_id=None):
        """
        Submit answers for a quiz and calculate the score.
        
        Args:
            quiz_id (int): The quiz ID
            submission_data (dict): Contains answers array and optional timing info
            student_id (str): Optional student identifier
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        if not quiz.is_active:
            return BaseController.error_response("Quiz is not currently available", 403)
        
        # Validate submission data
        if 'answers' not in submission_data:
            return BaseController.error_response("Submission must include answers", 422)
        
        answers_data = submission_data['answers']
        
        # Check if time limit was exceeded (if applicable)
        if quiz.time_limit and 'started_at' in submission_data:
            try:
                started_at = datetime.fromisoformat(submission_data['started_at'].replace('Z', '+00:00'))
                time_elapsed = (datetime.utcnow() - started_at).total_seconds() / 60
                if time_elapsed > quiz.time_limit:
                    return BaseController.error_response(
                        "Time limit exceeded for this quiz", 
                        422
                    )
            except (ValueError, KeyError):
                # If we can't parse the start time, continue without time validation
                pass
        
        # Process answers and calculate score
        results = QuizSessionController._process_quiz_submission(quiz, answers_data)
        
        return BaseController.success_response(
            data=results,
            message="Quiz submitted successfully!"
        )
    
    @staticmethod
    def _process_quiz_submission(quiz, submitted_answers):
        """
        Process quiz submission and calculate detailed results.
        
        Args:
            quiz (Quiz): The quiz object
            submitted_answers (list): List of submitted answer data
            
        Returns:
            dict: Detailed quiz results with scoring and feedback
        """
        # Initialize result tracking
        correct_count = 0
        total_questions = len(quiz.questions)
        total_points_possible = sum(q.points for q in quiz.questions)
        total_points_earned = 0
        question_results = []
        
        # Create lookup for submitted answers
        submitted_lookup = {
            int(answer['question_id']): int(answer['answer_id']) 
            for answer in submitted_answers 
            if 'question_id' in answer and 'answer_id' in answer
        }
        
        # Process each question
        for question in quiz.questions:
            submitted_answer_id = submitted_lookup.get(question.id)
            correct_answer = question.get_correct_answer()
            
            # Determine if answer was correct
            is_correct = False
            if submitted_answer_id and correct_answer:
                is_correct = submitted_answer_id == correct_answer.id
            
            if is_correct:
                correct_count += 1
                total_points_earned += question.points
            
            # Find the submitted answer object for detailed feedback
            submitted_answer = None
            if submitted_answer_id:
                submitted_answer = next(
                    (a for a in question.answers if a.id == submitted_answer_id), 
                    None
                )
            
            # Build question result
            question_result = {
                'question_id': question.id,
                'question_text': question.text,
                'question_type': question.question_type,
                'points_possible': question.points,
                'points_earned': question.points if is_correct else 0,
                'is_correct': is_correct,
                'submitted_answer': {
                    'id': submitted_answer.id if submitted_answer else None,
                    'text': submitted_answer.text if submitted_answer else None
                } if submitted_answer else None,
                'correct_answer': {
                    'id': correct_answer.id if correct_answer else None,
                    'text': correct_answer.text if correct_answer else None,
                    'explanation': correct_answer.explanation if correct_answer else None
                } if correct_answer else None,
                'question_explanation': question.explanation
            }
            
            question_results.append(question_result)
        
        # Calculate percentages
        percentage_correct = (correct_count / total_questions * 100) if total_questions > 0 else 0
        points_percentage = (total_points_earned / total_points_possible * 100) if total_points_possible > 0 else 0
        
        # Determine grade/performance level
        grade = QuizSessionController._calculate_grade(percentage_correct)
        
        # Build comprehensive results
        results = {
            'quiz_info': {
                'id': quiz.id,
                'title': quiz.title,
                'category': quiz.category,
                'difficulty_level': quiz.difficulty_level
            },
            'score_summary': {
                'correct_answers': correct_count,
                'total_questions': total_questions,
                'percentage_correct': round(percentage_correct, 2),
                'points_earned': total_points_earned,
                'total_points_possible': total_points_possible,
                'points_percentage': round(points_percentage, 2),
                'grade': grade
            },
            'question_results': question_results,
            'performance_feedback': QuizSessionController._generate_performance_feedback(
                percentage_correct, 
                quiz.difficulty_level
            ),
            'submitted_at': datetime.utcnow().isoformat()
        }
        
        return results
    
    @staticmethod
    def _calculate_grade(percentage):
        """
        Calculate letter grade based on percentage.
        
        Args:
            percentage (float): Percentage score
            
        Returns:
            str: Letter grade
        """
        if percentage >= 90:
            return 'A'
        elif percentage >= 80:
            return 'B'
        elif percentage >= 70:
            return 'C'
        elif percentage >= 60:
            return 'D'
        else:
            return 'F'
    
    @staticmethod
    def _generate_performance_feedback(percentage, difficulty_level):
        """
        Generate personalized feedback based on performance.
        
        Args:
            percentage (float): Percentage score
            difficulty_level (str): Quiz difficulty level
            
        Returns:
            dict: Feedback message and suggestions
        """
        feedback = {
            'message': '',
            'suggestions': []
        }
        
        if percentage >= 90:
            feedback['message'] = "Excellent work! You've mastered this material."
            feedback['suggestions'] = [
                f"Consider trying a more challenging {difficulty_level} quiz",
                "You're ready to move on to advanced topics"
            ]
        elif percentage >= 80:
            feedback['message'] = "Great job! You have a solid understanding of the material."
            feedback['suggestions'] = [
                "Review the questions you missed for even better results",
                "You're doing well - keep practicing!"
            ]
        elif percentage >= 70:
            feedback['message'] = "Good work! You're getting the hang of it."
            feedback['suggestions'] = [
                "Focus on reviewing the areas where you made mistakes",
                "Try some practice exercises to strengthen weak areas"
            ]
        elif percentage >= 60:
            feedback['message'] = "You're making progress, but there's room for improvement."
            feedback['suggestions'] = [
                "Review the material and try again",
                "Consider studying the explanations for incorrect answers",
                "Practice with similar quizzes to build confidence"
            ]
        else:
            feedback['message'] = "This is a challenging topic - don't give up!"
            feedback['suggestions'] = [
                "Review the study material carefully",
                "Start with easier quizzes to build your foundation",
                "Consider getting help from a teacher or study group",
                "Take your time and try again when you feel ready"
            ]
        
        return feedback
    
    @staticmethod
    def get_quiz_statistics(quiz_id):
        """
        Get statistics about quiz performance (for educators).
        Note: This would require a submissions table in a real application.
        For now, this is a placeholder for future implementation.
        
        Args:
            quiz_id (int): The quiz ID
            
        Returns:
            tuple: (Flask response, status_code)
        """
        quiz = Quiz.query.get(quiz_id)
        
        if not quiz:
            return BaseController.error_response("Quiz not found", 404)
        
        # This is a placeholder - in a real application, you'd query a submissions table
        stats = {
            'quiz_id': quiz_id,
            'quiz_title': quiz.title,
            'total_questions': len(quiz.questions),
            'total_points': sum(q.points for q in quiz.questions),
            'note': 'Statistics tracking would require a submissions table for full implementation'
        }
        
        return BaseController.success_response(
            data=stats,
            message="Quiz statistics retrieved (placeholder)"
        )