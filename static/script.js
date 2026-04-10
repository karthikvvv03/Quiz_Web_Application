let questions = [];
let currentQuestion = 0;
let selectedAnswers = [];
let answered = false;

const questionEl = document.getElementById("question");
const optionBtns = document.querySelectorAll(".option");
const nextBtn = document.getElementById("next");
const resultEl = document.getElementById("result");
const progressEl = document.getElementById("progress");
const progressFill = document.getElementById("progressFill");
const restartBtn = document.getElementById("restart");
const quizEl = document.getElementById("quiz");
const startScreenEl = document.getElementById("start-screen");
const startBtn = document.getElementById("start-btn");
const feedbackEl = document.getElementById("feedback");
const feedbackTextEl = document.getElementById("feedback-text");
const showExplanationBtn = document.getElementById("show-explanation");
const explanationEl = document.getElementById("explanation");

// Fetch questions initially (in background)
fetch("/get_questions", {
    credentials: 'include'
})
    .then(res => {
        if (!res.ok) {
            throw new Error('Authentication failed');
        }
        return res.json();
    })
    .then(data => {
        questions = data;
    })
    .catch(error => {
        console.error('Initial questions fetch failed:', error);
        // Don't show error here, handle it when user clicks start
    });

startBtn.onclick = () => {
    if (!questions.length) {
        startBtn.textContent = "Loading...";
        // Fetch questions if not loaded yet
        fetch("/get_questions", {
            credentials: 'include'
        })
            .then(res => {
                if (!res.ok) {
                    if (res.status === 401) {
                        throw new Error('Please login first');
                    }
                    throw new Error('Failed to load questions');
                }
                return res.json();
            })
            .then(data => {
                questions = data;
                startBtn.textContent = "Get Started";
                startScreenEl.classList.add("hide");
                quizEl.classList.remove("hide");
                loadQuestion();
            })
            .catch(error => {
                console.error('Error loading questions:', error);
                startBtn.textContent = "Error - Please Login";
                alert('Please login to access the quiz.');
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            });
        return;
    }
    startScreenEl.classList.add("hide");
    quizEl.classList.remove("hide");
    loadQuestion();
};

function loadQuestion() {
    let q = questions[currentQuestion];
    questionEl.textContent = q.question;
    const progressPercent = ((currentQuestion + 1) / questions.length) * 100;
    progressFill.style.width = progressPercent + "%";
    progressEl.textContent = `Question ${currentQuestion + 1} of ${questions.length}`;
    answered = false;

    // Reset styles and hide feedback
    optionBtns.forEach(btn => {
        btn.classList.remove("selected", "correct", "incorrect");
        btn.style.pointerEvents = "auto";
    });
    feedbackEl.classList.add("hide");
    explanationEl.classList.add("hide");
    showExplanationBtn.style.display = "inline-block";

    optionBtns.forEach((btn, index) => {
        btn.textContent = q.options[index];

        btn.onclick = () => {
            if (answered) return; // Prevent re-selecting

            // Remove selection from all
            optionBtns.forEach(b => b.classList.remove("selected"));

            // Add selection to clicked
            btn.classList.add("selected");

            // Store answer
            selectedAnswers[currentQuestion] = btn.textContent;
            answered = true;

            // Show feedback
            showFeedback(q.answer, q.explanation);
        };
    });
}

function showFeedback(correctAnswer, explanation) {
    const selectedAnswer = selectedAnswers[currentQuestion];
    const isCorrect = selectedAnswer === correctAnswer;

    // Show feedback text
    feedbackTextEl.textContent = isCorrect ? "✅ Correct Answer!😎" : "❌ Wrong Answer!☹️";
    feedbackTextEl.style.color = isCorrect ? "#00aa44" : "#ff4d4d";
    feedbackEl.classList.remove("hide");

    // Style the selected answer
    optionBtns.forEach(btn => {
        btn.style.pointerEvents = "none";

        if (btn.classList.contains("selected")) {
            btn.classList.add(isCorrect ? "correct" : "incorrect");
        }
    });

    // Set up explanation button
    showExplanationBtn.onclick = () => {
        explanationEl.textContent = explanation;
        explanationEl.classList.remove("hide");
        showExplanationBtn.style.display = "none";
    };

    nextBtn.textContent = currentQuestion === questions.length - 1 ? "Submit Quiz ✓" : "Next Question ➡️";
}

nextBtn.onclick = () => {
    // Prevent skipping without selecting
    if (!answered) {
        alert("Please select an answer!");
        return;
    }

    currentQuestion++;

    if (currentQuestion < questions.length) {
        loadQuestion();
    } else {
        submitQuiz();
    }
};

function submitQuiz() {
    fetch("/submit", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        credentials: 'include',
        body: JSON.stringify(selectedAnswers)
    })
    .then(res => res.json())
    .then(data => {
        quizEl.classList.add("hide");
        resultEl.classList.remove("hide");
        restartBtn.classList.remove("hide");

        const percentage = (data.score / data.total) * 100;
        let message = "";
        if (percentage === 100) {
            message = "🏆 Perfect Score! Outstanding!";
        } else if (percentage >= 80) {
            message = "🎉 Excellent Work!";
        } else if (percentage >= 60) {
            message = "👍 Good Job!";
        } else {
            message = "💪 Keep Practicing!";
        }

        resultEl.textContent = `${message}\n\n🎯 Your Score: ${data.score}/${data.total} (${percentage.toFixed(0)}%)`;
    });
}

restartBtn.onclick = () => {
    location.reload();
};