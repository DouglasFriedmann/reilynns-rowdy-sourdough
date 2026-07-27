/**
 * Cloudflare Pages Function — texts order/chat details to the baker via Twilio.
 *
 * Set these secrets in Cloudflare Pages → Settings → Environment variables:
 *   TWILIO_ACCOUNT_SID
 *   TWILIO_AUTH_TOKEN
 *   TWILIO_FROM_NUMBER   (your Twilio number, E.164 like +15551234567)
 *   BAKER_TO_NUMBER     (optional; defaults to +12015724418)
 */

const DEFAULT_BAKER = '+12015724418';

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      'Cache-Control': 'no-store',
    },
  });
}

function clean(value, max = 500) {
  return String(value || '').trim().slice(0, max);
}

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ error: 'Invalid JSON body.' }, 400);
  }

  const type = body.type === 'chat' ? 'chat' : 'order';
  const name = clean(body.name, 120);
  const phone = clean(body.phone, 40);
  const email = clean(body.email, 120);
  const message = clean(body.message, 1000);

  if (!name || !phone) {
    return json({ error: 'Name and phone are required.' }, 400);
  }
  if (type === 'order' && !email) {
    return json({ error: 'Email is required for orders.' }, 400);
  }
  if (type === 'chat' && !message) {
    return json({ error: 'Message is required.' }, 400);
  }

  const sid = env.TWILIO_ACCOUNT_SID;
  const token = env.TWILIO_AUTH_TOKEN;
  const from = env.TWILIO_FROM_NUMBER;
  const to = env.BAKER_TO_NUMBER || DEFAULT_BAKER;

  if (!sid || !token || !from) {
    // Site JS will fall back to the device sms: link.
    return json({
      error: 'SMS not configured yet. Add Twilio secrets in Cloudflare Pages.',
      fallback: true,
    }, 503);
  }

  const lines = [
    type === 'chat' ? '💬 New website chat' : '🍞 New website order request',
    `Name: ${name}`,
    `Phone: ${phone}`,
    email ? `Email: ${email}` : null,
    message ? `Message: ${message}` : null,
    '',
    'Reply to their phone number above.',
  ].filter((line) => line !== null);

  const twilioUrl = `https://api.twilio.com/2010-04-01/Accounts/${sid}/Messages.json`;
  const auth = btoa(`${sid}:${token}`);
  const form = new URLSearchParams({
    To: to,
    From: from,
    Body: lines.join('\n'),
  });

  const twilioRes = await fetch(twilioUrl, {
    method: 'POST',
    headers: {
      Authorization: `Basic ${auth}`,
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: form,
  });

  if (!twilioRes.ok) {
    const detail = await twilioRes.text();
    console.error('Twilio error', twilioRes.status, detail);
    return json({
      error: 'Twilio could not send the text. Check your Twilio credentials/number.',
      fallback: true,
    }, 502);
  }

  return json({ ok: true, via: 'twilio' });
}

export async function onRequestOptions() {
  return new Response(null, {
    status: 204,
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
