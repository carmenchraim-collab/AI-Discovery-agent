#!/usr/bin/env python3
"""
Creates the 5 Notion databases for the Expat Apartment Assistant demo and
populates them with the sample data in sample_data.py.

Usage:
    export NOTION_API_KEY="secret_..."
    export NOTION_PARENT_PAGE_ID="..."   # page the databases are created under
    python3 setup_notion.py              # add --dry-run to preview with no API calls

Requires only the Python 3 standard library — nothing to pip install.
"""
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

import sample_data as data

NOTION_VERSION = "2022-06-28"
API_BASE = "https://api.notion.com/v1"


class NotionClient:
    def __init__(self, api_key, dry_run=False):
        self.api_key = api_key
        self.dry_run = dry_run

    def request(self, method, path, body=None):
        if self.dry_run:
            print(f"[dry-run] {method} {path}")
            print(json.dumps(body, indent=2))
            return {"id": f"dry-run-id-{path}-{time.time_ns()}"}

        url = f"{API_BASE}{path}"
        payload = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=payload, method=method)
        req.add_header("Authorization", f"Bearer {self.api_key}")
        req.add_header("Notion-Version", NOTION_VERSION)
        req.add_header("Content-Type", "application/json")

        for attempt in range(5):
            try:
                with urllib.request.urlopen(req) as resp:
                    return json.loads(resp.read())
            except urllib.error.HTTPError as e:
                error_body = e.read().decode("utf-8")
                if e.code == 429 and attempt < 4:
                    retry_after = int(e.headers.get("Retry-After", "1"))
                    print(f"Rate limited, retrying in {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                if e.code >= 500 and attempt < 4:
                    wait = 2 ** attempt
                    print(f"Server error {e.code}, retrying in {wait}s...")
                    time.sleep(wait)
                    continue
                raise RuntimeError(f"Notion API error {e.code} on {method} {path}: {error_body}") from e

    def create_database(self, parent_page_id, title, properties, icon=None):
        body = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties,
        }
        if icon:
            body["icon"] = {"type": "emoji", "emoji": icon}
        result = self.request("POST", "/databases", body)
        print(f"Created database '{title}' -> {result['id']}")
        return result["id"]

    def create_page(self, database_id, properties):
        body = {
            "parent": {"type": "database_id", "database_id": database_id},
            "properties": properties,
        }
        return self.request("POST", "/pages", body)


# --- Property value helpers (for writing rows) -----------------------------

def title_val(text):
    return {"title": [{"text": {"content": text}}]}


def rich_text_val(text):
    return {"rich_text": [{"text": {"content": text}}]}


def select_val(name):
    return {"select": {"name": name}}


def number_val(n):
    return {"number": n}


def date_val(iso_date):
    return {"date": {"start": iso_date}}


def relation_val(page_ids):
    return {"relation": [{"id": pid} for pid in page_ids]}


# --- Database schemas --------------------------------------------------

def product_idea_schema():
    return {
        "Title": {"title": {}},
        "Elevator Pitch": {"rich_text": {}},
        "Status": {"select": {"options": [{"name": s} for s in data.PRODUCT_STATUS_OPTIONS]}},
    }


def personas_schema():
    return {
        "Persona Name": {"title": {}},
        "Description": {"rich_text": {}},
    }


def interview_questions_schema():
    return {
        "Question": {"title": {}},
        "Order": {"number": {"format": "number"}},
    }


def interview_answers_schema(questions_db_id, persona_names):
    return {
        "Answer": {"title": {}},
        "Persona": {"select": {"options": [{"name": p} for p in persona_names]}},
        "Question": {"relation": {"database_id": questions_db_id, "single_property": {}}},
        "Date": {"date": {}},
    }


def insight_reports_schema():
    return {
        "Report Title": {"title": {}},
        "Validation Status": {"select": {"options": [{"name": s} for s in data.INSIGHT_STATUS_OPTIONS]}},
        "Summary": {"rich_text": {}},
        "Key Insights": {"rich_text": {}},
        "Opportunities": {"rich_text": {}},
        "Date Generated": {"date": {}},
    }


# --- Orchestration -------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="Print API calls instead of making them")
    args = parser.parse_args()

    api_key = os.environ.get("NOTION_API_KEY")
    parent_page_id = os.environ.get("NOTION_PARENT_PAGE_ID")

    if not args.dry_run and not api_key:
        sys.exit("Missing NOTION_API_KEY environment variable.")
    if not parent_page_id:
        sys.exit("Missing NOTION_PARENT_PAGE_ID environment variable (the page the databases are created under).")

    client = NotionClient(api_key, dry_run=args.dry_run)

    # 1. Product Idea
    product_db = client.create_database(parent_page_id, "Product Idea", product_idea_schema(), icon="\U0001F4A1")
    client.create_page(product_db, {
        "Title": title_val(data.PRODUCT_IDEA["title"]),
        "Elevator Pitch": rich_text_val(data.PRODUCT_IDEA["elevator_pitch"]),
        "Status": select_val(data.PRODUCT_IDEA["status"]),
    })

    # 2. Personas
    personas_db = client.create_database(parent_page_id, "Personas", personas_schema(), icon="\U0001F465")
    persona_names = [p["name"] for p in data.PERSONAS]
    for persona in data.PERSONAS:
        client.create_page(personas_db, {
            "Persona Name": title_val(persona["name"]),
            "Description": rich_text_val(persona["description"]),
        })

    # 3. Interview Questions
    questions_db = client.create_database(parent_page_id, "Interview Questions", interview_questions_schema(), icon="❓")
    question_page_ids = {}  # question text -> page id, for linking answers
    for q in sorted(data.INTERVIEW_QUESTIONS, key=lambda q: q["order"]):
        page = client.create_page(questions_db, {
            "Question": title_val(q["question"]),
            "Order": number_val(q["order"]),
        })
        question_page_ids[q["question"]] = page["id"]

    # 4. Interview Answers (relates to Interview Questions, so it's created after)
    answers_db = client.create_database(
        parent_page_id, "Interview Answers",
        interview_answers_schema(questions_db, persona_names), icon="\U0001F4AC",
    )
    for a in data.INTERVIEW_ANSWERS:
        question_id = question_page_ids.get(a["question"])
        if not question_id and not args.dry_run:
            sys.exit(f"Answer references a question not found in INTERVIEW_QUESTIONS: {a['question']!r}")
        client.create_page(answers_db, {
            "Answer": title_val(a["answer"]),
            "Persona": select_val(a["persona"]),
            "Question": relation_val([question_id] if question_id else []),
            "Date": date_val(a["date"]),
        })

    # 5. Insight Reports (schema only, starts empty)
    client.create_database(parent_page_id, "Insight Reports", insight_reports_schema(), icon="\U0001F4CA")

    print("\nDone. Databases created:")
    print(f"  Product Idea:         {product_db}")
    print(f"  Personas:             {personas_db}")
    print(f"  Interview Questions:  {questions_db}")
    print(f"  Interview Answers:    {answers_db}")


if __name__ == "__main__":
    main()
