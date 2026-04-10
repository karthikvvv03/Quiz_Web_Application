from flask import Flask, render_template, jsonify, request, session, redirect, url_for, flash
import random
import os
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'dev-secret-key-change-in-production-12345'
app.config['SESSION_TYPE'] = 'filesystem'

# Simple in-memory user storage (in production, use a database)
users = {}

# Questions data - 2-3 questions per topic
questions_by_topic = {
    "JavaScript": [
        {
            "question": "What is the difference between 'let' and 'var' in JavaScript?",
            "options": ["No difference", "'let' has block scope, 'var' has function scope", "'var' is faster than 'let'", "'let' cannot be redeclared, 'var' can"],
            "answer": "'let' has block scope, 'var' has function scope",
            "topic": "JavaScript",
            "explanation": "'let' is block-scoped (limited to the block where it's declared), while 'var' is function-scoped (accessible throughout the entire function)."
        },
        {
            "question": "What is the output of 'console.log(typeof null)' in JavaScript?",
            "options": ["null", "undefined", "object", "boolean"],
            "answer": "object",
            "topic": "JavaScript",
            "explanation": "This is a well-known quirk in JavaScript. Despite null being a primitive value, typeof null returns 'object' due to a bug in the original JavaScript implementation."
        },
        {
            "question": "Which method is used to add an element to the end of an array in JavaScript?",
            "options": ["push()", "pop()", "shift()", "unshift()"],
            "answer": "push()",
            "topic": "JavaScript",
            "explanation": "The push() method adds one or more elements to the end of an array and returns the new length of the array."
        }
    ],
    "Web APIs": [
        {
            "question": "Which HTTP method is used to partially update a resource?",
            "options": ["PUT", "PATCH", "POST", "UPDATE"],
            "answer": "PATCH",
            "topic": "Web APIs",
            "explanation": "PATCH is used for partial updates to a resource, while PUT replaces the entire resource. PATCH is more efficient for small changes."
        },
        {
            "question": "What does the HTTP status code 404 mean?",
            "options": ["Server Error", "Not Found", "Unauthorized", "Bad Request"],
            "answer": "Not Found",
            "topic": "Web APIs",
            "explanation": "HTTP 404 status code indicates that the server cannot find the requested resource. It's commonly seen when a URL doesn't exist."
        },
        {
            "question": "Which HTTP method is idempotent and used to retrieve data?",
            "options": ["POST", "PUT", "GET", "DELETE"],
            "answer": "GET",
            "topic": "Web APIs",
            "explanation": "GET is idempotent (multiple identical requests have the same effect) and is used to retrieve data from a server without modifying it."
        }
    ],
    "Data Structures": [
        {
            "question": "What is the time complexity of accessing an element in a hash table?",
            "options": ["O(n)", "O(1) on average", "O(log n)", "O(n²)"],
            "answer": "O(1) on average",
            "topic": "Data Structures",
            "explanation": "Hash tables provide average O(1) time complexity for access operations due to direct indexing using hash functions."
        },
        {
            "question": "Which data structure follows LIFO (Last In, First Out) principle?",
            "options": ["Queue", "Stack", "Array", "Linked List"],
            "answer": "Stack",
            "topic": "Data Structures",
            "explanation": "A Stack follows LIFO principle - the last element added is the first one to be removed, like a stack of plates."
        },
        {
            "question": "What is the worst-case time complexity of Quick Sort?",
            "options": ["O(n log n)", "O(n²)", "O(n)", "O(log n)"],
            "answer": "O(n²)",
            "topic": "Data Structures",
            "explanation": "Quick Sort has O(n²) worst-case complexity when the pivot selection is poor, but O(n log n) on average with good pivot selection."
        }
    ],
    "CSS": [
        {
            "question": "Which of the following is NOT a CSS pseudo-class?",
            "options": [":hover", ":focus", ":active", ":colors"],
            "answer": ":colors",
            "topic": "CSS",
            "explanation": ":hover, :focus, and :active are valid CSS pseudo-classes, but :colors is not a standard pseudo-class."
        },
        {
            "question": "What does CSS stand for?",
            "options": ["Computer Style Sheets", "Cascading Style Sheets", "Creative Style Sheets", "Colorful Style Sheets"],
            "answer": "Cascading Style Sheets",
            "topic": "CSS",
            "explanation": "CSS stands for Cascading Style Sheets - a style sheet language used for describing the presentation of a document written in HTML."
        },
        {
            "question": "Which CSS property is used to create space between elements?",
            "options": ["margin", "padding", "border", "spacing"],
            "answer": "margin",
            "topic": "CSS",
            "explanation": "The margin property creates space around elements, outside of any defined borders, while padding creates space inside elements."
        }
    ],
    "REST APIs": [
        {
            "question": "What does 'REST' stand for in API design?",
            "options": ["Representational State Transfer", "Remote Execution System Transfer", "Resource Exchange System Technology", "Rapid Event State Transmission"],
            "answer": "Representational State Transfer",
            "topic": "REST APIs",
            "explanation": "REST stands for Representational State Transfer - an architectural style for designing networked applications."
        },
        {
            "question": "Which HTTP method is typically used to create a new resource?",
            "options": ["GET", "POST", "PUT", "DELETE"],
            "answer": "POST",
            "topic": "REST APIs",
            "explanation": "POST is used to create new resources on the server. It sends data to the server to create a new resource."
        },
        {
            "question": "What is the main principle of RESTful design?",
            "options": ["Everything is a resource", "Use only JSON", "No authentication", "Only GET requests"],
            "answer": "Everything is a resource",
            "topic": "REST APIs",
            "explanation": "In REST, everything is treated as a resource that can be identified by a URI and manipulated using standard HTTP methods."
        }
    ],
    "Python": [
        {
            "question": "In Python, what is the output of list(map(lambda x: x**2, [1, 2, 3]))?",
            "options": ["[1, 2, 3]", "[1, 4, 9]", "[2, 4, 6]", "[1, 4, 9, 16]"],
            "answer": "[1, 4, 9]",
            "topic": "Python",
            "explanation": "The map() function applies the lambda function (x**2) to each element in the list [1, 2, 3], resulting in [1, 4, 9]."
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "options": ["function", "def", "func", "define"],
            "answer": "def",
            "topic": "Python",
            "explanation": "In Python, functions are defined using the 'def' keyword followed by the function name and parameters."
        },
        {
            "question": "What is the correct way to create a list in Python?",
            "options": ["list = []", "list = {}", "list = ()", "list = <>"],
            "answer": "list = []",
            "topic": "Python",
            "explanation": "In Python, lists are created using square brackets []. Curly braces {} create dictionaries, parentheses () create tuples."
        }
    ],
    "Algorithms": [
        {
            "question": "Which sorting algorithm has the best average-case time complexity?",
            "options": ["Bubble Sort O(n²)", "Quick Sort O(n log n)", "Merge Sort O(n log n)", "Both Quick and Merge Sort"],
            "answer": "Both Quick and Merge Sort",
            "topic": "Algorithms",
            "explanation": "Both Quick Sort and Merge Sort have O(n log n) average-case time complexity, which is optimal for comparison-based sorting."
        },
        {
            "question": "What is the time complexity of Binary Search?",
            "options": ["O(n)", "O(n log n)", "O(log n)", "O(n²)"],
            "answer": "O(log n)",
            "topic": "Algorithms",
            "explanation": "Binary Search has O(log n) time complexity because it repeatedly divides the search space in half with each comparison."
        },
        {
            "question": "Which algorithm is used to find the shortest path in a graph?",
            "options": ["Dijkstra's Algorithm", "Bubble Sort", "Binary Search", "Quick Sort"],
            "answer": "Dijkstra's Algorithm",
            "topic": "Algorithms",
            "explanation": "Dijkstra's Algorithm finds the shortest path between nodes in a graph with non-negative edge weights."
        }
    ],
    "Async Programming": [
        {
            "question": "What is the purpose of the 'async' keyword in JavaScript?",
            "options": ["Makes code run faster", "Marks a function that returns a Promise", "Makes loops asynchronous", "Prevents function execution"],
            "answer": "Marks a function that returns a Promise",
            "topic": "Async Programming",
            "explanation": "The 'async' keyword declares an asynchronous function that implicitly returns a Promise, allowing the use of 'await' inside it."
        },
        {
            "question": "Which keyword is used to wait for a Promise to resolve?",
            "options": ["wait", "await", "pause", "delay"],
            "answer": "await",
            "topic": "Async Programming",
            "explanation": "'await' pauses the execution of an async function until the Promise is resolved or rejected."
        },
        {
            "question": "What does Promise.all() do?",
            "options": ["Runs promises sequentially", "Runs promises in parallel and waits for all", "Cancels all promises", "Returns the first resolved promise"],
            "answer": "Runs promises in parallel and waits for all",
            "topic": "Async Programming",
            "explanation": "Promise.all() takes an array of promises and returns a single promise that resolves when all input promises have resolved."
        }
    ],
    "SQL": [
        {
            "question": "In SQL, which clause is used to filter groups?",
            "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"],
            "answer": "HAVING",
            "topic": "SQL",
            "explanation": "HAVING is used to filter groups created by GROUP BY, while WHERE filters individual rows before grouping."
        },
        {
            "question": "Which SQL command is used to retrieve data from a database?",
            "options": ["INSERT", "UPDATE", "DELETE", "SELECT"],
            "answer": "SELECT",
            "topic": "SQL",
            "explanation": "SELECT is the SQL command used to query and retrieve data from database tables."
        },
        {
            "question": "What does JOIN do in SQL?",
            "options": ["Creates a new table", "Combines rows from two or more tables", "Deletes duplicate rows", "Sorts the table"],
            "answer": "Combines rows from two or more tables",
            "topic": "SQL",
            "explanation": "JOIN combines rows from two or more tables based on a related column between them."
        }
    ],
    "Express.js": [
        {
            "question": "What is the purpose of middleware in Express.js?",
            "options": ["To style web pages", "To process requests and responses", "To store data", "To create databases"],
            "answer": "To process requests and responses",
            "topic": "Express.js",
            "explanation": "Middleware functions have access to the request and response objects and can modify them or execute code during the request-response cycle."
        },
        {
            "question": "Which method is used to define a route in Express.js?",
            "options": ["route()", "path()", "app.get()", "express.route()"],
            "answer": "app.get()",
            "topic": "Express.js",
            "explanation": "app.get() defines a route that handles GET requests to a specific path. Similar methods exist for other HTTP methods like app.post(), app.put(), etc."
        },
        {
            "question": "What does req.body contain in Express.js?",
            "options": ["URL parameters", "Request headers", "Request body data", "Response data"],
            "answer": "Request body data",
            "topic": "Express.js",
            "explanation": "req.body contains the parsed request body data, typically from POST or PUT requests, after using middleware like express.json()."
        }
    ]
}

