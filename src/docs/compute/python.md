# Python

## `pyenv`

### Install `pyenv`

```shell
$ sudo apt-get install -y make build-essential git libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev

$ curl -L https://raw.githubusercontent.com/pyenv/pyenv-installer/master/bin/pyenv-installer | bash
```
Also set the following in your `~/.bashrc` or `~/.zshrc`:
```bash
# PyEnv
export PATH="${HOME}/.pyenv/bin:${PATH}"
eval "$(${HOME}/.pyenv/bin/pyenv init --path)"
eval "$(${HOME}/.pyenv/bin/pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

### Cheatsheet

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

#### `pyenv install`

List available remote Python versions you can install:
```shell
$ pyenv install -l
```
Install Python 3.9.12:
```shell
$ pyenv install 3.9.12
$ pyenv rehash
```

#### `pyenv versions`

List locally installed versions:
```shell
$ pyenv versions
```

#### `pyenv local`

Sets a local application-specific pyenv virtualenv in the current directory:
```shell
$ pwd
# ~/workspace/my-project
$ pyenv local my-pyenv-virtualenv-name
```

Sets a local application-specific pyenv virtualenv in the current directory:
```shell
$ pyenv local 2.7.6
```

Unset the local version:
```shell
$ pyenv local --unset
# or
$ rm .python-version
```

#### `pyenv virtualenv`

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

### Upgrade `pyenv`

```shell
$ cd $(pyenv root)
$ git pull
```
