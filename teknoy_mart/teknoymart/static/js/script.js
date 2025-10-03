document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const emailInput = document.getElementById("email");

  // ---------- simple institutional email validator ----------
  function validateInstitutionalEmail(el) {
    el.setCustomValidity(""); // clear previous

    const v = (el.value || "").trim().toLowerCase();
    if (!v) return;
    if (!v.includes("@")) return;

    const allowed = ["cit.edu", "cit.edu.ph"];
    const domain = v.split("@")[1];
    if (!allowed.includes(domain)) {
      el.setCustomValidity("Must be institutional email (@cit.edu or @cit.edu.ph)");
    }
  }

  emailInput?.addEventListener("input", () => validateInstitutionalEmail(emailInput));
  emailInput?.addEventListener("invalid", () => validateInstitutionalEmail(emailInput));

  // ---------- Form submission ----------
  form?.addEventListener("submit", function (e) {
    let valid = true;

    const firstName = document.getElementById("first_name")?.value.trim();
    const lastName = document.getElementById("full_name")?.value.trim();
    const studentId = document.getElementById("student_id")?.value.trim();
    const password = document.getElementById("password")?.value;
    const confirmPassword = document.getElementById("confirm_password")?.value;

    // Email check
    validateInstitutionalEmail(emailInput);
    if (emailInput && !emailInput.checkValidity()) {
      emailInput.reportValidity();
      valid = false;
    }

    // Student ID format check
    const idPattern = /^\d{2}-\d{4}-\d{3}$/;
    if (studentId && !idPattern.test(studentId)) {
      alert("Student ID must be in format: xx-xxxx-xxx");
      valid = false;
    }

    // Password match
    if (password !== confirmPassword) {
      alert("Passwords do not match!");
      valid = false;
    }

    if (!valid) e.preventDefault();
  });

  // ---------- UI Enhancements ----------
  // 1. Ripple effect on buttons
  document.querySelectorAll(".btn").forEach(btn => {
    btn.addEventListener("click", function (e) {
      const circle = document.createElement("span");
      circle.classList.add("ripple");
      circle.style.left = `${e.clientX - btn.offsetLeft}px`;
      circle.style.top = `${e.clientY - btn.offsetTop}px`;
      this.appendChild(circle);
      setTimeout(() => circle.remove(), 600);
    });
  });

  // 2. Fade-in animation for hero content
  const heroContent = document.querySelector(".hero-content");
  if (heroContent) {
    heroContent.style.opacity = 0;
    heroContent.style.transform = "translateY(30px)";
    setTimeout(() => {
      heroContent.style.transition = "all 1s ease";
      heroContent.style.opacity = 1;
      heroContent.style.transform = "translateY(0)";
    }, 200);
  }

  // 3. Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      document.querySelector(this.getAttribute("href")).scrollIntoView({
        behavior: "smooth"
      });
    });
  });

  // 4. Input valid/invalid glow
  document.querySelectorAll("input, select").forEach(input => {
    input.addEventListener("blur", () => {
      if (input.checkValidity()) {
        input.style.boxShadow = "0 0 6px rgba(0, 128, 0, 0.4)";
      } else {
        input.style.boxShadow = "0 0 6px rgba(255, 0, 0, 0.4)";
      }
      setTimeout(() => input.style.boxShadow = "none", 1000);
    });
  });
});
