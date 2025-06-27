# `jq` / `yq`

## Base actions

```shell
$ echo '{"foo": "bar"}' | jq .
{
  "foo": "bar"
}
```

```shell
$ echo '{"foo": "bar"}' | jq '.foo'
"bar"
```

```shell
$ echo '{"foo": "bar"}' | jq -r '.foo'
bar
```

```shell
echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq .
[
  {
    "foo": "bar"
  },
  {
    "foo": 2
  },
  {
    "foo": "kowabunga"
  }
]
```

```shell
$ echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq '.[]'
{
  "foo": "bar"
}
{
  "foo": 2
}
{
  "foo": "kowabunga"
}
```

```shell
$ echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq '.[0]'
{
  "foo": "bar"
}
```

```shell
$ echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq '.[2]'
{
  "foo": "kowabunga"
}
```

```shell
$ echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq '.[2].foo'
"kowabunga
```

## Select

Find in array:

Find based on key ("in this array, print the ID of the user "bob"):

```shell
$ echo '[ {"id": 1, "name": "alice"}, {"id": 2, "name": "bob"} ]' | jq '.[] | select(.name == "bob") | .id'
2
```

Find based on key in array ("in this array, print the ID of all dict having `alice` in its users"):

```shell
$ echo '[ {"id": 1, "users": ["alice", "bob"]}, {"id": 2, "users": ["alice"]}, {"id": 3, "users": ["bob"]} ]' | jq '.[] | select(.users[] | contains("alice")) | .id'
1
2
```

## Append

Add key to dict:

```shell
$ echo '{"foo": "kowabunga"}' | jq '. + {"bar": "new item"}'
{
  "foo": "kowabunga",
  "bar": "new item"
}
```

It can override existing keys:

```shell
echo '{"foo": "kowabunga"}' | jq '. + {"foo": "new item"}'
{
  "foo": "new item"
}
```

Add item to array:

```shell
echo '[{"foo": "bar"}, {"foo": 2}, {"foo": "kowabunga"}]' | jq '. + [{"foo": "new item"}]'
[
  {
    "foo": "bar"
  },
  {
    "foo": 2
  },
  {
    "foo": "kowabunga"
  },
  {
    "foo": "new item"
  }
]
```

## Useful aliases

Flatten YAML:

```shell
$ alias flatten_yaml='yq -y '\''[tostream | select(has(1)) | first |= join(".") | {key: first, value: last}]| from_entries'\'

$ cat file.yaml
image:
  repository: prom/prom-kpi
  pullPolicy: IfNotPresent
  tag: ""
imagePullSecrets: []
replicaCount: 1
...

$ flatten_yaml file.yaml
image.repository: prom/prom-kpi
image.pullPolicy: IfNotPresent
image.tag: ''
imagePullSecrets: []
replicaCount: 1
...
```

## Note about `yq` and `yq`

There are **two distincts** `yq` packages:

- [https://github.com/mikefarah/yq](https://github.com/mikefarah/yq){target=_blank}
- [https://github.com/kislyuk/yq](https://github.com/kislyuk/yq){target=_blank}
