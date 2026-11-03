# Test Inputs

15 ready-to-use inputs (3 per task) for the Prompt Improvement Lab. Pick a task in the app,
paste one block into the **Input text** box, and click **Run comparison** to see the lazy vs
improved prompt side by side.

Each input is chosen to stress something specific — ambiguity, missing fields, typos, multiple
items — so you can see where the lazy prompt drifts and the improved prompt holds its shape.

---

## 1. Summarization
_Expected from the improved prompt: exactly 3 bullets, under 20 words each, every number kept._

**1a — Earnings call (the built-in sample)**
```
Our Q3 earnings call covered a lot of ground. Revenue came in at $4.2M, up 18% from Q2, driven mostly by the new enterprise tier which added 120 accounts. Churn ticked up slightly to 3.1% as a few early customers moved to a competitor. We hired 14 people, bringing headcount to 96, and we expect to close the Series B (targeting $25M) by the end of January. The team also shipped the mobile app, which now accounts for 22% of daily active usage.
```

**1b — Product launch retro (many numbers)**
```
The v3 launch went live on October 12 after a two-week beta with 400 users. Sign-ups jumped 240% in the first 72 hours, and we processed 11,300 orders worth $512,000 in week one. Support tickets spiked to 190 a day, mostly about the new checkout, so we rolled a hotfix on October 15 that cut that volume in half. Net Promoter Score landed at 61, up from 48 before launch. We are now planning a localized release for three European markets in Q1.
```

**1c — Research abstract (dense prose, few numbers)**
```
This study examines whether short, frequent feedback improves retention in online courses. Across 1,200 learners split into two cohorts, the group receiving weekly nudges completed 34% more modules than the control group, which received a single mid-course summary. Dropout in the nudged group fell from 41% to 27%. The effect was strongest among first-time learners and negligible among those who had completed a prior course. The authors conclude that cadence matters more than message length.
```

---

## 2. Classification
_Expected from the improved prompt: strict JSON with one label from billing / bug / feature_request / account_access / general_question / unknown._

**2a — Duplicate charge (the built-in sample)**
```
Hi, I was charged twice for my subscription this month and I can see two identical line items on my card. Can someone refund the duplicate? This is really frustrating.
```

**2b — Login failure (account_access)**
```
I've tried resetting my password three times but the reset email never arrives. I checked spam. I really need to get into my account before the end of the day for a client demo.
```

**2c — Ambiguous / mixed intent (should lean unknown or general_question)**
```
Hey, just wondering what you all think about the new dashboard — it looks nice but I'm not sure where my old reports went, and also is there a way to get a yearly plan? Thanks!
```

---

## 3. Extraction
_Expected from the improved prompt: JSON matching the schema, with `null` for anything missing — no guessing._

**3a — Full order (the built-in sample)**
```
Order confirmation: Jane Doe ordered 2x Wireless Mouse and 1x USB-C Hub on March 3rd. Ship to 42 Oak Street, Austin. She can be reached at jane.doe@example.com. Total was $89.97, paid by card.
```

**3b — Missing fields (tests the null handling)**
```
Confirming the order for Marcus Lee: 3 notebooks and a pack of pens. No email on file. Please ship to our Denver office. We'll sort out payment later.
```

**3c — Noisy forwarded email (data buried in chatter)**
```
Fwd: re: your stuff — ok so finally got it sorted lol. Priya Nair wants 1x Standing Desk and 4x Monitor Arm, shipping to Seattle. Her email is priya.nair@workmail.com if you need it. I think the total came to $1,240.50? Paid by invoice. Let me know if that's wrong.
```

---

## 4. Rewriting
_Expected from the improved prompt: one warm, professional 2–3 sentence email; Thursday proposed as a question._

**4a — Cancel a meeting (the built-in sample)**
```
hey so i cant make the meeting tomrrow something came up, can we do it later in the week maybe thursday? sorry for the hassle
```

**4b — Chase an overdue invoice (keep it polite)**
```
yo its been like 3 weeks and that invoice still isnt paid, whats going on?? we need this sorted asap its kind of holding things up on our end
```

**4c — Decline a request without burning the bridge**
```
no i cant take on the extra project rn im already slammed and honestly it should probably go to someone else, maybe thursday we can talk about who
```

---

## 5. Content Generation
_Expected from the improved prompt: 50–70 words, confident friendly tone, must mention the key features, ends with a call to action._

**5a — Water bottle (the built-in sample)**
```
A reusable stainless-steel water bottle that keeps drinks cold for 24 hours.
```

**5b — Different product (tests whether constraints transfer)**
```
A merino-wool base layer for hikers that resists odor for multiple days and packs down to the size of a fist.
```

**5c — Vague brief (where the lazy prompt really wanders)**
```
An app that helps people remember to drink water.
```