def get_shuffled_questions():
    """Return one random question from each of 5 different topics"""
    selected_questions = []
    topics = list(questions_by_topic.keys())

    # Select 5 random topics
    selected_topics = random.sample(topics, min(5, len(topics)))

    # Get one random question from each selected topic
    for topic in selected_topics:
        question = random.choice(questions_by_topic[topic])
        selected_questions.append(question)

    # Shuffle the questions
    random.shuffle(selected_questions)
    return selected_questions

@app.route('/')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/debug')
def debug():
    return {
        'session': dict(session),
        'username_in_session': 'username' in session,
        'current_user': session.get('username')
    }

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username], password):
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match')
            return redirect(url_for('register'))

        if username in users:
            flash('Username already exists')
            return redirect(url_for('register'))

        users[username] = generate_password_hash(password)
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Send shuffled questions to frontend
@app.route('/get_questions')
def get_questions():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    questions = get_shuffled_questions()
    # Store questions in session for verification
    session['questions'] = questions
    return jsonify(questions)

# Check answers and return score
@app.route('/submit', methods=['POST'])
def submit():
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401

    try:
        questions = session.get('questions', [])
        user_answers = request.json
        score = 0

        for i in range(len(questions)):
            if i < len(user_answers) and user_answers[i] == questions[i]["answer"]:
                score += 1

        return jsonify({"score": score, "total": len(questions)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)