---
description: "jq and yq cheatsheet: query, filter, map and transform JSON and YAML data from the command line."
---

# `jq` / `yq`

## jq

### Flags

| Flag | Effect |
|------|--------|
| `-r` | Raw output — strips JSON string quotes |
| `-c` | Compact output (single line) |
| `-e` | Exit non-zero if last output is `false` or `null` |
| `-n` | No input — use `null` as input (useful with `--arg`) |
| `-s` | Slurp — read all inputs into a single array |
| `--arg name val` | Bind shell string to `$name` |
| `--argjson name val` | Bind parsed JSON to `$name` |
| `--rawfile name file` | Bind raw file content to `$name` |

### Field access

```shell
# Pretty-print
$ echo '{"foo": "bar"}' | jq .
{
  "foo": "bar"
}

# Access a field (quoted string output)
$ echo '{"foo": "bar"}' | jq '.foo'
"bar"

# Raw output (unquoted string)
$ echo '{"foo": "bar"}' | jq -r '.foo'
bar

# Nested access
$ echo '{"a": {"b": {"c": 42}}}' | jq '.a.b.c'
42

# Optional field (no error if missing)
$ echo '{"foo": "bar"}' | jq '.missing?'
null
```

### Arrays

```shell
# Iterate — emit each element
$ echo '[{"name": "alice"}, {"name": "bob"}]' | jq '.[]'
{"name": "alice"}
{"name": "bob"}

# Index
$ echo '[10, 20, 30]' | jq '.[0]'
10

# Slice
$ echo '[10, 20, 30, 40]' | jq '.[1:3]'
[20, 30]

# Last element
$ echo '[10, 20, 30]' | jq '.[-1]'
30

# Length
$ echo '[1, 2, 3]' | jq 'length'
3

# Map over array
$ echo '[1, 2, 3]' | jq 'map(. * 2)'
[2, 4, 6]

# Flatten nested arrays
$ echo '[[1, 2], [3, [4, 5]]]' | jq 'flatten'
[1, 2, 3, 4, 5]

# Unique values
$ echo '[1, 2, 2, 3, 1]' | jq 'unique'
[1, 2, 3]

# Sort
$ echo '[3, 1, 2]' | jq 'sort'
[1, 2, 3]

# Sort by field
$ echo '[{"n":3},{"n":1},{"n":2}]' | jq 'sort_by(.n)'
[{"n":1},{"n":2},{"n":3}]
```

### Select / filter

```shell
# Keep elements matching a condition
$ echo '[{"id":1,"name":"alice"},{"id":2,"name":"bob"}]' \
    | jq '.[] | select(.name == "bob")'
{"id": 2, "name": "bob"}

# Extract a single field from matched elements
$ echo '[{"id":1,"name":"alice"},{"id":2,"name":"bob"}]' \
    | jq '.[] | select(.name == "bob") | .id'
2

# Select where a sub-array contains a value
$ echo '[{"id":1,"users":["alice","bob"]},{"id":2,"users":["alice"]},{"id":3,"users":["bob"]}]' \
    | jq '.[] | select(.users[] | contains("alice")) | .id'
1
2

# Select with regex
$ echo '[{"name":"foo-prod"},{"name":"bar-dev"}]' \
    | jq '.[] | select(.name | test("prod$")) | .name'
"foo-prod"

# Rebuild filtered array (wrapping with map + select)
$ echo '[1, 2, 3, 4, 5]' | jq '[.[] | select(. > 3)]'
[4, 5]
```

### Transform / reshape

```shell
# Construct a new object
$ echo '{"first":"John","last":"Doe","age":30}' \
    | jq '{fullname: "\(.first) \(.last)", age}'
{"fullname": "John Doe", "age": 30}

# Extract keys / values
$ echo '{"a":1,"b":2}' | jq 'keys'
["a", "b"]
$ echo '{"a":1,"b":2}' | jq '[.[] ]'  # or: values
[1, 2]

# to_entries / from_entries — pivot object to array and back
$ echo '{"a":1,"b":2}' | jq 'to_entries'
[{"key":"a","value":1},{"key":"b","value":2}]

$ echo '{"a":1,"b":2}' | jq '[to_entries[] | select(.value > 1) | .key]'
["b"]

# with_entries shorthand (to_entries | map(…) | from_entries)
$ echo '{"a":1,"b":2}' | jq 'with_entries(.value += 10)'
{"a": 11, "b": 12}

# String interpolation
$ echo '{"name":"world"}' | jq '"Hello, \(.name)!"'
"Hello, world!"

# Group and count
$ echo '[{"env":"prod"},{"env":"dev"},{"env":"prod"}]' \
    | jq 'group_by(.env) | map({env: .[0].env, count: length})'
[{"env":"dev","count":1},{"env":"prod","count":2}]
```

