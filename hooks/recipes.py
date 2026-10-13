"""MkDocs hook: mark up recipe pages at build time.

Recipes follow the format in AGENTS.md. This hook turns that convention into
markup the theme can style, so nothing depends on JavaScript or shifts on load:

- the servings/times paragraph right before "Ingrédients" becomes a list of
  facts ("Pour 6 personnes", "Cuisson : 25 min à 180 °C"…);
- the ingredients table gets `data-ingredients` (an attribute, not a class:
  Material only styles `table:not([class])`);
- group rows (`| **Pâte** | | |`) get the `ingredients__group` class.
"""

import re

FACTS = re.compile(
    r"<p>((?:(?!</p>).)*)</p>(\s*<h[23] id=\"ingredients[^\"]*\")", re.DOTALL
)
TABLE = re.compile(r"<table>(\s*<thead>\s*<tr>\s*<th>Ingrédient</th>)")
GROUP_ROW = re.compile(
    r"<tr>(\s*<td><strong>[^<]*</strong></td>(?:\s*<td></td>)+\s*</tr>)"
)
# "Cuisson : 25 min à 180 °C" -> label "Cuisson", value "25 min à 180 °C".
LABELLED = re.compile(r"^([^:]{1,40}?) : (.+)$", re.DOTALL)


def _fact(sentence):
    match = LABELLED.match(sentence)
    if not match:
        return f"<li>{sentence}</li>"
    label, value = match.groups()
    return (
        f'<li><span class="recipe-facts__label">{label}</span> '
        f"{value}</li>"
    )


def _facts(match):
    text, heading = match.groups()
    # Sentences end with ". "; numbers use a decimal comma, so a period is
    # always a sentence boundary here.
    sentences = [s.strip() for s in re.split(r"\.\s+", text.strip().rstrip("."))]
    items = "".join(_fact(s) for s in sentences if s)
    return f'<ul class="recipe-facts">{items}</ul>{heading}'


def on_page_content(html, page, **kwargs):
    if not page.file.src_uri.startswith("docs/cook/"):
        return html
    html = FACTS.sub(_facts, html)
    html = TABLE.sub(r"<table data-ingredients>\1", html)
    return GROUP_ROW.sub(r'<tr class="ingredients__group">\1', html)
