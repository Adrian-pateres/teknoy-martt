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

if (false) {
  renderDemoProducts();
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


// ================ HAMBURGER DROPDOWN ================
(function () {
  const btn   = document.getElementById('hamburgerBtn');
  const menu  = document.getElementById('userMenu');
  if (!btn || !menu) return;

  const close = () => {
    menu.classList.remove('open');
    btn.setAttribute('aria-expanded', 'false');
  };

  const open = () => {
    menu.classList.add('open');
    btn.setAttribute('aria-expanded', 'true');
  };

  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    menu.classList.contains('open') ? close() : open();
  });

  // click outside
  document.addEventListener('click', (e) => {
    if (!menu.classList.contains('open')) return;
    if (!menu.contains(e.target) && e.target !== btn) close();
  });

  // close with ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') close();
  });
})();

// ================ DARK MODE TOGGLE ================
(function () {
  const THEME_KEY = 'tm_theme';
  const root = document.documentElement;
  const btn = document.getElementById('menu-dark');

  function applySaved() {
    const t = localStorage.getItem(THEME_KEY) || 'light';
    root.setAttribute('data-theme', t);
    if (btn) btn.textContent = (t === 'dark') ? '☀️ Light Mode' : '🌙 Dark Mode';
  }

  function toggleTheme() {
    const next = (root.getAttribute('data-theme') === 'dark') ? 'light' : 'dark';
    root.setAttribute('data-theme', next);
    localStorage.setItem(THEME_KEY, next);
    if (btn) btn.textContent = (next === 'dark') ? '☀️ Light Mode' : '🌙 Dark Mode';
  }

  // initialize and wire up
  applySaved();
  if (btn) btn.addEventListener('click', toggleTheme);
})();