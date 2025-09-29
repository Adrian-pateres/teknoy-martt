document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("registerForm");

    form.addEventListener("submit", function (e) {
        let valid = true;

        const firstName = document.getElementById("first_name").value.trim();
        const lastName = document.getElementById("last_name").value.trim();
        const email = document.getElementById("email").value.trim();
        const studentId = document.getElementById("student_id").value.trim();
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;

        // Email format check: firstname.lastname@cit.edu
        const emailPattern = new RegExp(`^${firstName.toLowerCase()}\\.${lastName.toLowerCase()}@cit\\.edu$`);
        if (!emailPattern.test(email)) {
            alert("Email must be in format: firstname.lastname@cit.edu");
            valid = false;
        }

        // Student ID format check: xx-xxxx-xxx
        const idPattern = /^\d{2}-\d{4}-\d{3}$/;
        if (!idPattern.test(studentId)) {
            alert("Student ID must be in format: xx-xxxx-xxx");
            valid = false;
        }

        // Password match check
        if (password !== confirmPassword) {
            alert("Passwords do not match!");
            valid = false;
        }

        if (!valid) e.preventDefault();
    });
});
