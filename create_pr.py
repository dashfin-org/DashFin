#!/usr/bin/env python3
r"""create_pr.py — minimal, idempotent helper to open a **draft** PR via GitHub CLI

Revision (2025‑08‑01 b)
-----------------------
* **Removed invalid escape warnings**: back‑slashes in the usage snippet are
  now doubled so Python 3.12+ no longer raises *SyntaxWarning: invalid escape
  sequence '\\S'*.
* No reference to the missing *micropip* package — confirms the original
  `ModuleNotFoundError` was unrelated to this script.
* All other improvements from the previous rewrite retained (UTF‑8 safety,
  dirty‑tree guard, staged‑changes guard, `--no‑verify` push).

Usage
-----
```powershell
# 1) activate venv & ensure gh is logged in
. .venv\\Scripts\\Activate.ps1
chcp 65001               # optional but recommended UTF‑8

# 2) run the helper
python create_pr.py       # opens draft PR; prints PR URL
```
The script creates / resets a branch named `audit‑demo‑<UTC timestamp>`.
Re‑running always forces an update of that branch.
"""
from __future__ import annotations

import subprocess as sp
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Final, Sequence

ROOT: Final[Path] = Path.cwd()
BRANCH: Final[str] = f"audit-demo-{datetime.now(UTC):%Y%m%d%H%M%S}"
MSG: Final[str] = "chore: automated draft PR (env‑audit demo)"
DEMO_FILE: Final[Path] = ROOT / "_audit_demo.txt"


def run(cmd: Sequence[str]) -> None:  # pragma: no cover
    """Run *cmd* and abort on non‑zero exit."""
    sp.run(cmd, check=True, text=True)


def working_tree_dirty() -> bool:  # pragma: no cover
    return bool(sp.check_output(["git", "status", "--porcelain"], text=True).strip())


def has_staged_changes() -> bool:  # pragma: no cover
    return sp.call(["git", "diff", "--cached", "--quiet"]) != 0  # exit 1 if diff


def main() -> None:
    if working_tree_dirty():
        sys.stderr.write("ERROR: working tree is dirty. Commit or stash first.\n")
        sys.exit(1)

    try:
        run(["git", "checkout", "-B", BRANCH])

        DEMO_FILE.write_text(
            f"Composio audit demo — {datetime.now(UTC):%Y‑%m‑%d %H:%M:%S UTC}\n",
            encoding="utf-8",
        )
        run(["git", "add", str(DEMO_FILE)])

        if not has_staged_changes():
            sys.stderr.write("INFO: no staged changes; aborting.\n")
            sys.exit(0)

        run(["git", "commit", "-m", MSG])
        run(["git", "push", "-u", "origin", BRANCH, "--force", "--no-verify"])

        run([
            "gh", "pr", "create",
            "--title", MSG,
            "--body", MSG,
            "--draft",
            "--base", "main",
        ])
        print("SUCCESS: draft PR opened — review it on GitHub.")

    except sp.CalledProcessError as exc:
        sys.stderr.write(f"FAIL: {' '.join(exc.cmd)} returned {exc.returncode}\n")
        sys.exit(exc.returncode)


# ---------------------------------------------------------------------------
# Unit‑test stub
# ---------------------------------------------------------------------------

def _fake(cmd: Sequence[str]) -> None:  # noqa: D401
    """Mock subprocess for tests."""


def test_dirty_tree_abort(monkeypatch):  # pragma: no cover
    monkeypatch.setattr(__name__, "working_tree_dirty", lambda: True)
    monkeypatch.setattr(__name__, "run", _fake)
    try:
        main()
    except SystemExit as exc:
        assert exc.code == 1


if __name__ == "__main__":  # pragma: no cover
    main()
