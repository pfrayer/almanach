# `whois`

## Get all IP ranges for a given ASN

```shell
$ whois -h whois.radb.net -- '-i origin AS16276' | grep "^route"
route:          2.57.18.0/24
route:          2.57.18.0/24
route:          2.57.242.0/24
route:          5.39.0.0/17
route:          5.83.153.0/24
...
```

[Source](https://man.ilayk.com/man/whois/)
