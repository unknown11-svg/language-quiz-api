"""
Answer model for the Language Learning Quiz API.

This model represents individual answer choices for questions.
Each answer belongs to a question and indicates whether it's the correct choice.
"""
from models import db
from datetime import datetime

class Answer(db.Model):
    """
    Answer model representing a possible answer choice for a question.
    
    Attributes:
        id (int): Primary key, unique identifier for the answer
        text (str): The answer choice text
        is_correct (bool): Whether this answer is the correct one
        explanation (str): Optional explanation for why this answer is right/wrong
        order_index (int): Display order within the question
        created_at (datetime): When the answer was created
        question_id (int): Foreign key linking to the parent question
        
    Relationships:
        question: Many-to-one relationship with Question model (via backref)
    """
    
    __tablename__ = 'answer'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Answer Content
    text = db.Column(db.String(500), nullable=False)  # The answer choice text
    is_correct = db.Column(db.Boolean, default=False, nullable=False)  # Whether this is correct
    explanation = db.Column(db.Text, nullable=True)  # Optional explanation
    
    # Answer Settings
    order_index = db.Column(db.Integer, default=0)  # Display order within question
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    
    def __repr__(self):
        """String representation of the Answer object."""
        status = "✓" if self.is_correct else "✗"
        return f'<Answer {self.id}: {status} {self.text[:30]}...>'
    
    def to_dict(self) -> dict:
        """
        Convert Answer object to dictionary for JSON serialization.
        Includes the correct answer information (for educators).
        
        Returns:
            dict: Dictionary representation of the answer
        """
        return {
            'id': self.id,
            'text': self.text,
            'is_correct': self.is_correct,
            'explanation': self.explanation,
            'order_index': self.order_index,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'question_id': self.question_id
        }
    
    def to_student_dict(self) -> dict:
        """
        Convert Answer to dictionary for student view (no correct answer info).
        
        Returns:
            dict: Student-safe dictionary representation
        """
        return {
            'id': self.id,
            'text': self.text,
            'order_index': self.order_index
        }
    
    def to_result_dict(self) -> dict:
        """
        Convert Answer to dictionary for quiz results/feedback.
        Shows correct answer status and explanation.
        
        Returns:
            dict: Dictionary with feedback information
        """
        return {
            'id': self.id,
            'text': self.text,
            'is_correct': self.is_correct,
            'explanation': self.explanation,
            'order_index': self.order_index
        }
