# Poetry

## Create and use a project

```shell
$ poetry new my-project        # create a new package/project scaffold
$ cd my-project                # move into the project directory
$ poetry install               # create venv and install dependencies from lock/project
$ poetry shell                 # open a shell inside the Poetry virtualenv
```

Run without entering shell:

```shell
$ poetry run python -m my_project  # run module with project virtualenv without activating shell
```

## Add / remove dependencies

```shell
# runtime deps
$ poetry add requests                # add package to main dependencies and lock it

# dev deps
$ poetry add --group dev pytest ruff # add packages to dev group only

# remove
$ poetry remove requests             # remove dependency and update lock file
```

## Lock and sync

```shell
# update lock file with current constraints
$ poetry lock                     # resolve versions and regenerate poetry.lock

# install exactly what lock defines
$ poetry install --sync           # install exactly lock content, remove extra packages from venv
```

## Useful daily commands

```shell
$ poetry show --tree               # display dependency tree with transitive dependencies
$ poetry env info                  # show current virtualenv path and interpreter info
$ poetry run pytest -q             # run tests using project virtualenv
$ poetry run python -V             # print Python version from project virtualenv
```

## Export requirements (for Docker/CI)

```shell
$ poetry self add poetry-plugin-export                                  # install export plugin in Poetry itself
$ poetry export -f requirements.txt --output requirements.txt --without-hashes  # generate pip-style requirements.txt
```

!!! tip "Simple workflow"
    `poetry add ...` -> `poetry run pytest` -> `poetry lock` -> commit `pyproject.toml` + `poetry.lock`.
