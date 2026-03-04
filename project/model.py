from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class CourseRecommender:
    def __init__(self):
        # Sample course database with skills and descriptions
        self.courses = [
            {
                'id': 1,
                'name': 'Python for Beginners',
                'skills': 'python programming basics variables functions',
                'level': 'Beginner',
                'description': 'Learn Python fundamentals from scratch'
            },
            {
                'id': 2,
                'name': 'Advanced Python Programming',
                'skills': 'python advanced oop decorators generators',
                'level': 'Advanced',
                'description': 'Master advanced Python concepts'
            },
            {
                'id': 3,
                'name': 'Java Programming Masterclass',
                'skills': 'java programming oop inheritance polymorphism',
                'level': 'Intermediate',
                'description': 'Complete Java programming course'
            },
            {
                'id': 4,
                'name': 'JavaScript Full Course',
                'skills': 'javascript programming web development frontend',
                'level': 'Beginner',
                'description': 'Learn JavaScript for web development'
            },
            {
                'id': 5,
                'name': 'Machine Learning with Python',
                'skills': 'python machine-learning scikit-learn data-science',
                'level': 'Advanced',
                'description': 'Build ML models with Python'
            },
            {
                'id': 6,
                'name': 'Data Structures and Algorithms',
                'skills': 'algorithms data-structures python java programming',
                'level': 'Intermediate',
                'description': 'Master DSA concepts'
            },
            {
                'id': 7,
                'name': 'Web Development Bootcamp',
                'skills': 'html css javascript react web-development',
                'level': 'Beginner',
                'description': 'Full stack web development'
            },
            {
                'id': 8,
                'name': 'SQL Database Design',
                'skills': 'sql database mysql postgresql data',
                'level': 'Intermediate',
                'description': 'Learn database design and SQL'
            },
            {
                'id': 9,
                'name': 'React Frontend Development',
                'skills': 'react javascript frontend web-development',
                'level': 'Intermediate',
                'description': 'Build modern web apps with React'
            },
            {
                'id': 10,
                'name': 'Django Web Framework',
                'skills': 'python django web-development backend',
                'level': 'Intermediate',
                'description': 'Build web apps with Django'
            },
            {
                'id': 11,
                'name': 'C++ Programming',
                'skills': 'cpp c++ programming oop algorithms',
                'level': 'Intermediate',
                'description': 'Learn C++ programming'
            },
            {
                'id': 12,
                'name': 'Cloud Computing AWS',
                'skills': 'aws cloud devops deployment',
                'level': 'Advanced',
                'description': 'Master AWS cloud services'
            }
        ]

        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()
        self.course_vectors = self.vectorizer.fit_transform([c['skills'] for c in self.courses])

    def recommend_courses(self, user_skills, top_n=5):
        if not user_skills:
            # Return beginner courses if no skills
            return [c for c in self.courses if c['level'] == 'Beginner'][:top_n]

        # Convert user skills to a single string
        user_skills_text = ' '.join([skill.lower() for skill in user_skills])

        # Transform user skills to vector
        user_vector = self.vectorizer.transform([user_skills_text])

        # Calculate similarity scores
        similarities = cosine_similarity(user_vector, self.course_vectors)[0]

        # Get top N course indices
        top_indices = np.argsort(similarities)[::-1][:top_n]

        # Return recommended courses with similarity scores
        recommendations = []
        for idx in top_indices:
            course = self.courses[idx].copy()
            course['similarity'] = round(similarities[idx] * 100, 2)
            recommendations.append(course)

        return recommendations


def get_skill_level(score, total):
    """Determine skill level based on quiz score"""
    percentage = (score / total) * 100

    if percentage >= 80:
        return 'Advanced'
    elif percentage >= 60:
        return 'Intermediate'
    else:
        return 'Beginner'


