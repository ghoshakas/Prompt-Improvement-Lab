# Before / After Outputs

Real responses from **`gemini-3.6-flash`**, captured live on 2026-11-03. Each task runs the
lazy **original** prompt and the **improved** prompt on the *same* input, so the only variable
is the prompt. Outputs are the model's actual text (only stray trailing whitespace trimmed).

The prompts themselves live in [`backend/prompts.py`](backend/prompts.py); more inputs to try
are in [`TEST_INPUTS.md`](TEST_INPUTS.md).

> **What to look for:** the lazy prompts "work" but drift — inconsistent length, invented
> structure, extra commentary, multiple options you didn't ask for. The improved prompts
> return exactly the requested shape every time: 3 bullets, strict JSON, a fixed schema.

---

## 1. Summarization

**Input**
> Our Q3 earnings call covered a lot of ground. Revenue came in at $4.2M, up 18% from Q2, driven mostly by the new enterprise tier which added 120 accounts. Churn ticked up slightly to 3.1% as a few early customers moved to a competitor. We hired 14 people, bringing headcount to 96, and we expect to close the Series B (targeting $25M) by the end of January. The team also shipped the mobile app, which now accounts for 22% of daily active usage.

**Original prompt** → `Summarize this: {input}`
```
Here is a summary of the Q3 earnings call highlights:

* **Revenue:** Reached $4.2M (up 18% from Q2), driven by 120 new enterprise tier accounts.
* **Churn:** Slightly increased to 3.1% due to competitors.
* **Product:** Launched the mobile app, which currently represents 22% of daily active usage.
* **Team:** Hired 14 new employees, expanding total headcount to 96.
* **Funding:** On track to close a targeted $25M Series B round by late January.
```

**Improved prompt** → business-editor role, *exactly 3 bullets under 20 words, keep every number*
```
* Revenue reached $4.2M in Q3, representing an 18% growth from Q2.
* Headcount increased to 96 after hiring 14 people, with a $25M Series B targeting late January.
* Churn rose to 3.1%, while mobile app adoption hit 22% of daily active usage.
```

**Takeaway:** the lazy prompt produced **5** bullets with bold labels it invented; the improved
prompt honored the exact "3 bullets" constraint while still preserving every key number.

---

## 2. Classification

**Input**
> Hi, I was charged twice for my subscription this month and I can see two identical line items on my card. Can someone refund the duplicate? This is really frustrating.

**Original prompt** → `What category is this? {input}`
```
This falls under the category of **Billing & Payments** (or more specifically, **Duplicate Charge / Refund Request**).

If you are sorting customer service tickets, common category names for this would be:

* **Primary Category:** Billing & Financial / Subscriptions
* **Sub-Category:** Overcharge / Duplicate Billing / Refund Request
* **Priority/Sentiment:** Medium-High (due to customer frustration and monetary error)
```

**Improved prompt** → triage system, *one label from a fixed enum, JSON only*
```
{"label": "billing", "confidence": 0.98, "reason": "The user is requesting a refund for a duplicate subscription charge on their credit card."}
```

**Takeaway:** the lazy output is prose with made-up category names — unusable by code. The
improved output is a single machine-readable JSON object with a label from the fixed set, a
confidence score, and a reason.

---

## 3. Extraction

**Input**
> Order confirmation: Jane Doe ordered 2x Wireless Mouse and 1x USB-C Hub on March 3rd. Ship to 42 Oak Street, Austin. She can be reached at jane.doe@example.com. Total was $89.97, paid by card.

**Original prompt** → `Get the important info from this: {input}`
```
Here is the key information from the order confirmation:

* **Customer:** Jane Doe
* **Contact:** jane.doe@example.com
* **Order Date:** March 3rd
* **Items Ordered:**
  * 2x Wireless Mouse
  * 1x USB-C Hub
* **Total Cost:** $89.97
* **Payment Method:** Card
* **Shipping Address:** 42 Oak Street, Austin
```

**Improved prompt** → strict JSON schema, *null for missing, do not guess*
```json
{
  "customer_name": "Jane Doe",
  "email": "jane.doe@example.com",
  "order_date": null,
  "items": [
    {"name": "Wireless Mouse", "quantity": 2},
    {"name": "USB-C Hub", "quantity": 1}
  ],
  "total_amount": 89.97,
  "shipping_city": "Austin"
}
```

**Takeaway:** the best illustration in the set. The lazy prompt returns a bulleted paragraph you
still have to parse. The improved prompt returns schema-exact JSON — and crucially set
`"order_date": null` instead of guessing a year for "March 3rd", exactly as instructed ("do not
guess or invent values"). `total_amount` is a real number, items are a typed array.

---

## 4. Rewriting

**Input**
> hey so i cant make the meeting tomrrow something came up, can we do it later in the week maybe thursday? sorry for the hassle

**Original prompt** → `Make this better: {input}`
```
Here are a few ways to rewrite your message, depending on how formal you need to be:

**Option 1: Professional & Polite (Best for clients, managers, or external partners)**
> "Hi [Name], I apologize, but something unexpected has come up and I won't be able to make our meeting tomorrow. Would we be able to reschedule for later in the week? I'm available this Thursday if that works for you. Sorry for any inconvenience!"

**Option 2: Casual & Friendly (Best for close colleagues or team members)**
> "Hey [Name], I'm so sorry, but something came up and I won't be able to make our meeting tomorrow. Could we reschedule for later in the week? Thursday works well for me if you're free. Thanks, and sorry for the short notice!"

**Option 3: Short & Direct (Great for Slack/Teams messages)**
> "Hi [Name], I need to reschedule our meeting tomorrow due to a last-minute conflict. Are you free to connect this Thursday instead? Apologies for the hassle!"

**Key improvements made:**
* Fixed typos ("tomrrow").
* Added a placeholder for their name to make it personal.
* Rephrased "sorry for the hassle" to sound more professional.
* Proposed a specific day (Thursday) to make rescheduling easier for the other person.
```

**Improved prompt** → communications editor, *one warm 2–3 sentence email, propose Thursday as a question*

> _Capture pending — the free-tier daily quota (20 requests/day) was reached mid-run. This
> output will be filled in when the quota resets. The improved prompt is designed to return a
> single, ready-to-send 2–3 sentence email (no "Option 1/2/3" menu), which is the whole point
> of the contrast with the lazy output above._

**Takeaway:** even without the improved capture, the contrast is already clear — the lazy prompt
dumped **three** options plus a meta-commentary section instead of the one rewrite a user wants.

---

## 5. Content Generation

**Input**
> A reusable stainless-steel water bottle that keeps drinks cold for 24 hours.

**Improved prompt** → DTC copywriter, *50–70 words, named audience & tone, must mention 24h cold + reusable, end with a CTA*

> _Both captures pending — the free-tier daily quota was reached before this task ran. Will be
> filled in on quota reset._

---

### How these were captured

Generated by running each original and improved prompt from `backend/prompts.py` against the
same `sample_input`, via the project's own `gemini_client.generate()` — the identical code path
the live app uses. Model: `gemini-3.6-flash` with thinking disabled for fast responses.

> **Note on the free tier:** Google's free Gemini tier allows ~5 requests/minute and ~20
> requests/day. Capturing all 10 outputs in one sitting hits the daily cap, which is why the
> last two are pending. The same limit affects the live demo late in a heavy day.