### Modify

```shell
# Add / override a field
$ echo '{"foo":"bar"}' | jq '. + {"baz": "new"}'
{"foo": "bar", "baz": "new"}

# Update a field in-place
$ echo '{"foo":"bar"}' | jq '.foo = "updated"'
{"foo": "updated"}

# Delete a field
$ echo '{"foo":"bar","keep":"me"}' | jq 'del(.foo)'
{"keep": "me"}

# Append to an array
$ echo '[1,2,3]' | jq '. + [4]'
[1, 2, 3, 4]

# Update a nested field across all array elements
$ echo '[{"x":1},{"x":2}]' | jq '[.[] | .x += 10]'
[{"x": 11}, {"x": 12}]
```

### Variables & args

```shell
# Pass a shell variable as a jq string
$ TAG=v1.2.3
$ echo '{}' | jq -n --arg tag "$TAG" '{tag: $tag}'
{"tag": "v1.2.3"}

# Pass JSON
$ echo '{}' | jq -n --argjson data '{"a":1}' '$data.a'
1

# Define an internal variable with `as`
$ echo '{"multiplier": 3}' | jq '.multiplier as $m | [1,2,3] | map(. * $m)'
[3, 6, 9]
```

---

## yq

!!! warning "Two distinct `yq` packages"
    There are **two unrelated** `yq` tools — make sure you know which one you have:

    - [**kislyuk/yq**](https://github.com/kislyuk/yq){target=_blank} — Python wrapper around `jq`. Uses **jq syntax**. Pass `-y` to output YAML.
    - [**mikefarah/yq**](https://github.com/mikefarah/yq){target=_blank} — Standalone Go tool. Uses its **own syntax** (similar to jq but different).

    The examples below cover both. Check yours with `yq --version`.

### kislyuk/yq (jq wrapper)

kislyuk/yq reads YAML as input and runs a jq filter. Use `-y` to write YAML output instead of JSON.

```shell
# Read a field from a YAML file
$ yq '.image.tag' values.yaml
"1.0.0"

# Raw string output
$ yq -r '.image.tag' values.yaml
1.0.0

# Output YAML (not JSON)
$ yq -y '.image' values.yaml
repository: prom/prom-kpi
tag: 1.0.0

# Convert YAML → JSON
$ yq . file.yaml

# Convert JSON → YAML
$ cat file.json | yq -y .

# Flatten a nested YAML to dot-notation keys
$ alias flatten_yaml='yq -y '\''[tostream | select(has(1)) | first |= join(".") | {key: first, value: last}] | from_entries'\'''
$ flatten_yaml values.yaml
image.repository: prom/prom-kpi
image.pullPolicy: IfNotPresent
image.tag: ''
imagePullSecrets: []
replicaCount: 1
```

### mikefarah/yq

mikefarah/yq uses a path expression syntax inspired by jq but with differences (e.g. `|` behaves differently, use `.*` to iterate maps).

```shell
# Read a field
$ yq '.image.tag' values.yaml
1.0.0

# Update a field (in-place with -i)
$ yq -i '.image.tag = "2.0.0"' values.yaml

# Delete a key
$ yq -i 'del(.image.pullPolicy)' values.yaml

# Iterate over a sequence
$ yq '.users[]' file.yaml

# Convert YAML → JSON
$ yq -o=json . file.yaml

# Convert JSON → YAML
$ yq -P . file.json

# Merge two YAML files (second overrides first)
$ yq '. *= load("overrides.yaml")' base.yaml

# Select elements from a sequence
$ yq '.users[] | select(.role == "admin")' file.yaml
```
