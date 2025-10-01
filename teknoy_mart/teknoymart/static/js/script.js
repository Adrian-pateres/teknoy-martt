document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const emailInput = document.getElementById("email");

  // ---------- simple institutional email validator ----------
  function validateInstitutionalEmail(el) {
    // clear previous custom message
    el.setCustomValidity("");

    const v = (el.value || "").trim().toLowerCase();
    if (!v) return;                 // let "required" handle empty
    if (!v.includes("@")) return;   // let browser show its built-in "@ missing" message

    const allowed = ["cit.edu", "cit.edu.ph"];
    const domain = v.split("@")[1];
    if (!allowed.includes(domain)) {
      el.setCustomValidity("Must be institutional email (@cit.edu or @cit.edu.ph)");
    }
  }

  // live feedback while typing / when the browser validates the field
  emailInput.addEventListener("input", () => validateInstitutionalEmail(emailInput));
  emailInput.addEventListener("invalid", () => validateInstitutionalEmail(emailInput));

  // ---------------------------------------------------------

  form.addEventListener("submit", function (e) {
    let valid = true;

    const firstName = document.getElementById("first_name").value.trim();
    const lastName = document.getElementById("full_name").value.trim(); // your field name is full_name
    const studentId = document.getElementById("student_id").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirm_password").value;

    // Run institutional email check; if invalid, show the popup and block submit
    validateInstitutionalEmail(emailInput);
    if (!emailInput.checkValidity()) {
      emailInput.reportValidity(); // shows: "Must be institutional email ..."
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
