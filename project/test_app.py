import os
import sys

print("Testing AI Learning Assistant application...")

# Test imports
try:
    import flask
    print("✓ Flask imported successfully")
except ImportError as e:
    print(f"✗ Failed to import Flask: {e}")
    sys.exit(1)

try:
    import sklearn
    print("✓ scikit-learn imported successfully")
except ImportError as e:
    print(f"✗ Failed to import scikit-learn: {e}")
    sys.exit(1)

try:
    import pandas
    print("✓ pandas imported successfully")
except ImportError as e:
    print(f"✗ Failed to import pandas: {e}")
    sys.exit(1)

try:
    import numpy
    print("✓ numpy imported successfully")
except ImportError as e:
    print(f"✗ Failed to import numpy: {e}")
    sys.exit(1)

# Test app initialization
try:
    from app import app, init_db
    print("✓ Flask app imported successfully")
except ImportError as e:
    print(f"✗ Failed to import app: {e}")
    sys.exit(1)

# Test model
try:
    from model import CourseRecommender, get_skill_level, get_chat_response, get_quiz_questions
    print("✓ Model imported successfully")
except ImportError as e:
    print(f"✗ Failed to import model: {e}")
    sys.exit(1)

# Test CourseRecommender
try:
    recommender = CourseRecommender()
    recommendations = recommender.recommend_courses(['Python', 'Java'], top_n=3)
    print(f"✓ Course recommender working: Found {len(recommendations)} recommendations")
except Exception as e:
    print(f"✗ Course recommender failed: {e}")
    sys.exit(1)

# Test skill level calculation
try:
    level = get_skill_level(8, 10)
    assert level == 'Advanced', f"Expected 'Advanced' but got '{level}'"
    level = get_skill_level(6, 10)
    assert level == 'Intermediate', f"Expected 'Intermediate' but got '{level}'"
    level = get_skill_level(3, 10)
    assert level == 'Beginner', f"Expected 'Beginner' but got '{level}'"
    print("✓ Skill level calculation working")
except Exception as e:
    print(f"✗ Skill level calculation failed: {e}")
    sys.exit(1)

# Test chatbot
try:
    response = get_chat_response("Hello", ['Python'])
    assert len(response) > 0, "Chatbot returned empty response"
    print("✓ Chatbot working")
except Exception as e:
    print(f"✗ Chatbot failed: {e}")
    sys.exit(1)

# Test quiz questions
try:
    questions = get_quiz_questions('Python')
    assert len(questions) == 10, f"Expected 10 questions but got {len(questions)}"
    print("✓ Quiz questions working")
except Exception as e:
    print(f"✗ Quiz questions failed: {e}")
    sys.exit(1)

# Test database initialization
try:
    if os.path.exists('database.db'):
        os.remove('database.db')
    init_db()
    assert os.path.exists('database.db'), "Database file not created"
    print("✓ Database initialized successfully")
except Exception as e:
    print(f"✗ Database initialization failed: {e}")
    sys.exit(1)

# Test Flask routes
try:
    with app.test_client() as client:
        # Test login page
        response = client.get('/login')
        assert response.status_code == 200, f"Login page returned status {response.status_code}"

        # Test register page
        response = client.get('/register')
        assert response.status_code == 200, f"Register page returned status {response.status_code}"

        print("✓ Flask routes working")
except Exception as e:
    print(f"✗ Flask routes failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("All tests passed! ✓")
print("="*50)
print("\nYour AI Learning Assistant is ready to run!")
print("\nTo start the application:")
print("  python app.py")
print("\nThen open your browser to:")
print("  http://127.0.0.1:5000")
