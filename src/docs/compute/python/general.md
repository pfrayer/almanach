# General

## List & dict comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]
evens = [x for x in range(20) if x % 2 == 0]

# Dict comprehension
lengths = {word: len(word) for word in ["foo", "bar", "baz"]}

# Set comprehension
unique_lengths = {len(word) for word in ["foo", "bar", "baz"]}

# Flatten a list of lists
nested = [[1, 2], [3, 4], [5]]
flat = [x for sublist in nested for x in sublist]
# or
import itertools
flat = list(itertools.chain.from_iterable(nested))
```

---

## Sorting

```python
# Sort list of dicts by key
users = [{"name": "Julien", "age": 12}, {"name": "Alex", "age": 43}]
sorted(users, key=lambda d: d["name"])
sorted(users, key=lambda d: d["age"], reverse=True)

# Sort by multiple keys
sorted(users, key=lambda d: (d["age"], d["name"]))

# min / max with key
youngest = min(users, key=lambda d: d["age"])
```

---

## collections

```python
from collections import defaultdict, Counter, namedtuple

# defaultdict — no KeyError on missing keys
groups = defaultdict(list)
for user in users:
    groups[user["age"]].append(user["name"])

# Counter — count occurrences
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
c = Counter(words)
# Counter({'apple': 3, 'banana': 2, 'cherry': 1})
c.most_common(2)
# [('apple', 3), ('banana', 2)]

# namedtuple — lightweight immutable struct
Point = namedtuple("Point", ["x", "y"])
p = Point(1, 2)
p.x  # 1
```

---

## dataclasses

```python
from dataclasses import dataclass, field

@dataclass
class User:
    name: str
    age: int
    tags: list = field(default_factory=list)

u = User("Alice", 30)
u.name   # "Alice"

# With ordering and immutability
@dataclass(order=True, frozen=True)
class Point:
    x: float
    y: float
```

---

## Strings & f-strings

```python
name = "world"
pi = 3.14159

f"Hello, {name}!"
f"Pi is {pi:.2f}"                  # "Pi is 3.14"
f"{1000000:,}"                     # "1,000,000"
f"{'left':<10}|{'right':>10}"      # padding
f"{name!r}"                        # repr()
f"{pi=}"                           # debug: "pi=3.14159" (Python 3.8+)

# Multi-line
msg = (
    f"Name: {name}\n"
    f"Pi:   {pi:.4f}"
)
```

---

## Regex

```python
import re

text = "Order #1234 placed on 2024-01-15"

# Search (first match)
m = re.search(r"\d{4}-\d{2}-\d{2}", text)
m.group()  # "2024-01-15"

# Find all
re.findall(r"\d+", text)   # ["1234", "2024", "01", "15"]

# Named groups
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
m.group("year")   # "2024"

# Substitute
re.sub(r"\d+", "X", text)  # "Order #X placed on X-X-X"

# Compile for reuse
pattern = re.compile(r"\d{4}-\d{2}-\d{2}")
pattern.findall(text)
```

---

## Dates

```python
from datetime import datetime, timedelta, timezone

now = datetime.now()
utcnow = datetime.now(timezone.utc)

# Parse
dt = datetime.strptime("2024-01-15 14:30", "%Y-%m-%d %H:%M")

# Format
dt.strftime("%d/%m/%Y")            # "15/01/2024"

# Arithmetic
tomorrow = now + timedelta(days=1)
two_weeks_ago = now - timedelta(weeks=2)
delta = datetime(2025, 1, 1) - now
delta.days

# ISO format (round-trips)
iso = now.isoformat()
datetime.fromisoformat(iso)
```

---

## pathlib

```python
from pathlib import Path

p = Path("/etc/nginx/nginx.conf")
p.name          # "nginx.conf"
p.stem          # "nginx"
p.suffix        # ".conf"
p.parent        # Path("/etc/nginx")
p.exists()
p.is_file()
p.is_dir()

