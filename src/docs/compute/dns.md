# DNS

## `nslookup`

Search a given record for a given domain:

```shell
$ nslookup -type=[record type] [domain]
$ nslookup -type=A
Server:     10.15.25.129
Address:    10.15.25.129#53

Non-authoritative answer:
Name:    almanach.pateenchroot.ovh
Address: 54.36.98.105
```

## `dig`

Basics:

```shell
$ dig [ns server] [domain name] [record type]
$ dig almanach.pateenchroot.ovh A

; <<>> DiG 9.20.10 <<>> almanach.pateenchroot.ovh A
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36123
;; flags: qr rd ra ad; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 1232
;; QUESTION SECTION:
;almanach.pateenchroot.ovh.	IN	A

;; ANSWER SECTION:
almanach.pateenchroot.ovh. 3600	IN	A	54.36.98.105

;; Query time: 16 msec
;; SERVER: 213.186.33.99#53(213.186.33.99) (UDP)
;; WHEN: Tue Jun 24 09:45:13 CEST 2025
;; MSG SIZE  rcvd: 70

```

More readable output:

```shell
$ dig +noall +answer almanach.pateenchroot.ovh
almanach.pateenchroot.ovh. 1418	IN	A	54.36.98.105
```

Get IPv4 & IPv6:

```shell
$ dig pateenchroot.ovh A pateenchroot.ovh AAAA +short
54.36.98.105
2001:41d0:302:2200::2723
```

Use a specific DNS server:

```shell
$ dig @1.1.1.1 pateenchroot.ovh +short
54.36.98.105
```

### `dig not found`

```shell
$ apt install dnsutils
```
