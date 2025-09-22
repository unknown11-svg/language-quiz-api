"""
Base controller class for the Language Learning Quiz API.

This module provides common functionality and patterns that all controllers
can inherit from, promoting consistency and reducing code duplication.
"""
from flask import jsonify
from models import db
import traceback

class BaseController:
    """
    Base controller class providing common functionality for all controllers.
    
    This class includes:
    - Standard response formatting
    - Error handling patterns
    - Database transaction management
    - Common validation methods
    """
    
    @staticmethod
    def success_response(data=None, message="Success", status_code=200):
        """
        Create a standardized success response.
        
        Args:
            data: The data to include in the response
            message (str): Success message
            status_code (int): HTTP status code
            
        Returns:
            tuple: (Flask response, status_code)
        """
        response_data = {
            "success": True,
            "message": message,
            "data": data
        }
        return jsonify(response_data), status_code
    
    @staticmethod
    def error_response(message="An error occurred", status_code=400, error_details=None):
        """
        Create a standardized error response.
        
        Args:
            message (str): Error message
            status_code (int): HTTP status code
            error_details: Additional error information
            
        Returns:
            tuple: (Flask response, status_code)
        """
        response_data = {
            "success": False,
            "message": message,
            "error": error_details
        }
        return jsonify(response_data), status_code
    
    @staticmethod
    def validation_error_response(errors):
        """
        Create a response for validation errors.
        
        Args:
            errors (dict): Dictionary of field validation errors
            
        Returns:
            tuple: (Flask response, status_code)
        """
        return BaseController.error_response(
            message="Validation errors",
            status_code=422,
            error_details=errors
        )
    
    @staticmethod
    def handle_database_error(func):
        """
        Decorator to handle database errors consistently.
        
        Args:
            func: The function to wrap
            
        Returns:
            function: Wrapped function with error handling
        """
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                db.session.rollback()
                print(f"Database error in {func.__name__}: {str(e)}")
                print(traceback.format_exc())
                return BaseController.error_response(
                    message="A database error occurred",
                    status_code=500,
                    error_details=str(e) if not hasattr(e, 'hide_parameters') else None
                )
        return wrapper
    
    @staticmethod
    def validate_required_fields(data, required_fields):
        """
        Validate that all required fields are present in the data.
        
        Args:
            data (dict): The data to validate
            required_fields (list): List of required field names
            
        Returns:
            dict: Dictionary of validation errors (empty if valid)
        """
        errors = {}
        for field in required_fields:
            if field not in data or data[field] is None or data[field] == "":
                errors[field] = f"{field} is required"
        return errors
    
    @staticmethod
    def paginate_query(query, page=1, per_page=10, max_per_page=100):
        """
        Paginate a SQLAlchemy query.
        
        Args:
            query: SQLAlchemy query object
            page (int): Page number (1-based)
            per_page (int): Items per page
            max_per_page (int): Maximum items per page
            
        Returns:
            dict: Pagination information and results
        """
        per_page = min(per_page, max_per_page)
        
        paginated = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'items': paginated.items,
            'total': paginated.total,
            'pages': paginated.pages,
            'current_page': paginated.page,
            'per_page': per_page,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev,
            'next_num': paginated.next_num,
            'prev_num': paginated.prev_num
        }