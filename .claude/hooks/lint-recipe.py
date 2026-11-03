#!/usr/bin/env python3
"""Lint the mechanical rules of AGENTS.md ("Recipe format") on cooking pages.

Usage:
  lint-recipe.py FILE...      lint the given files (exit 1 on problems)
  lint-recipe.py              Claude Code PostToolUse hook: reads the hook
                              JSON on stdin, lints the edited file if it is
                              under src/docs/cook/, exit 2 sends the problems
                              back to Claude.

Only rules a script can check without false positives live here; the rest
(ingredients used in the steps, infinitive titles, no invented times) is for
the recipe-reviewer agent.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COOK = ROOT / "src" / "docs" / "cook"

TEXT_RULES = [
    (re.compile(r"(?i)oeu|oeil"), "write the ligature œ (œuf, bœuf, cœur, œil)"),
    (re.compile(r"(?i)cuill[eè]res? à (soupe|caf[eé])|\bcuil\.|c\. à caf[eé]|c\.à\.[sc]"),
     "spoons are written `c. à s.` / `c. à c.`"),
    (re.compile(r"\d°"), "a space goes between a number and its unit (`180 °C`)"),
    (re.compile(r"°F|(?i:\b(cups?|tbsp|tsp|oz|lbs?|inch(es)?)\b)"),
     "convert imperial units to metric"),
    (re.compile("[\u00a0\u202f]"), "no non-breaking spaces, plain spaces only"),
    (re.compile("[\u2018\u2019]"), "straight apostrophes only (')"),
    (re.compile("[\u201c\u201d]"), "French quotes « … » instead of “ ”"),
    (re.compile("[\u2010\u2011]"), "plain hyphens only (-)"),
]

HEADING = re.compile(r"^#{1,6} ")
INGREDIENTS = re.compile(r"^#{2,3} Ingrédients\s*$")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def lint_table(lines, problems):
    in_table = False
    for n, line in enumerate(lines, 1):
        if INGREDIENTS.match(line):
            in_table = True
            continue
        if HEADING.match(line):
            in_table = False
        if not in_table or not line.startswith("|"):
            continue
        if set(line.strip()) <= set("|-: "):
            if line.strip() != "|---|---|---|":
                problems.append((n, "separator row must be exactly `|---|---|---|`"))
            continue
        row = cells(line)
        if row[:3] == ["Ingrédient", "Quantité", "Remarque"]:
            continue
        if len(row) != 3:
            problems.append((n, "ingredient rows have exactly 3 columns"))
            continue
        name, qty, note = row
        if name.startswith("**"):  # group row
            continue
        if name[:1].islower():
            problems.append((n, f"ingredient starts with a capital letter: `{name}`"))
        if qty in ("", "-", "—", "–"):
            problems.append((n, f"`{name}`: no empty or `-` quantity (use `Au goût`, `Un filet`…)"))
        if re.search(r"\d+/\d+", qty):
            problems.append((n, f"`{name}`: ranges with `à` (`2 à 3`), fractions as ½ / ¼"))
        if note[:1].islower():
            problems.append((n, f"`{name}`: the remark starts with a capital letter"))


def lint_registration(path, problems):
    if path.name == "index.md":
        return
    in_docs = path.relative_to(ROOT / "src").as_posix()
    if in_docs not in (ROOT / "mkdocs.yml").read_text(encoding="utf-8"):
        problems.append((0, f"missing from the `nav:` of mkdocs.yml ({in_docs})"))
    in_cook = path.relative_to(COOK).as_posix()
    if f"]({in_cook})" not in (COOK / "index.md").read_text(encoding="utf-8"):
        problems.append((0, f"no card linking `{in_cook}` in src/docs/cook/index.md"))


def lint(path):
    path = Path(path).resolve()
    lines = path.read_text(encoding="utf-8").splitlines()
    problems = []
    for n, line in enumerate(lines, 1):
        if line.startswith(("[Source", "<", "http")):
            continue  # source line keeps the original title / URL
        text = re.sub(r"\]\([^)]*\)|`[^`]*`", "", line)  # skip URLs and code
        for rule, message in TEXT_RULES:
            if rule.search(text):
                problems.append((n, message))
    lint_table(lines, problems)
    lint_registration(path, problems)
    return problems


def report(path, problems):
    rel = Path(path).resolve().relative_to(ROOT)
    return "\n".join(f"{rel}:{n}: {msg}" if n else f"{rel}: {msg}" for n, msg in problems)


def main():
    if len(sys.argv) > 1:
        status = 0
        for f in sys.argv[1:]:
            problems = lint(f)
            if problems:
                print(report(f, problems))
                status = 1
        return status

    event = json.load(sys.stdin)
    f = event.get("tool_input", {}).get("file_path") or ""
    path = Path(f).resolve() if f else None
    if not path or path.suffix != ".md" or COOK not in path.parents or not path.exists():
        return 0
    problems = lint(path)
    if problems:
        print("Recipe format (AGENTS.md) problems:\n" + report(path, problems), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
