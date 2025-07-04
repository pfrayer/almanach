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

## List

### Sort list of dict based on a dict's key

```python
my_unsorted_list = [ {"name": "Julien", "age": 12}, {"name": "Xavier", "age": 20}, {"name": "Alex", "age": 43}]
sorted(my_unsorted_list, key=lambda d: d["name"])
# Output
# [{'name': 'Alex', 'age': 43}, {'name': 'Julien', 'age': 12}, {'name': 'Xavier', 'age': 20}]
```

## Archives

Create a `.tar.gz` archive. Let say you have this source folder structure:
```
.
└── source-dir
    ├── file1
    ├── file2
    └── file3
```
Then:
```python
import tarfile

with tarfile.open(f"source-dir.tgz", "w:gz") as tar:
    tar.add("source-dir")
```
Will create a `source-dir.tgz` archive containing the exact same structure (keeping the `source-dir`):

To only add files to the archives (without keeping `source-dir`):
```python
import os
import tarfile

with tarfile.open(f"source-dir.tgz", "w:gz") as tar:
    for filename in os.listdir("source-dir"):
        tar.add(
            os.path.join("source-dir", filename), # source file path
            arcname=filename,                     # name of the file in the archive
            recursive=False,                      # should we keep the source structure, aka keep "source-dir/filename" ?
        )
```
Will create a `source-dir.tgz` archive with this structure:
```
.
├── file1
├── file2
└── file3
```
Other compression algorithms are supported (`bz2`, `lzma` etc). [Official doc](https://docs.python.org/fr/3.13/library/archiving.html){target=_blank}

## Select random item in a list

```python
import random

my_list = [1, 2, 3, 4]
random.choice(my_list)
# 2
```
