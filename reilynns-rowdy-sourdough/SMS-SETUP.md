# Make order form + chat text 201-572-4418

Your site can now collect orders and chat messages. To **automatically text you**, connect free-to-start **Twilio** to your existing **Cloudflare Pages** site. No AWS SNS/SQS needed for this scale.

## What you get

| Feature | How it works |
|--------|----------------|
| Combined “Chat / Custom Flavor” button | Opens an on-site chat panel |
| Send from chat or order form | Cloudflare Function → Twilio → SMS to **201-572-4418** |
| Your reply | You text the customer back on **their phone** |
| If Twilio isn’t set up yet | Site opens the visitor’s own texting app with a prefilled message (still works!) |

## Honest answer: “Can replies show in the website chat box?”

**Not with this lightweight setup.** That would need:

1. Twilio inbound webhook when you reply  
2. A database to store conversation threads  
3. The website polling or using websockets to show new messages  

That’s the enterprise-ish path (closer to SNS/SQS + storage). For a bakery, **you text them back on their cell** is simpler, cheaper, and what customers expect.

## 15-minute setup

### 1) Create a Twilio account
1. Go to [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio)
2. Get a **US phone number** that can send SMS (~$1.15/month + ~1–2¢ per text)
3. Copy from the Twilio console:
   - **Account SID**
   - **Auth Token**
   - **From number** (looks like `+1XXXXXXXXXX`)

### 2) Add secrets in Cloudflare Pages
1. Cloudflare Dashboard → **Workers & Pages** → your `rowdysourdough` project  
2. **Settings** → **Environment variables**  
3. Add (for Production):

| Name | Value |
|------|--------|
| `TWILIO_ACCOUNT_SID` | from Twilio |
| `TWILIO_AUTH_TOKEN` | from Twilio (mark Encrypted) |
| `TWILIO_FROM_NUMBER` | e.g. `+15551234567` |
| `BAKER_TO_NUMBER` | `+12015724418` (optional; this is already the default) |

4. **Save** and **Redeploy** the latest commit (Functions only pick up new env vars after a deploy).

### 3) Push this code & test
```bash
git add .
git commit -m "Add order form and Twilio SMS notify"
git push
```

Then on https://rowdysourdough.com :
1. Submit a test order with your own cell  
2. You should get a text at **201-572-4418**  
3. Try the chat button too  

## Cost reality check
- Twilio number: about **$1/month**
- Each SMS: about **1–2 cents**
- Cloudflare Pages Functions: free tier is plenty for bakery volume  
- No SQS/SNS/Lambda required

## Business cards folder vs website
- Pushing `business-cards/` puts files **in git**
- They won’t appear in the nav / homepage UI  
- They **are** still downloadable if someone knows the URL, e.g.  
  `https://rowdysourdough.com/business-cards/business-card-front.pdf`  
- If you want them private, we can stop deploying that folder or remove the PDFs from the repo.
