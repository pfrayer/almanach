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

## Conventions

### Content language

Compute docs are in English. Cooking docs are in French. **Always write in the section's language, regardless of the language used in the prompt.**

### Adding a new page

1. Create the markdown file in the appropriate `src/docs/` subdirectory
2. Add the page to the `nav:` section in `mkdocs.yml` — it won't appear in navigation otherwise

### Recipe format

Follow the most recent recipes (e.g. `src/docs/cook/focaccia.md`, `poulet_gaston_gerard.md`); older ones like `brownie.md` predate this format:

1. Frontmatter with a one-sentence French `description`
2. `# Title`, then one line with servings and times (préparation, repos/levée, cuisson with temperature in °C)
3. `## Ingrédients`: a `| Ingrédient | Quantité | Remarque |` table, with bold rows (`| **Pâte** | | |`) to group ingredients. Use metric units and French abbreviations (`c. à s.`, `c. à c.`)
4. `## Étapes`: numbered list starting at 1, each step opening with a bold title (`1. **Préchauffer le four** à 200 °C.` or `2. **Former la pâte :** …`)
5. Optional `!!! tip` admonition for storage, equipment or substitutions
6. Last line: `[Source : <name>](<url>){target=_blank}`, or plain text when there is no URL

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
