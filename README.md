# AI Product Insights Agent

An agentic workflow that helps a product manager validate a product idea against real user interview data — instead of manually synthesizing interviews by hand.

Given a product idea, its underlying assumptions, target personas, interview questions, and raw interview answers, the agent produces a structured synthesis report — flagging which assumptions the data supports, which it contradicts, and what the interviews missed — and writes it directly back to Notion.

## Why this exists

Product teams collect interview data constantly, but synthesis is slow, manual, and easy to do inconsistently. This agent turns that synthesis step into a repeatable, structured, one-click workflow.

**Sample use case in this repo:** "Expat Apartment Assistant" — a hypothetical product helping expats navigate apartment hunting in a new country.

## How it works

1. **Trigger** — manually started in n8n (designed to be swapped for a Notion webhook or scheduled trigger in production)
2. **Fetch** — five parallel Notion nodes pull markdown content from the Product Idea, Product Assumptions, Personas, Interview Questions, and Interview Answers pages
3. **Merge** — the five markdown documents are combined into a single input
4. **Synthesize** — the merged input is sent to Claude (Anthropic API) with a structured prompt asking it to validate each assumption against the interview data, surface gaps, and return a structured JSON verdict
5. **Parse** — a small code step extracts and cleans Claude's JSON response
6. **Write back** — the structured result (title, validation status, summary, key insights, opportunities, confirmed/challenged assumptions) is written back into the Notion Output page as formatted blocks

## Tech stack

- **[n8n](https://n8n.io)** — workflow orchestration
- **[Claude (Anthropic API)](https://www.anthropic.com)** — synthesis and reasoning
- **[Notion API](https://developers.notion.com)** — data source and output destination

## Setup

### 1. Notion
- Duplicate the sample workspace structure: Product Idea, Product Assumptions, Personas, Interview Questions, Interview Answers, and Output pages
- Create a Notion integration at [notion.so/my-integrations](https://www.notion.so/my-integrations) with Read, Insert, and Update content capabilities
- Share each of the six pages with your integration (••• menu → Connections → add your integration)

### 2. Anthropic API
- Get an API key from [console.anthropic.com](https://console.anthropic.com)
- Ensure the account has available credit

### 3. n8n
- Import `workflow.json` from this repo into your n8n instance
- Set up credentials:
  - **Notion**: your integration secret
  - **Anthropic**: your API key (used in the HTTP Request node's headers)
- Update the page/database IDs in the Notion nodes to point at your own workspace pages

### 4. Run it
- Click "Execute workflow" from the manual trigger
- Check the Output page in Notion for the generated report

## Design notes / decisions

- **Claude over GPT-5**: this project was originally built on GPT-5 and rebuilt on Claude for this iteration.
- **Blocks, not a database, for Output**: the Output page writes structured content as Notion blocks (headings + paragraphs) rather than database rows, keeping the setup accessible without requiring a paid Notion plan for larger databases.
- **Structured JSON prompting**: Claude is instructed to return a strict JSON shape rather than free-form markdown, making the output reliably parseable and mappable to specific Notion blocks.

## Possible next steps

- Replace the manual trigger with a Notion webhook so the agent runs automatically when new interview answers are added
- Add a "Turn into database" write-back option for teams that want a running log of past validation reports
- Expand the synthesis prompt to support multiple product ideas being compared side by side
