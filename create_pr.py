#!/usr/bin/env python3
"""
create_pr.py – idempotent draft‑PR helper

Prerequisites
-------------
• Activate venv  ->  ``.venv\Scripts\Activate.ps1``  (Windows)
• ``gh auth status`` must show a logged‑in account.
• Working tree **clean** (no staged/unstaged changes) or the script aborts.

What it does
------------
1. Verifies the git working tree is clean.
2. Checks out/creates branch ``audit-demo-<UTC timestamp>``.
3. Adds a throw‑away file ``_audit_demo.txt``.
4. Commits & force‑pushes the branch.
5. Opens a **draft** PR against ``main`` using GitHub CLI.

The branch name is time‑stamped; re‑running the script creates a fresh branch.
"""

from __future__ import annotations

import subprocess as sp
import sys
from datetime import datetime, UTC
from pathlib import Path
from typing import Sequence

if hasattr(sys.stdout, "reconfigure"):
    # Prevent UnicodeEncodeError on CP‑1252 consoles
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path.cwd()
BRANCH = f"audit-demo-{datetime.now(UTC):%Y%m%d%H%M%S}"
MSG = "chore: automated draft PR (env‑audit demo)"


def run(cmd: Sequence[str]) -> None:
    """Run *cmd* aborting immediately on non‑zero exit."""
    sp.run(cmd, check=True, text=True)


def working_tree_dirty() -> bool:
    """Return True if git working tree has unstaged or untracked changes."""
    status = sp.check_output(["git", "status", "--porcelain"], text=True)
    return bool(status.strip())


def main() -> None:
    # 0. Preconditions ------------------------------------------------------
    if working_tree_dirty():
        print("❌ Working tree is dirty. Commit/stash your changes first.", file=sys.stderr)
        sys.exit(1)

    try:
        # 1. Branch manip ---------------------------------------------------
        run(["git", "checkout", "-B", BRANCH])

        # 2. Dummy file -----------------------------------------------------
        demo_file = ROOT / "_audit_demo.txt"
        demo_file.write_text("Composio audit demo\n", encoding="utf-8")
        run(["git", "add", str(demo_file)])

        # 3. Commit & push --------------------------------------------------
        run(["git", "commit", "-m", MSG])
        run(["git", "push", "-u", "origin", BRANCH, "--force"])

        # 4. Draft PR -------------------------------------------------------
        run([
            "gh", "pr", "create",
            "--title", MSG,
            "--body", MSG,
            "--draft",
            "--base", "main",
        ])
        print("✔ Draft PR created — review it on GitHub.")

    except sp.CalledProcessError as exc:
        print(f"❌ Command failed: {' '.join(exc.cmd)}", file=sys.stderr)
        sys.exit(exc.returncode)


if __name__ == "__main__":
    main()
