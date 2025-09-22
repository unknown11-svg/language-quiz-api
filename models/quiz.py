"""
Quiz model for the Language Learning Quiz API.

This model represents a quiz created by educators/facilitators.
A quiz contains multiple questions and serves as the main container
for assessment content.
"""
from models import db
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, relationship

if TYPE_CHECKING:
    from .question import Question

class Quiz(db.Model):
    """
    Quiz model representing a language learning quiz.
    
    Attributes:
        id (int): Primary key, unique identifier for the quiz
        title (str): The title/name of the quiz (max 100 characters)
        description (str): Optional detailed description of the quiz
        category (str): Subject category (e.g., 'Spanish Grammar', 'French Vocabulary')
        difficulty_level (str): Difficulty level ('beginner', 'intermediate', 'advanced')
        time_limit (int): Time limit in minutes (None = no time limit)
        is_active (bool): Whether the quiz is currently active/available
        created_at (datetime): When the quiz was created
        updated_at (datetime): When the quiz was last modified
        created_by (str): ID or name of the educator who created it
        
    Relationships:
        questions: One-to-many relationship with Question model
    """
    
    __tablename__ = 'quiz'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # Classification
    category = db.Column(db.String(50), nullable=True)
    difficulty_level = db.Column(db.String(20), default='beginner')  # beginner, intermediate, advanced
    
    # Quiz Settings
    time_limit = db.Column(db.Integer, nullable=True)  # in minutes, None = no limit
    is_active = db.Column(db.Boolean, default=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.String(100), nullable=True)  # Can store user ID or name
    
    # Relationships
    questions: Mapped[list['Question']] = relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of the Quiz object."""
        return f'<Quiz {self.id}: {self.title}>'
    
    def to_dict(self, include_questions: bool = False) -> dict:
        """
        Convert Quiz object to dictionary for JSON serialization.
        
        Args:
            include_questions (bool): Whether to include questions in the output
            
        Returns:
            dict: Dictionary representation of the quiz
        """
        quiz_dict = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'time_limit': self.time_limit,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by,
            'question_count': len(self.questions)
        }
        
        if include_questions:
            quiz_dict['questions'] = [question.to_dict(include_answers=True) for question in self.questions]
            
        return quiz_dict
    
    def to_student_dict(self) -> dict:
        """
        Convert Quiz to dictionary for student view (no correct answers).
        
        Returns:
            dict: Student-safe dictionary representation
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'difficulty_level': self.difficulty_level,
            'time_limit': self.time_limit,
            'question_count': len(self.questions),
            'questions': [question.to_student_dict() for question in self.questions]
        }
