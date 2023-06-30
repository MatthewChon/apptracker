function drop_submission_form() {
    const submission_form_elem = document.getElementById("submission-form");
    submission_form_elem.classList.add("open");
}
function exit_submission_form() {
    const submission_form_elem = document.getElementById("submission-form");
    submission_form_elem.reset();
    submission_form_elem.classList.remove("open");
}