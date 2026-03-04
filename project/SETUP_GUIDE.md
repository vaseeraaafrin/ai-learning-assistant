# AI Learning Assistant - Setup Guide

## Quick Start Guide

Follow these steps to run the AI Learning Assistant on your local machine:

### Step 1: Install Dependencies

Open your terminal in VS Code and run:

```bash
pip install flask scikit-learn pandas numpy werkzeug
```

Or use the requirements file:

```bash
pip install -r requirements.txt
```

### Step 2: Run the Application

Start the Flask server:

```bash
python app.py
```

You should see output like:
```
Database initialized!
 * Running on http://127.0.0.1:5000
```

### Step 3: Open in Browser

Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

### Step 4: Create an Account

1. Click on "Register here" on the login page
2. Fill in your username, email, and password
3. Click "Register"
4. You'll be redirected to the login page

### Step 5: Start Using the Platform

After logging in, you can:

1. **Add Skills**: Enter your programming skills (e.g., Python, Java, JavaScript)
2. **View Recommendations**: See personalized course recommendations based on your skills
3. **Take Quizzes**: Test your knowledge and get your skill level assessed
4. **Chat with AI**: Ask questions about programming, learning tips, and career advice

## Features Overview

### Dashboard
- Add and manage your skills
- View personalized course recommendations with match scores
- See your recent quiz results and skill levels

### Quiz System
- Available for Python, Java, JavaScript, and general programming
- 10 questions per quiz
- Automatic skill level determination (Beginner/Intermediate/Advanced)
- Results are saved and displayed on your dashboard

### AI Chat Assistant
The chatbot can help with:
- Programming language guidance
- Course recommendations
- Study tips and learning strategies
- Career advice
- Web development questions
- Data structures and algorithms

### Example Questions for the Chatbot:
- "How do I start learning Python?"
- "What are some tips for studying programming?"
- "Tell me about Java programming"
- "How can I prepare for technical interviews?"
- "What is the best way to learn web development?"

## Troubleshooting

### If you get "Module not found" errors:
Make sure all dependencies are installed:
```bash
pip install flask scikit-learn pandas numpy werkzeug
```

### If port 5000 is already in use:
Edit `app.py` and change the port number:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### If the database doesn't initialize:
Delete `database.db` and restart the application:
```bash
rm database.db
python app.py
```

## Project Structure

```
project/
├── app.py                  # Main Flask application with routes
├── model.py                # ML model and AI logic
├── database.db             # SQLite database (auto-created)
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── SETUP_GUIDE.md         # This file
├── test_app.py            # Test script
├── templates/             # HTML templates
│   ├── base.html          # Base template with navbar
│   ├── login.html         # Login page
│   ├── register.html      # Registration page
│   ├── dashboard.html     # Main dashboard
│   ├── quiz.html          # Quiz interface
│   └── chat.html          # AI chatbot
└── static/                # Static files
    └── style.css          # CSS styling
```

## Technologies Used

- **Backend**: Python Flask 3.0.0
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Database**: SQLite3
- **Machine Learning**: scikit-learn (TF-IDF, Cosine Similarity)
- **Security**: Werkzeug password hashing, Flask sessions

## Key Features

1. ✅ User authentication (register/login)
2. ✅ Skill management system
3. ✅ ML-based course recommendations
4. ✅ Interactive quiz system with multiple topics
5. ✅ Rule-based AI chatbot
6. ✅ Responsive design
7. ✅ Clean and modern UI
8. ✅ Secure password handling
9. ✅ Session management
10. ✅ Real-time quiz feedback

## For Development

To run in development mode (with auto-reload):
- The app is already configured with `debug=True`
- Any changes to Python files will auto-reload the server

To run tests:
```bash
python test_app.py
```

## Notes

- The database is created automatically on first run
- Sample course data is included in `model.py`
- Quiz questions are pre-loaded for Python, Java, and JavaScript
- The chatbot uses rule-based pattern matching
- All passwords are hashed before storage
- Sessions expire when you close the browser

## Next Steps

After getting familiar with the platform:
1. Try adding different skills to see varied recommendations
2. Take quizzes in different programming languages
3. Experiment with the AI chatbot by asking various questions
4. Check how your skill levels update after taking quizzes

Enjoy learning with the AI Learning Assistant!
