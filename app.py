"""
Main application entry point for the Language Learning Quiz API.

This file creates and runs the Flask application using the application factory pattern.
"""
import os
from __init__ import create_app

# Determine configuration based on environment
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

"""
Main application entry point for the Language Learning Quiz API.

This file creates and runs the Flask application using the application factory pattern.
"""
import os
from __init__ import create_app

# Determine configuration based on environment
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

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