---
description: "pyenv cheatsheet: install and switch Python versions, manage virtualenvs and set per-project versions."
---

# pyenv

## Install `pyenv`

```shell
$ sudo apt-get install -y make build-essential git libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

$ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```

Also, add the following to your `~/.bashrc` or `~/.zshrc`:

```bash
# PyEnv
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(${HOME}/.pyenv/bin/pyenv init --path)"
eval "$(${HOME}/.pyenv/bin/pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

## Cheatsheet

Main usage is:

- Install a new Python version
- Create a new `virtualenv` using this version
- Make your project use this `virtualenv`
- Install dependencies / run your project inside this `virtualenv`

```shell
$ pyenv install 3.12.1
$ pyenv rehash
$ pyenv virtualenv 3.12.1 my-project
$ cd ~/workspace/my-project
$ pyenv local my-project
$ python --version
# Python 3.12.1
```

### `pyenv install`

List available remote Python versions you can install:

```shell
$ pyenv install -l
```

Install Python 3.9.12:

```shell
$ pyenv install 3.9.12
$ pyenv rehash
```

### `pyenv versions`

List locally installed versions:

```shell
$ pyenv versions
```

### `pyenv global`

Set the default Python version system-wide:

```shell
$ pyenv global 3.12.1
```

### `pyenv shell`

Override the version for the current shell session only (takes precedence over `global` and `local`):

```shell
$ pyenv shell 3.10.0
$ pyenv shell --unset
```

### `pyenv local`

Set the version for the current directory. Creates a `.python-version` file — pyenv reads it automatically whenever you `cd` into the directory.

```shell
$ pwd
# ~/workspace/my-project
$ pyenv local my-pyenv-virtualenv-name   # use a virtualenv
$ pyenv local 3.12.1                     # or a plain Python version
```

Unset:

```shell
$ pyenv local --unset
# or
$ rm .python-version
```

### `pyenv virtualenv`

List locally created `virtualenv`s:

```shell
$ pyenv virtualenvs
```

Create a new `virtualenv`:

```shell
# From system's Python version with name `my-project`:
$ pyenv virtualenv my-project
# From a given Python version:
$ pyenv virtualenv 3.9.12 my-other-project
```

Delete an existing `virtualenv`:

```shell
$ pyenv uninstall my-project
```

### `pyenv which` / `pyenv exec`

```shell
# Show the full path of a binary resolved by pyenv
$ pyenv which python
# ~/.pyenv/versions/my-project/bin/python

$ pyenv which pip

# Run a command with a specific version without activating it
$ pyenv exec python -c "import sys; print(sys.version)"
```

## Upgrade `pyenv`

```shell
$ pyenv update    # requires pyenv-update plugin (installed by pyenv-installer)
# or manually:
$ cd $(pyenv root) && git pull
```
