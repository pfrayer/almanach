# pytest

## Run tests fast

```shell
$ pytest -q                  # run all tests with concise output
$ pytest -x                  # stop on first failure
$ pytest -vv                 # verbose
$ pytest tests/unit/         # folder
$ pytest tests/test_api.py   # file
$ pytest tests/test_api.py::test_create_user  # single test
```

## Select tests

```shell
$ pytest -k "auth and not slow"     # by expression on names
$ pytest -m "integration"           # by marker
$ pytest --lf                       # last failed only
$ pytest --ff                       # failed first, then the rest
```

## Debug failures

```shell
$ pytest --pdb               # drop into pdb on failure
$ pytest -s                  # keep print/log output
$ pytest --maxfail=3         # stop test session after 3 failures
```

## Coverage (if pytest-cov installed)

```shell
$ pytest --cov=src --cov-report=term-missing  # coverage in terminal + list missing lines
$ pytest --cov=src --cov-report=xml           # coverage XML report (for CI tools)
```

## Markers

In `pyproject.toml`:

```toml
[tool.pytest.ini_options]
markers = [
    "slow: long-running tests",
    "integration: integration tests"
]
```

Then:

```shell
$ pytest -m "not slow"         # run tests excluding the slow marker
```

!!! tip "Daily default"
    Use `pytest -q --ff` locally for quick feedback.
