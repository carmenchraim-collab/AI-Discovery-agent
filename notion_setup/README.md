# Notion setup

Creates the 5 Notion databases the agent reads from and writes to, and seeds
them with demo data for "Expat Apartment Assistant — Berlin". Standard
library only — nothing to `pip install`.

## Databases created

| Database | Key properties |
|---|---|
| Product Idea | Title, Elevator Pitch, Status (select) |
| Personas | Persona Name, Description — 2 rows |
| Interview Questions | Question, Order (number) — 6 rows |
| Interview Answers | Answer, Persona (select), Question (relation → Interview Questions), Date |
| Insight Reports | Report Title, Validation Status (select), Summary, Key Insights, Opportunities, Date Generated — starts empty; the agent writes here |

## 1. Create a Notion integration

1. Go to https://www.notion.so/my-integrations → **New integration**.
2. Copy the **Internal Integration Secret** (`secret_...` or `ntn_...`).
3. Pick a Notion page to hold the demo (e.g. "Expat Apartment Assistant"),
   open it, click **... → Connections → Connect to**, and add your
   integration. Without this share step, database creation fails with a 404.
4. Copy that page's ID: it's the 32-character hex string in the page URL,
   e.g. `notion.so/My-Page-1a2b3c4d5e6f...` → `1a2b3c4d5e6f...`.

## 2. Configure

```bash
cp ../.env.example .env   # or export directly in your shell
export NOTION_API_KEY="secret_..."
export NOTION_PARENT_PAGE_ID="1a2b3c4d5e6f..."
```

Never commit `.env` or paste the API key into a file that gets pushed —
`.env` is already gitignored.

## 3. Preview, then run

```bash
python3 setup_notion.py --dry-run   # prints every API call, makes none
python3 setup_notion.py             # creates the databases for real
```

The script prints each database's ID as it's created. Re-running it creates
a second set of databases rather than updating the first — there's no
dedupe step, so delete the old ones in Notion first if you want a clean
re-run.

## Editing the demo content

All sample text — the product pitch, personas, questions, and answers —
lives in `sample_data.py`, separate from the API logic in `setup_notion.py`.
Edit values there; `Interview Answers` links to a question by matching its
`question` text against `INTERVIEW_QUESTIONS`, so keep those in sync if you
change the question wording.
