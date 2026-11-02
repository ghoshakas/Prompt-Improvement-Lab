"""The five tasks for the Prompt Improvement Lab.

Each task carries a deliberately lazy "original" prompt, a carefully written
"improved" prompt, a sample input to try, and a short explanation of why the
improved version produces a better result. Every prompt is a template with an
`{input}` slot that gets filled in at run time.
"""

TASKS = [
    {
        "id": "summarization",
        "name": "Summarization",
        "description": "Condense a long passage into a short, faithful summary.",
        "sample_input": (
            "Our Q3 earnings call covered a lot of ground. Revenue came in at "
            "$4.2M, up 18% from Q2, driven mostly by the new enterprise tier "
            "which added 120 accounts. Churn ticked up slightly to 3.1% as a "
            "few early customers moved to a competitor. We hired 14 people, "
            "bringing headcount to 96, and we expect to close the Series B "
            "(targeting $25M) by the end of January. The team also shipped the "
            "mobile app, which now accounts for 22% of daily active usage."
        ),
        "original_prompt": "Summarize this:\n\n{input}",
        "improved_prompt": (
            "You are an experienced business editor.\n\n"
            "Summarize the text below in exactly 3 bullet points, each under 20 "
            "words. Preserve every key number (revenue, growth, headcount, "
            "dates). Do not add any fact that is not in the source. Lead each "
            "bullet with the metric it describes.\n\n"
            "Return only the 3 bullets, nothing else.\n\n"
            "Text:\n{input}"
        ),
        "explanation": [
            "The lazy prompt leaves length, format and tone up to the model, so you get a different shape every run.",
            "The improved prompt fixes the format (3 short bullets) so results are consistent and scannable.",
            "It explicitly says 'keep the numbers' and 'add nothing new', which guards against dropped facts and hallucinated detail.",
            "Giving the model a role ('business editor') nudges it toward the right register.",
        ],
    },
    {
        "id": "classification",
        "name": "Classification",
        "description": "Sort a support message into one of a fixed set of categories.",
        "sample_input": (
            "Hi, I was charged twice for my subscription this month and I can "
            "see two identical line items on my card. Can someone refund the "
            "duplicate? This is really frustrating."
        ),
        "original_prompt": "What category is this?\n\n{input}",
        "improved_prompt": (
            "You are a support-ticket triage system.\n\n"
            "Classify the message below into exactly ONE of these labels:\n"
            "- billing\n- bug\n- feature_request\n- account_access\n- general_question\n\n"
            "If the message is ambiguous, use \"unknown\". Judge intent, not tone.\n\n"
            "Respond with JSON only, no prose, in this exact shape:\n"
            '{{"label": "<one label>", "confidence": <0.0-1.0>, "reason": "<one short sentence>"}}\n\n'
            "Message:\n{input}"
        ),
        "explanation": [
            "Without a defined label set, the model invents its own categories and names them differently every time.",
            "The improved prompt pins the output to a fixed enum, so results are consistent and comparable.",
            "Asking for JSON with a confidence score and reason makes the output machine-readable and auditable.",
            "An explicit 'unknown' escape hatch stops the model from forcing a wrong label on ambiguous input.",
        ],
    },
    {
        "id": "extraction",
        "name": "Extraction",
        "description": "Pull structured fields out of messy free-form text.",
        "sample_input": (
            "Order confirmation: Jane Doe ordered 2x Wireless Mouse and 1x USB-C "
            "Hub on March 3rd. Ship to 42 Oak Street, Austin. She can be reached "
            "at jane.doe@example.com. Total was $89.97, paid by card."
        ),
        "original_prompt": "Get the important info from this:\n\n{input}",
        "improved_prompt": (
            "Extract structured data from the text below.\n\n"
            "Return JSON only, matching exactly this schema:\n"
            "{{\n"
            '  "customer_name": string | null,\n'
            '  "email": string | null,\n'
            '  "order_date": string | null,   // ISO 8601, e.g. 2026-03-03\n'
            '  "items": [{{"name": string, "quantity": number}}],\n'
            '  "total_amount": number | null,\n'
            '  "shipping_city": string | null\n'
            "}}\n\n"
            "Use null for anything not present. Do not guess or invent values. "
            "Output JSON only, no commentary.\n\n"
            "Text:\n{input}"
        ),
        "explanation": [
            "'Important info' is undefined, so the model returns a loose paragraph you still have to parse by hand.",
            "The improved prompt hands over an explicit schema, so output drops straight into code.",
            "Requiring ISO dates and null-for-missing removes format guesswork and ambiguity.",
            "'Do not guess' is a direct guard against invented emails, totals or addresses.",
        ],
    },
    {
        "id": "rewriting",
        "name": "Rewriting",
        "description": "Rewrite a rough message into clear, professional prose.",
        "sample_input": (
            "hey so i cant make the meeting tomrrow something came up, can we do "
            "it later in the week maybe thursday? sorry for the hassle"
        ),
        "original_prompt": "Make this better:\n\n{input}",
        "improved_prompt": (
            "You are a communications editor.\n\n"
            "Rewrite the message below as a professional but warm email to a "
            "colleague. Keep the original meaning and all facts. Keep it to 2-3 "
            "sentences. Fix spelling and grammar. Propose Thursday as the "
            "alternative, phrased as a question.\n\n"
            "Return only the rewritten message.\n\n"
            "Message:\n{input}"
        ),
        "explanation": [
            "'Better' has no direction, so the model guesses — sometimes longer, sometimes a different tone, sometimes changing the meaning.",
            "The improved prompt names the target audience and tone, so the rewrite lands where you wanted.",
            "'Keep the meaning and all facts' prevents the model from quietly rewriting what you actually said.",
            "Length and format constraints keep the output usable instead of ballooning into an essay.",
        ],
    },
    {
        "id": "content_generation",
        "name": "Content Generation",
        "description": "Generate marketing copy from a short brief.",
        "sample_input": "A reusable stainless-steel water bottle that keeps drinks cold for 24 hours.",
        "original_prompt": "Write something about:\n\n{input}",
        "improved_prompt": (
            "You are a direct-to-consumer copywriter.\n\n"
            "Write a product description for the item below.\n\n"
            "Constraints:\n"
            "- Audience: outdoorsy, health-conscious buyers aged 25-40.\n"
            "- Tone: confident and friendly, no hype or clichés.\n"
            "- Length: 50-70 words.\n"
            "- Must mention: the 24-hour cold retention and that it is reusable (eco-friendly).\n"
            "- End with a one-line call to action.\n\n"
            "Return only the description.\n\n"
            "Product:\n{input}"
        ),
        "explanation": [
            "'Write something' produces generic filler of unpredictable length and focus.",
            "The improved prompt sets audience, tone and length, so the copy is on-brand and usable as-is.",
            "Listing the must-include points guarantees the key selling features actually appear.",
            "Asking for a call to action gives the copy a job to do instead of just describing the product.",
        ],
    },
]

TASKS_BY_ID = {task["id"]: task for task in TASKS}
