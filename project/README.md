# AI Learning Assistant - Intelligent Personalized Learning Platform

A web-based AI Learning Assistant that provides personalized course recommendations, skill assessments through quizzes, and an AI chatbot for learning guidance.

## Features

1. **User Authentication**
   - User registration with email and password
   - Secure login system
   - Session management

2. **Personalized Dashboard**
   - Add and manage your skills
   - View personalized course recommendations based on your skills
   - Track quiz results and skill levels

3. **ML-Powered Course Recommendations**
   - Uses scikit-learn TF-IDF and cosine similarity
   - Recommends courses based on your current skills
   - Shows match percentage for each recommendation

4. **Interactive Quiz System**
   - Take quizzes to assess your skill level
   - Multiple programming language quizzes (Python, Java, JavaScript)
   - Automatic skill level determination (Beginner, Intermediate, Advanced)

5. **AI Chat Assistant**
   - Rule-based chatbot for learning assistance
   - Get advice on programming languages, study tips, and career guidance
   - Context-aware responses based on your skills

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Machine Learning**: Scikit-learn (TF-IDF, Cosine Similarity)

## Project Structure

```
project/
├── app.py              # Main Flask application
├── model.py            # ML model and AI chatbot logic
├── database.db         # SQLite database (created automatically)
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── quiz.html
│   └── chat.html
└── static/            # Static files
    └── style.css      # CSS styling
```

## Installation & Setup

1. **Install Python packages:**
   ```bash
   pip install flask scikit-learn pandas numpy werkzeug
   ```

   Or use requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**
   ```bash
   python app.py
   ```

3. **Open your browser:**
   Navigate to `http://127.0.0.1:5000`

## Usage

1. **Register**: Create a new account with username, email, and password
2. **Login**: Sign in with your credentials
3. **Add Skills**: Add your current programming skills on the dashboard
4. **View Recommendations**: See personalized course recommendations based on your skills
5. **Take Quiz**: Assess your skill level by taking quizzes
6. **Chat with AI**: Ask questions and get learning guidance from the AI assistant

## Database Schema

### Users Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- created_at (Timestamp)

### User Skills Table
- id (Primary Key)
- user_id (Foreign Key)
- skill_name
- skill_level (Beginner/Intermediate/Advanced)
- added_at (Timestamp)

### Quiz Results Table
- id (Primary Key)
- user_id (Foreign Key)
- skill_name
- score
- total_questions
- skill_level
- taken_at (Timestamp)

## ML Model Details

The course recommendation system uses:
- **TF-IDF Vectorization**: Converts course descriptions and user skills into numerical vectors
- **Cosine Similarity**: Calculates similarity between user skills and available courses
- **Top-N Recommendations**: Returns the most relevant courses with match scores

## AI Chatbot

The rule-based chatbot can help with:
- Course recommendations
- Programming language guidance (Python, Java, JavaScript)
- Study tips and learning strategies
- Career advice
- Data structures and algorithms
- Web development guidance

## Security Features

- Password hashing using Werkzeug
- Session-based authentication
- Protected routes (requires login)
- SQL injection prevention using parameterized queries

## Future Enhancements

- OAuth social login
- More quiz topics
- Advanced ML models (collaborative filtering)
- Real-time progress tracking
- Discussion forums
- Video course integration

## Requirements

- Python 3.8+
- Flask 3.0.0
- scikit-learn 1.3.2
- pandas 2.1.4
- numpy 1.26.2
- werkzeug 3.0.1

## License

This project is for educational purposes.

## Author

AI Learning Assistant Platform
