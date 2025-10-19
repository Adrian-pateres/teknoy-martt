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

// --- Category + search filtering on home page ---
document.addEventListener("DOMContentLoaded", () => {
  const chips = Array.from(document.querySelectorAll(".cat-filter .chip"));
  const cards = Array.from(document.querySelectorAll(".product-card"));
  const search = document.getElementById("productSearch");

  if (!chips.length || !cards.length) return;

  let activeCat = "all";

  function applyFilters() {
    const q = (search?.value || "").trim().toLowerCase();

    cards.forEach(card => {
      const cat = (card.dataset.cat || "").toLowerCase();
      const name = (card.dataset.name || "").toLowerCase();

      const matchCat = activeCat === "all" || cat === activeCat;
      const matchQuery = !q || name.includes(q) || cat.includes(q);

      card.style.display = (matchCat && matchQuery) ? "" : "none";
    });
  }

  // Chip clicks
  chips.forEach(btn => {
    btn.addEventListener("click", () => {
      chips.forEach(c => { c.classList.remove("active"); c.setAttribute("aria-pressed", "false"); });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      activeCat = (btn.dataset.cat || "all").toLowerCase();
      applyFilters();
    });
  });

  // Search input
  if (search) {
    search.addEventListener("input", applyFilters);
  }
});
