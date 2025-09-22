# Language Learning Quiz API 🎓

A comprehensive REST API for creating and managing language learning quizzes. Built with Flask, SQLAlchemy, and designed for easy integration with language learning platforms.

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone and navigate to the project
cd language-quiz-api

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
copy .env.example .env
# Edit .env with your Supabase credentials
```

### 2. Configuration

Edit your `.env` file with your Supabase credentials:

```env
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
SUPABASE_URL=https://[YOUR-PROJECT-REF].supabase.co
SUPABASE_KEY=[YOUR-ANON-KEY]
SECRET_KEY=your-secret-key-here
```

### 3. Run the API

```bash
python app_new.py
```

The API will be available at `http://localhost:5000`

## 📚 API Endpoints

### Quiz Management (Educators)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/quizzes` | Create a new quiz |
| GET | `/api/v1/quizzes` | List all quizzes (with filtering) |
| GET | `/api/v1/quizzes/{id}` | Get specific quiz |
| PUT | `/api/v1/quizzes/{id}` | Update quiz |
| DELETE | `/api/v1/quizzes/{id}` | Delete quiz |
| GET | `/api/v1/quizzes/categories` | Get available categories |
| GET | `/api/v1/quizzes/difficulty-levels` | Get difficulty levels |

### Quiz Taking (Students)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/quiz-sessions/start/{id}` | Start a quiz session |
| POST | `/api/v1/quiz-sessions/submit/{id}` | Submit quiz answers |
| GET | `/api/v1/quiz-sessions/preview/{id}` | Preview quiz without starting |
| POST | `/api/v1/quiz-sessions/time-check/{id}` | Check remaining time |
| POST | `/api/v1/quiz-sessions/validate-answers` | Validate answer format |

## 🎯 Example Usage

### Creating a Quiz

```bash
curl -X POST http://localhost:5000/api/v1/quizzes \
  -H "Content-Type: application/json" \
  -H "X-User-ID: educator123" \
  -d '{
    "title": "Spanish Basics Quiz",
    "description": "Test your basic Spanish vocabulary",
    "category": "Spanish",
    "difficulty_level": "beginner",
    "time_limit": 30,
    "questions": [
      {
        "text": "What is the Spanish word for 'hello'?",
        "question_type": "multiple_choice",
        "explanation": "Hola is the most common Spanish greeting",
        "points": 1,
        "answers": [
          {"text": "Hola", "is_correct": true},
          {"text": "Adiós", "is_correct": false},
          {"text": "Gracias", "is_correct": false},
          {"text": "Por favor", "is_correct": false}
        ]
      }
    ]
  }'
```

### Taking a Quiz

```bash
# 1. Start a quiz session
curl -X POST http://localhost:5000/api/v1/quiz-sessions/start/1 \
  -H "Content-Type: application/json" \
  -H "X-Student-ID: student456" \
  -d '{"student_id": "student456"}'

# 2. Submit answers
curl -X POST http://localhost:5000/api/v1/quiz-sessions/submit/1 \
  -H "Content-Type: application/json" \
  -H "X-Student-ID: student456" \
  -d '{
    "started_at": "2023-09-22T10:30:00Z",
    "answers": [
      {"question_id": 1, "answer_id": 1}
    ]
  }'
```

## 🏗️ Architecture

### Directory Structure
```
language-quiz-api/
├── models/          # Database models (Quiz, Question, Answer)
├── controllers/     # Business logic
├── routes/          # HTTP endpoints
├── config.py        # Configuration management
├── requirements.txt # Python dependencies
└── app_new.py       # Application entry point
```

### Key Features

- **🎯 Separation of Concerns**: Models, Controllers, and Routes are clearly separated
- **🔒 Student Safety**: Student endpoints hide correct answers until submission
- **⏱️ Time Management**: Built-in support for timed quizzes
- **📊 Rich Feedback**: Detailed scoring with explanations and suggestions
- **🎨 Flexible Design**: Support for multiple question types and difficulty levels
- **🗄️ Supabase Integration**: PostgreSQL database with real-time capabilities
- **🌐 CORS Enabled**: Ready for frontend integration

## 🎮 Quiz Features

### Question Types
- Multiple Choice
- True/False
- Fill in the Blank (placeholder for future)

### Difficulty Levels
- Beginner
- Intermediate  
- Advanced

### Scoring System
- Point-based scoring
- Percentage calculations
- Letter grades (A-F)
- Personalized feedback based on performance

## 🔧 Development

### Project Structure Philosophy

This API follows the **MVC (Model-View-Controller)** pattern with Flask Blueprints:

- **Models**: Database entities and relationships
- **Controllers**: Business logic and data processing
- **Routes**: HTTP endpoints and request/response handling

### Adding New Features

1. **New Models**: Add to `models/` directory
2. **Business Logic**: Add to `controllers/` directory  
3. **API Endpoints**: Add to `routes/` directory
4. **Update**: Register new blueprints in `routes/__init__.py`

## 🚀 Deployment

This API is designed to work with:
- **Supabase** (PostgreSQL database)
- **Heroku** (easy deployment)
- **Docker** (containerization)
- **Any cloud provider** supporting Python/Flask

## 📖 Integration Guide

### For Language Learning Platforms

This API is designed to be easily integrated into existing language learning platforms:

1. **Create Quizzes**: Use educator endpoints to create course-specific quizzes
2. **Student Progress**: Track student performance through quiz sessions
3. **Adaptive Learning**: Use difficulty levels and categories to personalize content
4. **Real-time Features**: Leverage Supabase for real-time quiz updates

### Authentication Integration

The API includes placeholder headers (`X-User-ID`, `X-Student-ID`) for easy integration with your existing authentication system.

## 🎓 Educational Features

- **Immediate Feedback**: Students get explanations for right and wrong answers
- **Performance Tracking**: Detailed analytics on quiz performance
- **Adaptive Messaging**: Encouragement and suggestions based on performance
- **Time Management**: Optional time limits to simulate exam conditions

---

**Built for Learning, Designed for Scale** 🚀