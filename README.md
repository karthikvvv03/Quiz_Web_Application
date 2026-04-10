# Quiz Master Flask App

A simple Flask quiz application with user authentication, randomized coding quiz questions, instant answer feedback, and score reporting.

## Features

- User registration and login with session-based authentication
- Password hashing using Werkzeug for basic credential security
- Randomized quiz questions from multiple topics:
  - JavaScript
  - Web APIs
  - Data Structures
  - CSS
  - REST APIs
  - Python
  - Algorithms
  - Async Programming
  - SQL
  - Express.js
- Interactive quiz interface with progress tracking
- Immediate answer feedback and optional explanations
- Score summary at the end of the quiz

## Project Structure

- `app.py` - Flask backend with authentication, question serving, and quiz submission logic
- `templates/` - HTML templates for login, registration, and quiz interface
  - `index.html`
  - `login.html`
  - `register.html`
- `static/` - Frontend assets
  - `script.js` - quiz client logic and API interactions
  - `style.css` - UI styling
- `requirements.txt` - project dependencies

## Requirements

- Python 3.8+
- Flask
- Werkzeug

> Note: `requirements.txt` is currently empty. Install dependencies manually or add them to the file after verifying the virtual environment.

## Setup

1. Create and activate a Python virtual environment:

   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

2. Install the required packages:

   ```bash
   pip install Flask Werkzeug
   ```

3. (Optional) Add dependencies to `requirements.txt`:

   ```bash
   pip freeze > requirements.txt
   ```

## Run the App

Start the Flask application:

```bash
python app.py
```

Then open `http://127.0.0.1:5000` in your browser.

## Using the App

1. Register a new account.
2. Log in using your credentials.
3. Click **Get Started** to begin the quiz.
4. Answer each question, view feedback, and reveal explanations.
5. Submit the quiz to see your final score.

## Notes

- This app uses in-memory user storage for demonstration only; user accounts are lost when the app restarts.
- The secret key in `app.py` is for development only and should be changed for production use.
- For production, replace the in-memory `users` dictionary with a persistent database and handle session storage securely.
