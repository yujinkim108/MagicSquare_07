"""
sessionEnd hook: Copies the latest session transcript JSONL
from Cursor's agent-transcripts folder to the project's Prompting/ folder.
"""

import sys
import json
import re
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(r"c:\DEV\Arithmetic_XXX")
TRANSCRIPTS_DIR = Path(r"C:\Users\usejen_id\.cursor\projects\c-DEV-Arithmetic-XXX\agent-transcripts")
PROMPTING_DIR = PROJECT_ROOT / "Prompting"

def get_next_file_number(folder: Path) -> str:
    existing = list(folder.glob("*.md")) + list(folder.glob("*.jsonl"))
    max_num = 0
    for f in existing:
        m = re.match(r"^(\d+)_", f.name)
        if m:
            max_num = max(max_num, int(m.group(1)))
    return str(max_num + 1).zfill(2)


def jsonl_to_markdown(jsonl_path: Path) -> str:
    messages = []
    with open(jsonl_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                messages.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        f"# Session Transcript — {today}\n",
        f"\n> Source: `{jsonl_path.name}`\n\n---\n\n",
    ]

    for msg in messages:
        role = msg.get("role", "unknown")

        # Structure: { role, message: { content: [{ type, text }] } }
        # Fallback:  { role, content: "..." or [{ type, text }] }
        raw_content = msg.get("message", {}).get("content", msg.get("content", ""))

        if isinstance(raw_content, list):
            parts = [b.get("text", "") for b in raw_content if isinstance(b, dict)]
            content = "\n".join(p for p in parts if p)
        elif isinstance(raw_content, str):
            content = raw_content
        else:
            content = str(raw_content)

        # Strip system context injected by Cursor (timestamp, user_query wrappers)
        content = re.sub(r"<timestamp>.*?</timestamp>\n?", "", content, flags=re.DOTALL)
        content = re.sub(r"<[^>]+>", "", content).strip()

        if not content:
            continue

        if role == "user":
            lines.append(f"## 👤 User\n\n{content}\n\n---\n\n")
        elif role == "assistant":
            lines.append(f"## 🤖 Assistant\n\n{content}\n\n---\n\n")
        else:
            lines.append(f"## {role.title()}\n\n{content}\n\n---\n\n")

    return "".join(lines)


def main():
    # Optional argument: report filename (e.g. "05_hooks_setup_report.md")
    # If provided, the transcript is saved as the same name with "-prompt" before ".md"
    report_filename = sys.argv[1] if len(sys.argv) > 1 else None

    if not TRANSCRIPTS_DIR.exists():
        sys.exit(0)

    jsonl_files = list(TRANSCRIPTS_DIR.glob("**/*.jsonl"))
    if not jsonl_files:
        sys.exit(0)

    latest = max(jsonl_files, key=lambda f: f.stat().st_mtime)

    PROMPTING_DIR.mkdir(parents=True, exist_ok=True)

    if report_filename:
        stem = Path(report_filename).stem  # e.g. "05_hooks_setup_report"
        output_name = f"{stem}-prompt.md"
    else:
        next_num = get_next_file_number(PROMPTING_DIR)
        today_str = datetime.now().strftime("%Y%m%d")
        output_name = f"{next_num}_session_transcript_{today_str}-prompt.md"

    output_path = PROMPTING_DIR / output_name

    md_content = jsonl_to_markdown(latest)
    output_path.write_text(md_content, encoding="utf-8")

    print(json.dumps({}))


if __name__ == "__main__":
    main()
