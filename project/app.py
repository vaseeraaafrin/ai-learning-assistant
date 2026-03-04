from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
from model import CourseRecommender, get_skill_level, get_chat_response

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'

DATABASE = 'database.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # User skills table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_skills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            skill_level TEXT DEFAULT 'Beginner',
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    # Quiz results table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            skill_name TEXT NOT NULL,
            score INTEGER NOT NULL,
            total_questions INTEGER NOT NULL,
            skill_level TEXT NOT NULL,
            taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            return render_template('register.html', error='All fields are required')

        conn = get_db()
        cursor = conn.cursor()

        # Check if user exists
        cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', (username, email))
        if cursor.fetchone():
            conn.close()
            return render_template('register.html', error='Username or email already exists')

        # Create user
        hashed_password = generate_password_hash(password)
        cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                      (username, email, hashed_password))
        conn.commit()
        conn.close()

        return redirect(url_for('login', success='Registration successful! Please login.'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))

        return render_template('login.html', error='Invalid username or password')

    success = request.args.get('success')
    return render_template('login.html', success=success)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()

    # Get user skills
    cursor.execute('SELECT * FROM user_skills WHERE user_id = ? ORDER BY added_at DESC',
                  (session['user_id'],))
    skills = cursor.fetchall()

    # Get recommended courses
    recommender = CourseRecommender()
    skill_names = [skill['skill_name'] for skill in skills]
    recommendations = recommender.recommend_courses(skill_names)

    # Get recent quiz results
    cursor.execute('SELECT * FROM quiz_results WHERE user_id = ? ORDER BY taken_at DESC LIMIT 5',
                  (session['user_id'],))
    quiz_results = cursor.fetchall()

    conn.close()

    return render_template('dashboard.html',
                         username=session['username'],
                         skills=skills,
                         recommendations=recommendations,
                         quiz_results=quiz_results)

@app.route('/add_skill', methods=['POST'])
def add_skill():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    skill_name = request.form.get('skill_name')
    if not skill_name:
        return redirect(url_for('dashboard'))

    conn = get_db()
    cursor = conn.cursor()

    # Check if skill already exists for user
    cursor.execute('SELECT * FROM user_skills WHERE user_id = ? AND skill_name = ?',
                  (session['user_id'], skill_name))
    if cursor.fetchone():
        conn.close()
        return redirect(url_for('dashboard'))

    cursor.execute('INSERT INTO user_skills (user_id, skill_name) VALUES (?, ?)',
                  (session['user_id'], skill_name))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/delete_skill/<int:skill_id>')
def delete_skill(skill_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM user_skills WHERE id = ? AND user_id = ?',
                  (skill_id, session['user_id']))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/quiz')
def quiz():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    skill = request.args.get('skill', 'Python')
    from model import get_quiz_questions
    quiz_questions = get_quiz_questions(skill)
    return render_template('quiz.html', skill=skill, quiz_questions=quiz_questions)

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    skill = data.get('skill')
    score = data.get('score')
    total = data.get('total')

    # Calculate skill level
    skill_level = get_skill_level(score, total)

    conn = get_db()
    cursor = conn.cursor()

    # Save quiz result
    cursor.execute('''INSERT INTO quiz_results (user_id, skill_name, score, total_questions, skill_level)
                     VALUES (?, ?, ?, ?, ?)''',
                  (session['user_id'], skill, score, total, skill_level))

    # Update user skill level
    cursor.execute('''UPDATE user_skills SET skill_level = ?
                     WHERE user_id = ? AND skill_name = ?''',
                  (skill_level, session['user_id'], skill))

    conn.commit()
    conn.close()

    return jsonify({
        'success': True,
        'skill_level': skill_level,
        'score': score,
        'total': total
    })

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/chat_message', methods=['POST'])
def chat_message():
    if 'user_id' not in session:
        return jsonify({'error': 'Not logged in'}), 401

    data = request.json
    user_message = data.get('message', '')

    # Get user skills for context
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT skill_name FROM user_skills WHERE user_id = ?', (session['user_id'],))
    skills = [row['skill_name'] for row in cursor.fetchall()]
    conn.close()

    # Get AI response
    response = get_chat_response(user_message, skills)

    return jsonify({'response': response})

if __name__ == '__main__':
    if not os.path.exists(DATABASE):
        init_db()
        print('Database initialized!')
    app.run(debug=True, host='127.0.0.1', port=5000)
