# Agent Instructions

## Build & Serve

```shell
pip install -r requirements.txt
mkdocs serve -a "0.0.0.0:8080"
mkdocs build --strict -f mkdocs.yml -d site

# Or with Docker (serves on port 8181)
docker build -t almanach . && docker run --rm -p 8181:8181 almanach
```

There are no tests or linters configured: `mkdocs build --strict` is the only gate.

## Architecture

This is a **Material for MkDocs** documentation site ("Compute & Cook") serving two categories of cheatsheets:

- **Computers** (`src/docs/compute/`) — Technical cheatsheets written in **English**
- **Cooking** (`src/docs/cook/`) — Recipes written in **French**

Content lives under `src/` (configured via `docs_dir: src` in `mkdocs.yml`). The site navigation is manually defined in `mkdocs.yml` under `nav:` — new pages must be added there to appear.

Custom theming uses glassmorphism-style CSS in `src/assets/css/` (backdrop blur, transparent overlays). Fonts are self-hosted under `src/assets/fonts/`.

Theme overrides live in `overrides/` (`custom_dir`): pages under `src/docs/cook/` get a French interface and `<html lang="fr">` through `src/docs/cook/.meta.yml` (`locale: fr`), the rest stays in English. `hooks/recipes.py` marks up recipe pages at build time; `src/assets/js/` holds the small client scripts (language sync on instant navigation, ingredient checklist).

## Conventions

### Content language

Compute docs are in English. Cooking docs are in French. **Always write in the section's language, regardless of the language used in the prompt.**

### Adding a new page

1. Create the markdown file in the appropriate `src/docs/` subdirectory
2. Add the page to the `nav:` section in `mkdocs.yml` — it won't appear in navigation otherwise. Keep each group sorted alphabetically
3. Add it to its section's index page: a card in `src/docs/cook/index.md` (title link plus a one-line summary) or a line in the alphabetical list of `src/docs/compute/index.md`

### Recipe format

All recipes follow this format (reference: `src/docs/cook/focaccia.md`):

1. Frontmatter with a one-sentence French `description`
2. `# Title`, then one line with servings and times, in this order: `Pour 4 personnes. Préparation : 20 min. Repos : 30 min. Cuisson : 25 min à 180 °C.` Only include what is known — never invent servings or durations
   `hooks/recipes.py` turns this line into chips at build time: keep it a single paragraph right before `## Ingrédients`, sentences separated by `. `, labels written `Label : valeur`
3. `## Ingrédients`: a `| Ingrédient | Quantité | Remarque |` table (`|---|---|---|`, no column padding), with bold rows (`| **Pâte** | | |`) to group ingredients
4. `## Étapes`: numbered list starting at 1, each step opening with a bold title (`1. **Préchauffer le four** à 200 °C.` or `2. **Former la pâte :** …`)
5. Optional `!!! tip` admonition for storage, equipment, substitutions or variants
6. Last line: `[Source : <name>](<url>){target=_blank}`, or plain text when there is no URL (`Recette tirée du livre « … ».`)

A page holding several recipes (e.g. `tartiflette.md`) uses one `##` per recipe, followed by its servings line, then `### Ingrédients` and `### Étapes`.

#### Ingredients table

- **Ingrédient** starts with a capital letter and holds only the name (`Huile de noisette`, not `huile de noisette (ou de noix)`); alternatives, preparation and "Facultatif" go in **Remarque** (`Ou huile de noix`, `Hachée`, `Facultatif`)
- **Quantité** uses metric units (`g`, `kg`, `cl`, `l`, `cm`) and the abbreviations `c. à s.` / `c. à c.` — never `cuillère à soupe`, `cuil.`, `c. à café`. Write numbers as digits (`1 pincée`, not `Une pincée`), ranges with `à` (`2 à 3`, not `2/3`), fractions as `½` / `¼`. For unmeasured amounts use `Au goût`, `Un filet`, `Quelques brins`… — never `-` or an empty cell
- **Remarque** starts with a capital letter, or is left empty
- Every listed ingredient must be used in the steps, and vice versa

#### Steps

- The bold title is an infinitive (`**Faire fondre le chocolat**`, `**Cuire la crème :**`); the rest of the step uses the imperative with "vous" (`mélangez`, `faites cuire`). Never mix both in the body
- Each step is a full sentence ending with a period

#### French typography

- A space before `:`, `;`, `!`, `?` and between a number and its unit (`180 °C`, `20 cm`, `30 min`, `70 %`); ranges and dimensions as `30 à 40 min`, `23 × 33 cm`
- Proper ligatures and accents: `œuf` (not `oeuf`), capital accents (`À la cuisson`, `Étaler`)
- Straight apostrophes (`'`), French quotes (`« … »`), plain spaces and hyphens — no non-breaking spaces or special Unicode hyphens
- Cheese and product names that are common nouns stay lowercase in running text (`saint-nectaire`, `ossau-iraty`, `comté`)

When translating a recipe, convert imperial units (cups, °F, inches) to metric.

### Commits

Conventional commits scoped by section: `feat(cook): <recette>` for recipes, `feat(<tool>): …` for compute cheatsheets (e.g. `feat(claude): …`). One commit per recipe or page.

### Markdown features available

The site enables several PyMdown extensions — use them freely:

- Fenced code blocks with language-specific syntax highlighting and line numbers
- Admonitions (`!!! tip`, `!!! note`, `!!! warning`, `!!! danger`)
- Content tabs (`=== "Tab 1"`)
- Code annotations, inline code highlighting
- Task lists, definition lists, keyboard keys (`++ctrl+c++`)
- Attribute lists and `md_in_html` for embedding HTML with Material Design classes

### Formatting

Per `.editorconfig`: UTF-8, LF line endings, trailing whitespace trimmed, 4-space indent (2-space for YAML).

### Deployment

Pushes to `master` trigger a GitHub Actions workflow that deploys via SSH. There is no build step in CI — the remote host builds the site.

### Dependencies

Renovate is configured to auto-update minor and patch versions only (majors are disabled).
