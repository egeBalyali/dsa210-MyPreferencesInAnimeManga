function loadQuiz() {
    // Loop through quizData to populate each question
    quizData.forEach((quiz) => {
        const quizContainer = document.getElementById(`quiz${quiz.id}`);
        if (quizContainer) {
            quizContainer.innerHTML = `
                <h3>${quiz.question}</h3>
                ${quiz.options
                    .map(
                        (option) => `
                            <label>
                                <input type="radio" name="question${quiz.id}" value="${option}">
                                ${option}
                            </label><br>
                        `
                    )
                    .join('')}
            `;
        }
    });
}

function calculateQuizScore() {
    let score = 0;

    // Loop through the quizData to check answers
    quizData.forEach((quiz) => {
        const selectedOption = document.querySelector(
            `input[name="question${quiz.id}"]:checked`
        );
        if (selectedOption && selectedOption.value === quiz.correct) {
            score++;
        }
    });

    return score;
}

// Display the score when user submits the quiz
document.getElementById("submitQuiz").addEventListener("click", () => {
    const score = calculateQuizScore();
    alert(`You scored ${score} out of ${quizData.length}!`);
});

// Load quiz when the page loads
window.onload = loadQuiz;
