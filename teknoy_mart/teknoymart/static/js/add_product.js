// --- Institutional Email Validation ---
function validateInstitutionalEmail(el) {
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

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");
  const email = document.getElementById("email");
  if (form && email) {
    form.addEventListener("submit", (e) => {
      validateInstitutionalEmail(email);
      if (!form.checkValidity()) {
        e.preventDefault();       // stop submit
        email.reportValidity();   // show the bubble
      }
    });
  }
});

// --- Add Product Image Preview ---
function previewImage(event) {
  const input = event.target;
  const preview = document.getElementById("imagePreview");
  const uploadText = document.getElementById("uploadText");

  if (input.files && input.files[0]) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = "block";
      uploadText.style.display = "none";
    };
    reader.readAsDataURL(input.files[0]);
  } else {
    preview.src = "";
    preview.style.display = "none";
    uploadText.style.display = "block";
  }
}

// --- Form Validation / Modal Handling ---
function validateForm() {
  const form = document.getElementById("productForm");
  if (form.checkValidity()) {
    openModal("addModal");
  } else {
    form.reportValidity();
  }
}

function openModal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.add("open");           // uses CSS class instead of inline style
  document.body.style.overflow = "hidden"; // lock background scroll
}

function closeModal(id) {
  const el = document.getElementById(id);
  if (!el) return;
  el.classList.remove("open");
  // If no other modal is open, restore scroll
  if (!document.querySelector(".modal.open")) {
    document.body.style.overflow = "";
  }
}

function confirmAdd() {
  document.getElementById("productForm").submit();
}

function confirmCancel() {
  //fall back to seller home or root
  const url = window.CANCEL_URL || "/home/" || "/";
  window.location.href = url;
}

// --- Optional: Category + Search Filtering on Home Page ---
document.addEventListener("DOMContentLoaded", () => {
  const chips = Array.from(document.querySelectorAll(".cat-filter .chip"));
  const cards = Array.from(document.querySelectorAll(".product-card"));
  const search = document.getElementById("productSearch");

  if (!cards.length) return;

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
      chips.forEach(c => { 
        c.classList.remove("active"); 
        c.setAttribute("aria-pressed", "false"); 
      });
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


// Close when clicking the dark backdrop
document.addEventListener("click", (e) => {
  const modal = e.target.closest(".modal");
  if (modal && e.target === modal) {
    modal.classList.remove("open");
    if (!document.querySelector(".modal.open")) {
      document.body.style.overflow = "";
    }
  }
});

// Close on ESC
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    document.querySelectorAll(".modal.open").forEach(m => m.classList.remove("open"));
    document.body.style.overflow = "";
  }
});