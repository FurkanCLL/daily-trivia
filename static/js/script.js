document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit-button");
    const nextButton = document.getElementById("next-button");
    const quizForm = document.getElementById("quiz-form");
    const correctAnswer = quizForm.dataset.correct;
    const options = document.querySelectorAll(".quiz-option-label input");

    options.forEach(option => {
        option.addEventListener("change", function () {
            options.forEach(opt => opt.nextElementSibling.classList.remove("selected"));
            this.nextElementSibling.classList.add("selected");
        });
    });

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();

        const selectedOption = document.querySelector(".quiz-option-label input:checked");
        if (!selectedOption) {
            alert("Please select an answer before submitting!");
            return;
        }

        const selectedValue = selectedOption.value;
        const selectedLabel = selectedOption.nextElementSibling;
        const correctLabel = document.querySelector(`.quiz-option-label input[value='${correctAnswer}']`).nextElementSibling;

        if (selectedValue === correctAnswer) {
            selectedLabel.classList.add("correct");
        } else {
            selectedLabel.classList.add("incorrect");
            correctLabel.classList.add("correct");
        }

        submitButton.style.display = "none";
        nextButton.style.display = "inline-block";
    });
});