def get_chat_response(user_message, user_skills=None):
    """Rule-based chatbot for learning assistance"""
    message = user_message.lower().strip()

    # Greeting patterns
    if any(word in message for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! I'm your AI Learning Assistant. How can I help you today? You can ask me about courses, learning tips, or programming concepts!"

    # Course recommendation patterns
    elif any(word in message for word in ['recommend', 'suggest', 'course', 'learn']):
        if user_skills:
            skills_text = ', '.join(user_skills)
            return f"Based on your skills ({skills_text}), I recommend checking your dashboard for personalized course recommendations. You can also add more skills to get better suggestions!"
        else:
            return "I'd love to recommend courses! First, please add your current skills on the dashboard so I can give you personalized recommendations."

    # Python related
    elif 'python' in message:
        if any(word in message for word in ['start', 'begin', 'learn']):
            return "Python is a great choice! Start with 'Python for Beginners' course. Focus on: variables, data types, loops, functions, and then move to OOP concepts. Practice daily on coding platforms!"
        else:
            return "Python is versatile! It's used for web development (Django/Flask), data science, machine learning, automation, and more. What aspect interests you?"

    # Java related
    elif 'java' in message:
        return "Java is excellent for enterprise applications! Key topics: OOP principles, collections, exception handling, multithreading. Practice with projects like building a library management system or calculator app."

    # JavaScript related
    elif 'javascript' in message or 'js' in message:
        return "JavaScript powers the web! Learn: ES6+ syntax, DOM manipulation, async programming, and frameworks like React or Vue. Build projects like to-do apps or interactive websites!"

    # Career/job related
    elif any(word in message for word in ['job', 'career', 'interview', 'hire', 'work']):
        return "Focus on: 1) Build a strong portfolio with 3-5 projects, 2) Master data structures & algorithms, 3) Practice on LeetCode/HackerRank, 4) Contribute to open source, 5) Network on LinkedIn!"

    # Study tips
    elif any(word in message for word in ['study', 'tip', 'advice', 'how to', 'improve']):
        return "Effective learning tips: 1) Practice coding daily (1-2 hours), 2) Build real projects, 3) Learn by teaching others, 4) Join coding communities, 5) Take regular breaks (Pomodoro technique), 6) Review and revise regularly!"

    # Data structures
    elif any(word in message for word in ['data structure', 'algorithm', 'dsa']):
        return "DSA is crucial! Start with: Arrays → Linked Lists → Stacks & Queues → Trees → Graphs → Hash Tables. Practice problems from easy to hard. Understand time/space complexity (Big O notation)."

    # Web development
    elif 'web' in message and 'development' in message:
        return "Web development path: 1) HTML/CSS basics, 2) JavaScript fundamentals, 3) Frontend framework (React/Vue), 4) Backend (Node.js/Python), 5) Databases (SQL/MongoDB), 6) Version control (Git). Build full-stack projects!"

    # Quiz related
    elif 'quiz' in message or 'test' in message:
        return "Take quizzes to assess your skill level! Navigate to the Quiz section from your dashboard. Based on your score, I'll recommend appropriate courses for your level."

    # Help/features
    elif any(word in message for word in ['help', 'feature', 'what can you', 'how does']):
        return "I can help you with: 📚 Course recommendations, 💡 Learning tips, 🎯 Study advice, 💻 Programming guidance, 📊 Skill assessment via quizzes. Ask me anything about learning programming!"

    # Motivation
    elif any(word in message for word in ['motivate', 'difficult', 'hard', 'give up', 'frustrated']):
        return "Don't give up! Every expert was once a beginner. Programming is challenging but rewarding. Take breaks, celebrate small wins, and remember: bugs are learning opportunities! You're doing great by being here! 💪"

    # Thanks
    elif any(word in message for word in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! I'm here to help you succeed in your learning journey. Keep learning and coding! 🚀"

    # Default response
    else:
        return "I'm here to help with your learning journey! You can ask me about: course recommendations, programming languages (Python, Java, JavaScript), study tips, career advice, or web development. What would you like to know?"


# Quiz questions database
QUIZ_QUESTIONS = {
    'Python': [
        {
            'question': 'What is the correct way to create a function in Python?',
            'options': ['function myFunc():', 'def myFunc():', 'create myFunc():', 'fun myFunc():'],
            'answer': 1
        },
        {
            'question': 'Which of these is NOT a valid Python data type?',
            'options': ['int', 'float', 'char', 'str'],
            'answer': 2
        },
        {
            'question': 'What does the len() function do?',
            'options': ['Returns length of object', 'Creates a list', 'Deletes an item', 'Sorts a list'],
            'answer': 0
        },
        {
            'question': 'How do you create a list in Python?',
            'options': ['list = ()', 'list = {}', 'list = []', 'list = <>'],
            'answer': 2
        },
        {
            'question': 'What is the output of: print(2 ** 3)?',
            'options': ['6', '8', '9', '5'],
            'answer': 1
        },
        {
            'question': 'Which keyword is used for exception handling?',
            'options': ['try', 'catch', 'handle', 'error'],
            'answer': 0
        },
        {
            'question': 'What does "self" represent in a Python class?',
            'options': ['The class itself', 'The instance of class', 'A keyword', 'A function'],
            'answer': 1
        },
        {
            'question': 'Which method is called when object is created?',
            'options': ['__start__', '__init__', '__create__', '__new__'],
            'answer': 1
        },
        {
            'question': 'How do you comment in Python?',
            'options': ['//', '/* */', '#', '--'],
            'answer': 2
        },
        {
            'question': 'What is the correct way to import a module?',
            'options': ['include module', 'import module', 'using module', 'require module'],
            'answer': 1
        }
    ],
    'Java': [
        {
            'question': 'Which of these is the correct way to declare a variable in Java?',
            'options': ['int x = 5;', 'x = 5;', 'var int x = 5;', 'declare x = 5;'],
            'answer': 0
        },
        {
            'question': 'What is the parent class of all classes in Java?',
            'options': ['System', 'Main', 'Object', 'Parent'],
            'answer': 2
        },
        {
            'question': 'Which keyword is used for inheritance?',
            'options': ['inherits', 'extends', 'implements', 'inherit'],
            'answer': 1
        },
        {
            'question': 'What is the size of int in Java?',
            'options': ['16 bits', '32 bits', '64 bits', '8 bits'],
            'answer': 1
        },
        {
            'question': 'Which of these is NOT an access modifier?',
            'options': ['public', 'private', 'protected', 'package'],
            'answer': 3
        },
        {
            'question': 'What does JVM stand for?',
            'options': ['Java Visual Machine', 'Java Virtual Machine', 'Java Variable Method', 'Java Version Manager'],
            'answer': 1
        },
        {
            'question': 'Which method is the entry point of Java program?',
            'options': ['start()', 'run()', 'main()', 'execute()'],
            'answer': 2
        },
        {
            'question': 'What is the correct way to create an array?',
            'options': ['int[] arr = new int[5];', 'int arr[5];', 'array int arr[5];', 'int arr = new array[5];'],
            'answer': 0
        },
        {
            'question': 'Which package is imported by default?',
            'options': ['java.util', 'java.io', 'java.lang', 'java.net'],
            'answer': 2
        },
        {
            'question': 'What is encapsulation?',
            'options': ['Data hiding', 'Inheritance', 'Polymorphism', 'Abstraction'],
            'answer': 0
        }
    ],
    'JavaScript': [
        {
            'question': 'How do you declare a variable in JavaScript?',
            'options': ['var x;', 'variable x;', 'int x;', 'declare x;'],
            'answer': 0
        },
        {
            'question': 'Which method is used to parse a string to integer?',
            'options': ['parseInt()', 'parseInteger()', 'toInt()', 'convert()'],
            'answer': 0
        },
        {
            'question': 'What is the correct way to write an array?',
            'options': ['var arr = (1,2,3);', 'var arr = {1,2,3};', 'var arr = [1,2,3];', 'var arr = <1,2,3>;'],
            'answer': 2
        },
        {
            'question': 'Which operator is used for strict equality?',
            'options': ['==', '===', '=', '!='],
            'answer': 1
        },
        {
            'question': 'How do you create a function?',
            'options': ['function myFunc()', 'def myFunc()', 'create function myFunc()', 'func myFunc()'],
            'answer': 0
        },
        {
            'question': 'What does DOM stand for?',
            'options': ['Document Object Model', 'Data Object Model', 'Document Oriented Model', 'Dynamic Object Model'],
            'answer': 0
        },
        {
            'question': 'Which method adds an element to end of array?',
            'options': ['push()', 'add()', 'append()', 'insert()'],
            'answer': 0
        },
        {
            'question': 'What is the result of: typeof []?',
            'options': ['array', 'object', 'list', 'collection'],
            'answer': 1
        },
        {
            'question': 'How do you write a comment in JavaScript?',
            'options': ['//', '#', '<!-- -->', '/* only */'],
            'answer': 0
        },
        {
            'question': 'Which keyword declares a constant?',
            'options': ['const', 'constant', 'let', 'final'],
            'answer': 0
        }
    ],
    'Default': [
        {
            'question': 'What does HTML stand for?',
            'options': ['Hyper Text Markup Language', 'High Tech Modern Language', 'Home Tool Markup Language', 'Hyperlinks Text Mark Language'],
            'answer': 0
        },
        {
            'question': 'Which is a programming language?',
            'options': ['HTML', 'CSS', 'Python', 'XML'],
            'answer': 2
        },
        {
            'question': 'What does CPU stand for?',
            'options': ['Central Processing Unit', 'Computer Personal Unit', 'Central Program Utility', 'Computer Processing Unit'],
            'answer': 0
        },
        {
            'question': 'What is an algorithm?',
            'options': ['A programming language', 'Step-by-step procedure', 'A data structure', 'A compiler'],
            'answer': 1
        },
        {
            'question': 'Which of these is a database?',
            'options': ['Python', 'MySQL', 'Java', 'CSS'],
            'answer': 1
        },
        {
            'question': 'What does API stand for?',
            'options': ['Application Programming Interface', 'Advanced Programming Integration', 'Application Process Integration', 'Automated Programming Interface'],
            'answer': 0
        },
        {
            'question': 'What is Git used for?',
            'options': ['Database management', 'Version control', 'Web design', 'Debugging'],
            'answer': 1
        },
        {
            'question': 'What does IDE stand for?',
            'options': ['Integrated Development Environment', 'Internet Development Editor', 'Interactive Design Environment', 'Integrated Design Editor'],
            'answer': 0
        },
        {
            'question': 'Which is an object-oriented language?',
            'options': ['HTML', 'CSS', 'Java', 'SQL'],
            'answer': 2
        },
        {
            'question': 'What is debugging?',
            'options': ['Writing code', 'Testing software', 'Finding and fixing errors', 'Compiling code'],
            'answer': 2
        }
    ]
}

def get_quiz_questions(skill):
    """Get quiz questions for a specific skill"""
    return QUIZ_QUESTIONS.get(skill, QUIZ_QUESTIONS['Default'])
