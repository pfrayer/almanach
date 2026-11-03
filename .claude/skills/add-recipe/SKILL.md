---
name: add-recipe
description: Add a cooking recipe to the site from a URL, pasted text, a photo or a book - French page in the house format, nav entry, index card, checks. Use whenever the user gives or mentions a recipe to add, import, translate or put on the almanach, even without saying "add-recipe".
argument-hint: <url | recipe text>
---

# Add a recipe: $ARGUMENTS

The format rules are in AGENTS.md ("Recipe format", "Ingredients table",
"Steps", "French typography"): follow them exactly. `src/docs/cook/focaccia.md`
is the reference page. This skill is the workflow around them.

## 1. Get the source

- URL: fetch the page and keep only the recipe (ingredients, steps, servings,
  times, temperatures, tips). Note the source name and URL for the last line.
- Text, photo or book: use what is given; for a book, the last line is
  `Recette tirée du livre « … ».` without a link.
- Never invent servings, times or temperatures that the source does not give:
  leave them out of the servings line.

## 2. Write the page

- Place: `src/docs/cook/<name>.md`, or a sub-folder when it belongs to a family
  (`cookies/<name>.md`). File name: lowercase, ASCII, `_` between words.
- Language: French, whatever the source language. Translate the recipe, do not
  paraphrase it; convert imperial units (cups, oz, lb, °F, inches) to metric
  with sensible rounding (1 cup of flour ≈ 125 g, of sugar ≈ 200 g, of liquid
  ≈ 24 cl; °F → °C rounded to 5).
- Group ingredients with bold rows when the recipe has parts (pâte, garniture…).
- Check every ingredient is used in the steps and every step's ingredient is
  listed.

## 3. Register it

1. `mkdocs.yml` → `nav:` → `Cooking 🇫🇷` → `Sucré`, `Salé` or `Bases`, at its
   alphabetical place.
2. `src/docs/cook/index.md` → a card in the same section, at its alphabetical
   place: `-   [**Title**](path.md)` then a blank line and a one-line summary
   indented by 4 spaces, like the cards around it.

## 4. Check

- The PostToolUse hook lints each edited cooking page (`.claude/hooks/lint-recipe.py`):
  fix everything it reports. Run it by hand with
  `python3 -I .claude/hooks/lint-recipe.py src/docs/cook/<path>.md`.
- Ask the `recipe-reviewer` agent to review the new page (rules a script
  cannot check).
- `mkdocs build --strict` must pass (the Stop hook runs it; it is the CI gate).

## 5. Commit

Only when the user asked for commits: one commit per recipe,
`feat(cook): <recette>` (e.g. `feat(cook): focaccia`). Otherwise tell the user
the page is ready and give its path.
