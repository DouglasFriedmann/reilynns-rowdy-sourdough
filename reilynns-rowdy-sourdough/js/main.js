// Reilynn's Rowdy Sourdough — site interactivity + order/chat notify

const BAKER_SMS = "+12015724418";
const BAKER_DISPLAY = "201-572-4418";

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
    if (open) deliveryMenu.removeAttribute('hidden');
    else deliveryMenu.setAttribute('hidden', '');
    deliveryToggle.setAttribute('aria-expanded', String(open));
  });

  document.addEventListener('click', (event) => {
    if (!deliveryDropdown.contains(event.target)) {
      deliveryMenu.setAttribute('hidden', '');
      deliveryToggle.setAttribute('aria-expanded', 'false');
    }
  });
}

// Footer year
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ---------- Notify helpers ----------
function buildSmsLink({ name, phone, email, message, type }) {
  const lines = [
    type === 'chat' ? '💬 Website chat' : '🍞 Website order request',
    name ? `Name: ${name}` : null,
    phone ? `Phone: ${phone}` : null,
    email ? `Email: ${email}` : null,
    message ? `Message: ${message}` : null,
  ].filter(Boolean);
  const body = encodeURIComponent(lines.join('\n'));
  // iOS uses & body=, Android often accepts ?body=
  return `sms:${BAKER_SMS}?&body=${body}`;
}

async function notifyBaker(payload) {
  const res = await fetch('/api/notify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });

  let data = {};
  try { data = await res.json(); } catch { /* ignore */ }

  if (!res.ok) {
    const err = new Error(data.error || 'Could not send right now.');
    err.fallback = data.fallback !== false;
    throw err;
  }
  return data;
}

function openDeviceSms(payload) {
  window.location.href = buildSmsLink(payload);
}

// ---------- Chat panel ----------
const chatPanel = document.getElementById('chatPanel');
const openChatBtn = document.getElementById('openChatBtn');
const chatForm = document.getElementById('chatForm');
const chatThread = document.getElementById('chatThread');
const chatSend = document.getElementById('chatSend');

function openChat() {
  if (!chatPanel) return;
  chatPanel.hidden = false;
  document.body.style.overflow = 'hidden';
  document.getElementById('chatName')?.focus();
}

function closeChat() {
  if (!chatPanel) return;
  chatPanel.hidden = true;
  document.body.style.overflow = '';
}

function addBubble(text, who) {
  if (!chatThread) return;
  const bubble = document.createElement('div');
  bubble.className = `chat__bubble chat__bubble--${who}`;
  bubble.textContent = text;
  chatThread.appendChild(bubble);
  chatThread.scrollTop = chatThread.scrollHeight;
}

openChatBtn?.addEventListener('click', openChat);
chatPanel?.querySelectorAll('[data-close-chat]').forEach((el) => {
  el.addEventListener('click', closeChat);
});
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape' && chatPanel && !chatPanel.hidden) closeChat();
});

chatForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('chatName').value.trim();
  const phone = document.getElementById('chatPhone').value.trim();
  const message = document.getElementById('chatMessage').value.trim();
  if (!name || !phone || !message) return;

  const payload = { type: 'chat', name, phone, message };
  addBubble(message, 'you');
  document.getElementById('chatMessage').value = '';
  chatSend.disabled = true;
  chatSend.textContent = 'Sending…';

  try {
    await notifyBaker(payload);
    addBubble(`Got it — we texted the baker at ${BAKER_DISPLAY}. Watch your phone for a reply!`, 'baker');
  } catch (err) {
    addBubble('Opening your text app so you can send that to us directly…', 'baker');
    openDeviceSms(payload);
  } finally {
    chatSend.disabled = false;
    chatSend.textContent = 'Send to baker';
  }
});

// ---------- Order form ----------
const orderForm = document.getElementById('orderForm');
const orderStatus = document.getElementById('orderStatus');
const orderSubmit = document.getElementById('orderSubmit');

orderForm?.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('orderName').value.trim();
  const email = document.getElementById('orderEmail').value.trim();
  const phone = document.getElementById('orderPhone').value.trim();
  const message = document.getElementById('orderMessage').value.trim();

  if (!name || !email || !phone) {
    orderStatus.textContent = 'Please fill in your name, email, and phone.';
    orderStatus.className = 'order-form__status is-error';
    return;
  }

  const payload = { type: 'order', name, email, phone, message };
  orderSubmit.disabled = true;
  orderSubmit.textContent = 'Sending…';
  orderStatus.textContent = '';
  orderStatus.className = 'order-form__status';

  try {
    await notifyBaker(payload);
    orderStatus.textContent = `Sent! We'll text you back soon from ${BAKER_DISPLAY}.`;
    orderStatus.className = 'order-form__status is-ok';
    orderForm.reset();
  } catch (err) {
    orderStatus.textContent = 'Opening your text app with your order details…';
    orderStatus.className = 'order-form__status is-error';
    openDeviceSms(payload);
  } finally {
    orderSubmit.disabled = false;
    orderSubmit.textContent = 'Submit Order Request';
  }
});
