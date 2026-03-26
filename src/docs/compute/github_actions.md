# GitHub Actions

## Quick checks in GitHub UI

- Open a PR -> **Checks** tab -> inspect failed job.
- Read failing step logs first, not the full workflow.
- Re-run only failed jobs when possible.

## Common workflow skeleton

```yaml
name: CI

on:
  pull_request:
  push:
    branches: [master]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -r requirements.txt
      - run: mkdocs build --strict -f mkdocs.yml -d site
```

## Fast triage checklist

1. Fails on `checkout`/`setup-*`: action version or runner issue.
2. Fails on dependency install: lock/dependency drift.
3. Fails on tests/build only in CI: env mismatch (Python version, OS, missing env var).
4. Flaky test: rerun once, then isolate and fix root cause.

## Safe defaults

- Pin language versions (`python-version`, `node-version`).
- Keep actions major pinned (`@v4`, `@v5`).
- Prefer explicit build command over implicit behavior.

## Add manual trigger

```yaml
on:
  workflow_dispatch:
```

Useful to test a workflow change without opening a PR.