# Read / write
text = p.read_text()
p.write_text("content")
data = p.read_bytes()

# Navigate
base = Path(".")
config = base / "config" / "settings.yaml"

# Glob
for f in Path(".").glob("**/*.py"):
    print(f)

# Create directories
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

---

## JSON, YAML, CSV

```python
import json

# JSON
data = json.loads('{"key": "value"}')
json.dumps(data, indent=2)
with open("file.json") as f:
    data = json.load(f)
with open("file.json", "w") as f:
    json.dump(data, f, indent=2)

# YAML (pip install pyyaml)
import yaml
with open("file.yaml") as f:
    data = yaml.safe_load(f)
with open("out.yaml", "w") as f:
    yaml.dump(data, f, default_flow_style=False)

# CSV
import csv
with open("file.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)             # list of dicts

with open("out.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(rows)
```

---

## tar.gz archives

```python
import tarfile

# Create (keeps source-dir/ prefix)
with tarfile.open("archive.tgz", "w:gz") as tar:
    tar.add("source-dir")

# Create (files only, no prefix)
import os
with tarfile.open("archive.tgz", "w:gz") as tar:
    for filename in os.listdir("source-dir"):
        tar.add(os.path.join("source-dir", filename), arcname=filename)

# Extract
with tarfile.open("archive.tgz") as tar:
    tar.extractall("output-dir")

# List contents
with tarfile.open("archive.tgz") as tar:
    tar.list()
```

Supported modes: `w:gz`, `w:bz2`, `w:xz`, `r:*` (auto-detect).

---

## subprocess

```python
import subprocess

# Run and capture output
result = subprocess.run(["ls", "-la"], capture_output=True, text=True)
result.stdout
result.returncode

# Raise on error
result = subprocess.run(["git", "status"], capture_output=True, text=True, check=True)

# Shell pipeline (avoid when possible)
result = subprocess.run("ps aux | grep python", shell=True, capture_output=True, text=True)

# Stream output live
with subprocess.Popen(["tail", "-f", "app.log"], stdout=subprocess.PIPE, text=True) as proc:
    for line in proc.stdout:
        print(line, end="")
```

---

## itertools

```python
import itertools

# chain — flatten iterables
list(itertools.chain([1, 2], [3, 4], [5]))   # [1, 2, 3, 4, 5]

# groupby — group consecutive elements (input must be sorted)
data = sorted([{"env": "prod"}, {"env": "dev"}, {"env": "prod"}], key=lambda x: x["env"])
for key, group in itertools.groupby(data, key=lambda x: x["env"]):
    print(key, list(group))

# islice — lazy slice of any iterable
list(itertools.islice(range(1000), 5, 10))   # [5, 6, 7, 8, 9]

# product — cartesian product
list(itertools.product([1, 2], ["a", "b"]))  # [(1,'a'), (1,'b'), (2,'a'), (2,'b')]

# batched (Python 3.12+) — split iterable into chunks
list(itertools.batched(range(10), 3))        # [(0,1,2), (3,4,5), (6,7,8), (9,)]
```

---

## Context managers

```python
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    import time
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"{label}: {elapsed:.3f}s")

with timer("my block"):
    time.sleep(0.5)
```

---

## Debugging & perf

```python
# Drop into debugger
breakpoint()                  # Python 3.7+ (replaces import pdb; pdb.set_trace())
# pdb commands: n (next), s (step), c (continue), p <var>, l (list), q (quit)

# Quick timing
import timeit
timeit.timeit("'-'.join(str(n) for n in range(100))", number=10000)

# One-liner from shell
python -m timeit "'-'.join(str(n) for n in range(100))"
```

---

## logging

```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning")
logger.error("error")
logger.exception("with traceback", exc_info=True)  # inside except block

# File handler
handler = logging.FileHandler("app.log")
handler.setLevel(logging.WARNING)
logger.addHandler(handler)
```
