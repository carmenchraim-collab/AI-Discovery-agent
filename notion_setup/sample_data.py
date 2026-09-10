"""
Editable demo content for the Expat Apartment Assistant — Berlin databases.

Edit the values below, then run `python3 setup_notion.py`.
Nothing here talks to the Notion API — that logic lives in setup_notion.py.
"""

PRODUCT_IDEA = {
    "title": "Expat Apartment Assistant — Berlin",
    "elevator_pitch": (
        "An AI research agent that interviews recent expat renters, synthesizes "
        "their Berlin apartment-hunting pain points, and turns them into a "
        "validated, prioritized product brief — so PMs stop guessing what to "
        "build for newcomers navigating Anmeldung, Schufa, and WG culture."
    ),
    "status": "Discovery",
}

# Options shown in the "Status" select on the Product Idea database.
PRODUCT_STATUS_OPTIONS = ["Discovery", "Validating", "Validated", "Parked"]

PERSONAS = [
    {
        "name": "Relocating Tech Employee",
        "description": (
            "Mid-level engineer moving to Berlin for a new job on a "
            "company-sponsored visa. Needs to sign a lease within 30 days to "
            "register an address (Anmeldung) and satisfy immigration "
            "requirements. Time-poor, budget ~€1,200-1,600/month, weak German, "
            "relies on an employer relocation stipend and English-language "
            "resources."
        ),
    },
    {
        "name": "Self-Funded Remote Freelancer",
        "description": (
            "Freelance designer on a self-employment visa, no local employer "
            "backing or Schufa credit history. Budget-conscious "
            "(~€700-1,000/month), open to WG (flat-share) living, highly "
            "active in expat Facebook/Telegram groups, distrustful of "
            "listings after a near-scam experience."
        ),
    },
]

# "Order" controls both display order and how Interview Answers link back
# to a question below (matched by exact question text).
INTERVIEW_QUESTIONS = [
    {"order": 1, "question": "Walk me through the last time you searched for an apartment in Berlin — where did you start?"},
    {"order": 2, "question": "What was the most frustrating part of the process, and why?"},
    {"order": 3, "question": "How did you handle the Schufa / proof-of-income requirement?"},
    {"order": 4, "question": "Did you use any tools, apps, or communities to help you search? What worked and what didn't?"},
    {"order": 5, "question": "Tell me about a time you almost got scammed or lost money during your search."},
    {"order": 6, "question": "If you could wave a magic wand and fix one part of this experience, what would it be?"},
]

# Each answer links to a persona (by name, stored as a select) and a
# question (by matching question text, stored as a relation).
INTERVIEW_ANSWERS = [
    {
        "persona": "Relocating Tech Employee",
        "question": "Walk me through the last time you searched for an apartment in Berlin — where did you start?",
        "date": "2026-08-04",
        "answer": (
            "I started on ImmoScout24 the day after I signed my offer letter, "
            "but most of what I found was gone within hours. My company's "
            "relocation agency sent me three listings and I took the first "
            "one that would even respond to a foreigner."
        ),
    },
    {
        "persona": "Relocating Tech Employee",
        "question": "What was the most frustrating part of the process, and why?",
        "date": "2026-08-04",
        "answer": (
            "The 30-day Anmeldung deadline was the killer. Landlords wanted "
            "Schufa and proof of German income I didn't have yet, and my "
            "visa appointment was already booked for week three, so I felt "
            "like I was racing a clock I couldn't control."
        ),
    },
    {
        "persona": "Relocating Tech Employee",
        "question": "How did you handle the Schufa / proof-of-income requirement?",
        "date": "2026-08-05",
        "answer": (
            "I couldn't get a Schufa in time, so my employer's relocation "
            "partner co-signed as a guarantor. Without that I don't think "
            "any landlord would have taken me seriously."
        ),
    },
    {
        "persona": "Relocating Tech Employee",
        "question": "Did you use any tools, apps, or communities to help you search? What worked and what didn't?",
        "date": "2026-08-05",
        "answer": (
            "I tried Facebook expat groups but the volume of scam listings "
            "made me give up fast — 'WhatsApp me the deposit before viewing' "
            "is a huge red flag I only learned to spot after almost falling "
            "for it."
        ),
    },
    {
        "persona": "Self-Funded Remote Freelancer",
        "question": "Walk me through the last time you searched for an apartment in Berlin — where did you start?",
        "date": "2026-08-11",
        "answer": (
            "I started in Telegram groups because someone told me agencies "
            "won't touch freelancers. WG-Gesucht was my second stop, but "
            "half the good listings were flatshares choosing on vibe, not "
            "paperwork."
        ),
    },
    {
        "persona": "Self-Funded Remote Freelancer",
        "question": "What was the most frustrating part of the process, and why?",
        "date": "2026-08-11",
        "answer": (
            "Not having a Schufa or an employer letter made me invisible to "
            "half the listings. I'd message and just get ignored — no "
            "rejection, just silence, which was almost worse."
        ),
    },
    {
        "persona": "Self-Funded Remote Freelancer",
        "question": "Tell me about a time you almost got scammed or lost money during your search.",
        "date": "2026-08-12",
        "answer": (
            "Someone asked for a deposit via bank transfer before a viewing, "
            "using photos stolen from another listing. I lost about three "
            "days chasing it before a friend from an expat group told me it "
            "was a known scam pattern."
        ),
    },
    {
        "persona": "Self-Funded Remote Freelancer",
        "question": "If you could wave a magic wand and fix one part of this experience, what would it be?",
        "date": "2026-08-12",
        "answer": (
            "I'd want a way to prove I'm legit — income, references, intent "
            "— without needing a German bank account or Schufa first. "
            "Something that translates my freelance reality into something "
            "a landlord actually trusts."
        ),
    },
]

# Options shown in the "Validation Status" select on Insight Reports.
# The database itself starts with zero rows.
INSIGHT_STATUS_OPTIONS = ["Validated", "Partially Validated", "Not Validated", "Needs More Data"]
