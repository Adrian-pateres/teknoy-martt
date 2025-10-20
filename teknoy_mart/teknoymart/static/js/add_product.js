// Image preview
function previewImage(event) {
  const img = document.getElementById('imagePreview');
  const text = document.getElementById('uploadText');
  img.src = URL.createObjectURL(event.target.files[0]);
  img.style.display = 'block';
  text.style.display = 'none';
}

// Sample images preview
function previewSamples(event) {
  const carousel = document.getElementById('sampleCarousel');
  carousel.innerHTML = '';
  Array.from(event.target.files).forEach(file => {
    const imgBox = document.createElement('div');
    imgBox.classList.add('sample-box');
    const img = document.createElement('img');
    img.src = URL.createObjectURL(file);
    imgBox.appendChild(img);
    carousel.appendChild(imgBox);
  });
  const addBox = document.createElement('div');
  addBox.classList.add('sample-box');
  addBox.innerHTML = '<span>+</span>';
  addBox.onclick = () => document.getElementById('sampleUpload').click();
  carousel.appendChild(addBox);
}

function scrollCarousel(direction) {
  const carousel = document.getElementById('sampleCarousel');
  carousel.scrollBy({ left: direction * 100, behavior: 'smooth' });
}

// ===== MODAL FUNCTIONS =====
function openModal(id) {
  document.getElementById(id).style.display = 'flex';
}
function closeModal(id) {
  document.getElementById(id).style.display = 'none';
}
function confirmCancel() {
  window.location.href = "/";
}
function confirmAdd() {
  document.getElementById('productForm').submit();
}

// ===== FORM VALIDATION =====
function validateForm() {
  const form = document.getElementById('productForm');
  const requiredFields = form.querySelectorAll('input[required], select[required], textarea[required]');
  let allValid = true;

  requiredFields.forEach(field => {
    if (!field.value.trim()) {
      field.classList.add('invalid');
      allValid = false;
    } else {
      field.classList.remove('invalid');
    }
  });

  if (allValid) {
    openModal('addModal');
  } else {
    alert("⚠️ Please fill in all required fields before submitting.");
  }
}
