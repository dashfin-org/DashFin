#!/usr/bin/env python3
"""
agent_full_pr.py – end‑to‑end GitHub draft‑PR automation

This script *generates or updates* real docs, commits them on a fresh
branch, pushes, and opens a **draft** pull request – no manual steps.

Prerequisites
-------------
• Activate Windows venv  →  ``. .venv\\Scripts\\Activate.ps1``
• UTF‑8 console          →  ``chcp 65001``  (already in profile)
• ``gh auth status`` shows logged‑in account (mohavro)
• Working tree **clean** – script aborts if dirty.

Run:
```powershell
python agent_full_pr.py
```

Files touched
-------------
* ``docs/agent-overview.md`` – created or updated with timestamp.
* ``README.md``           – adds a “Project badges” section if not present.

The branch is named ``agent-demo-<UTC timestamp>``. Re‑running creates
another branch, leaving old ones intact.
"""
from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
import subprocess as sp
import sys
from typing import Sequence

ROOT = Path.cwd()
BRANCH = f"agent-demo-{datetime.now(UTC):%Y%m%d%H%M%S}"
PR_TITLE = "docs: add agent overview + badges stub"
PR_BODY = (
    "Adds initial docs/agent-overview.md and a badges section in README.\n\n"
    "Automated by agent_full_pr.py"
)

README_PATH = ROOT / "README.md"
DOC_PATH = ROOT / "docs" / "agent-overview.md"

# ---------------------------------------------------------------------------

def run(cmd: Sequence[str]) -> None:
    """Run *cmd* and exit on failure."""
    sp.run(cmd, check=True, text=True)


def working_tree_dirty() -> bool:
    return bool(sp.check_output(["git", "status", "--porcelain"], text=True).strip())

# ---------------------------------------------------------------------------

def generate_files() -> None:
    """Create or update real files so the PR contains meaningful content."""
    DOC_PATH.parent.mkdir(exist_ok=True)
    DOC_PATH.write_text(
        "# Agent overview\n"
        "This document explains the agent‑driven PR automation flow.\n\n"
        f"_Generated on {datetime.now(UTC):%Y-%m-%d %H:%M UTC}_\n",
        encoding="utf-8",
    )

    if README_PATH.exists():
        content = README_PATH.read_text(encoding="utf-8")
        if "## Project badges" not in content:
            content += "\n\n## Project badges\n(markdown badges TBD)\n"
            README_PATH.write_text(content, encoding="utf-8")
    else:
        README_PATH.write_text(
            "# DashFin\n\n## Project badges\n(markdown badges TBD)\n",
            encoding="utf-8",
        )

# ---------------------------------------------------------------------------

def main() -> None:
    if working_tree_dirty():
        sys.stderr.write("ERROR: working tree dirty. Commit/stash first.\n")
        sys.exit(1)

    # Step 1 – generate/update files
    generate_files()

    # Step 2 – branch checkout/reset
    run(["git", "checkout", "-B", BRANCH])

    # Step 3 – stage & commit
    run(["git", "add", "README.md", str(DOC_PATH)])
    run(["git", "commit", "-m", PR_TITLE])

    # Step 4 – push branch (force just in case of re‑run)
    run(["git", "push", "-u", "origin", BRANCH, "--force", "--no-verify"])

    # Step 5 – open draft PR via gh CLI
    run([
        "gh", "pr", "create",
        "--title", PR_TITLE,
        "--body", PR_BODY,
        "--draft",
        "--base", "main",
    ])

    print("SUCCESS: draft PR opened – review it on GitHub.")

# ---------------------------------------------------------------------------

if __name__ == "__main__":
    main()
