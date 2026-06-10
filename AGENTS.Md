# Copilot Instructions

## Build & Serve

```shell
pip install -r requirements.txt
mkdocs serve -a "0.0.0.0:8080"
mkdocs build --strict -f mkdocs.yml -d site
```

There are no tests or linters configured.

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
