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

## Note about `yq` and `yq`

There are **two distincts** `yq` packages:

- https://github.com/mikefarah/yq
- https://github.com/kislyuk/yq
