// Reilynn's Rowdy Sourdough — small bits of interactivity

// Mobile nav toggle
const nav = document.querySelector('.nav');
const toggle = document.getElementById('navToggle');
const links = document.getElementById('navLinks');

if (toggle && nav && links) {
  toggle.addEventListener('click', () => {
    const open = nav.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  });

  // Close the menu after tapping a link (mobile)
  links.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => {
      nav.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
    });
  });
}

// Delivery areas dropdown
const deliveryToggle = document.getElementById('deliveryToggle');
const deliveryMenu = document.getElementById('deliveryMenu');
const deliveryDropdown = document.getElementById('deliveryDropdown');

if (deliveryToggle && deliveryMenu && deliveryDropdown) {
  deliveryToggle.addEventListener('click', (event) => {
    event.stopPropagation();
    const open = deliveryMenu.hasAttribute('hidden');
    if (open) {
      deliveryMenu.removeAttribute('hidden');
    } else {
      deliveryMenu.setAttribute('hidden', '');
    }
    deliveryToggle.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (!deliveryDropdown.contains(event.target)) {
      deliveryMenu.setAttribute('hidden', '');
      deliveryToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// Auto-update the footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();
