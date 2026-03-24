# General

## Sort a list of dicts by key

```python
my_unsorted_list = [
    {"name": "Julien", "age": 12},
    {"name": "Xavier", "age": 20},
    {"name": "Alex", "age": 43},
]
sorted(my_unsorted_list, key=lambda d: d["name"])
# [{'name': 'Alex', 'age': 43}, {'name': 'Julien', 'age': 12}, {'name': 'Xavier', 'age': 20}]
```

## Random item from a list

```python
import random

my_list = [1, 2, 3, 4]
random.choice(my_list)
# 2
```

## `.tar.gz` archives

Create a `.tar.gz` archive. Suppose you have this source folder structure:

```text
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

Will create a `source-dir.tgz` archive containing the exact same structure (keeping the `source-dir`).

To only add files to the archives (without keeping `source-dir`):

```python
import os
import tarfile

with tarfile.open(f"source-dir.tgz", "w:gz") as tar:
    for filename in os.listdir("source-dir"):
        tar.add(
            os.path.join("source-dir", filename),
            arcname=filename,
            recursive=False,
        )
```

Will create a `source-dir.tgz` archive with this structure:

```text
.
├── file1
├── file2
└── file3
```

Other compression algorithms are supported (`bz2`, `lzma` etc). [Official doc](https://docs.python.org/3/library/archiving.html){target=_blank}
