// Show a custom message if the email isn't institutional
function validateInstitutionalEmail(el) {
  // Clear any previous custom message
  el.setCustomValidity("");

  const v = (el.value || "").trim().toLowerCase();
  if (!v) return;               // let "Please fill out this field." handle empty
  if (!v.includes("@")) return; // let browser handle missing @ / bad format

  const allowed = ["cit.edu", "cit.edu.ph"];
  const domain = v.split("@")[1];

  if (!allowed.includes(domain)) {
    el.setCustomValidity("Please use institutional email (@cit.edu or @cit.edu.ph).");
  }
}

// Ensure the message shows when clicking Register
document.addEventListener("DOMContentLoaded", () => {
  const form  = document.getElementById("registerForm");
  const email = document.getElementById("email");
  if (!form || !email) return;

  form.addEventListener("submit", (e) => {
    validateInstitutionalEmail(email);
    if (!form.checkValidity()) {
      e.preventDefault();       // stop submit
      email.reportValidity();   // show the bubble
    }
  });
});
