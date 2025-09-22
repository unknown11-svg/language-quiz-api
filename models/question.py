"""
Question model for the Language Learning Quiz API.

This model represents individual questions within a quiz.
Each question belongs to a quiz and can have multiple answer choices.
"""
from models import db
from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from .answer import Answer

class Question(db.Model):
    """
    Question model representing a single question in a quiz.
    
    Attributes:
        id (int): Primary key, unique identifier for the question
        text (str): The question text/prompt
        question_type (str): Type of question ('multiple_choice', 'true_false', 'fill_blank')
        explanation (str): Optional explanation for the correct answer
        points (int): Point value for this question (default: 1)
        order_index (int): Display order within the quiz
        created_at (datetime): When the question was created
        quiz_id (int): Foreign key linking to the parent quiz
        
    Relationships:
        quiz: Many-to-one relationship with Quiz model (via backref)
        answers: One-to-many relationship with Answer model
    """
    
    __tablename__ = 'question'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Question Content
    text = db.Column(db.String(500), nullable=False)  # Increased length for longer questions
    question_type = db.Column(db.String(20), default='multiple_choice')  # multiple_choice, true_false, fill_blank
    explanation = db.Column(db.Text, nullable=True)  # Explanation for the correct answer
    
    # Question Settings
    points = db.Column(db.Integer, default=1)  # Point value for this question
    order_index = db.Column(db.Integer, default=0)  # Order within the quiz
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    
    # Relationships
    answers: Mapped[list['Answer']] = relationship('Answer', backref='question', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of the Question object."""
        return f'<Question {self.id}: {self.text[:50]}...>'
    
    def to_dict(self, include_answers: bool = False) -> dict:
        """
        Convert Question object to dictionary for JSON serialization.
        
        Args:
            include_answers (bool): Whether to include answer choices
            
        Returns:
            dict: Dictionary representation of the question
        """
        question_dict = {
            'id': self.id,
            'text': self.text,
            'question_type': self.question_type,
            'explanation': self.explanation,
            'points': self.points,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'quiz_id': self.quiz_id
        }
        
        if include_answers:
            question_dict['answers'] = [answer.to_dict() for answer in self.answers]
            
        return question_dict
    
    def to_student_dict(self) -> dict:
        """
        Convert Question to dictionary for student view (no correct answer info).
        
        Returns:
            dict: Student-safe dictionary representation
        """
        return {
            'id': self.id,
            'text': self.text,
            'question_type': self.question_type,
            'points': self.points,
            'order_index': self.order_index,
            'answers': [answer.to_student_dict() for answer in self.answers]
        }
    
    def get_correct_answer(self) -> Optional['Answer']:
        """
        Get the correct answer for this question.
        
        Returns:
            Answer: The correct answer object, or None if not found
        """
        return next((answer for answer in self.answers if answer.is_correct), None)
    
    def validate_answer(self, submitted_answer_id: int) -> bool:
        """
        Check if the submitted answer ID is correct.
        
        Args:
            submitted_answer_id (int): The ID of the submitted answer
            
        Returns:
            bool: True if the answer is correct, False otherwise
        """
        correct_answer = self.get_correct_answer()
        return correct_answer is not None and correct_answer.id == submitted_answer_id
