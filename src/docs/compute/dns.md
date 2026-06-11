---
description: "DNS lookup cheatsheet: dig, nslookup and whois for records, delegation, reverse DNS and ASN IP ranges."
---

# DNS

## `dig`

```shell
# Basic lookup (A record)
dig example.com
dig example.com A

# Short output
dig +short example.com
dig +short example.com MX
dig +short example.com TXT
dig +short example.com NS
dig +short example.com CNAME

# IPv4 + IPv6 in one shot
dig pateenchroot.ovh A pateenchroot.ovh AAAA +short

# Readable single-line answer
dig +noall +answer example.com

# Use a specific resolver
dig @1.1.1.1 example.com +short      # Cloudflare
dig @8.8.8.8 example.com +short      # Google

# Trace full delegation from root
dig +trace example.com

# Reverse DNS (PTR)
dig -x 54.36.98.105 +short

# Check SOA (zone serial, TTLs)
dig example.com SOA +short
```

```shell
# dig not found
apt install dnsutils
```

---

## `nslookup`

```shell
nslookup example.com
nslookup -type=A example.com
nslookup -type=MX example.com
nslookup -type=TXT example.com

# Query a specific server
nslookup example.com 1.1.1.1
```

---

## `whois`

```shell
# Domain lookup — registrar, expiry, nameservers
whois example.com
whois pateenchroot.ovh

# IP lookup — ASN, org, country
whois 54.36.98.105

# All IP ranges for a given ASN
whois -h whois.radb.net -- '-i origin AS16276' | grep "^route"
# route: 2.57.18.0/24
# route: 5.39.0.0/17
# ...
```
