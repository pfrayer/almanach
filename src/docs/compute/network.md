# Network

## Public IP

```shell
curl ifconfig.me                       # plain IP
curl ip.pateenchroot.ovh               # same, self-hosted
curl ipinfo.io                         # JSON: IP, city, org, ASN
curl ipinfo.io/54.36.98.105            # info for a specific IP
curl ipinfo.io/54.36.98.105/org        # just the org/ASN
```

---

## nmap

```shell
# Ping scan — which hosts are up
nmap -sn 192.168.1.0/24

# Port scan (top 1000 ports)
nmap 192.168.1.1

# Scan specific ports
nmap -p 22,80,443 192.168.1.1
nmap -p 1-65535 192.168.1.1           # all ports

# Service + version detection
nmap -sV 192.168.1.1

# OS detection (requires root)
sudo nmap -O 192.168.1.1

# Aggressive scan (OS + version + scripts + traceroute)
sudo nmap -A 192.168.1.1

# Scan without DNS resolution (faster)
nmap -n 192.168.1.0/24

# UDP scan
sudo nmap -sU -p 53,123,161 192.168.1.1
```

---

## Open ports & sockets

```shell
# Listening ports (ss — modern replacement for netstat)
ss -tlnp                               # TCP listening, with process
ss -ulnp                               # UDP listening
ss -tlnp sport = :80                   # filter by port

# Established connections
ss -tnp

# All sockets summary
ss -s

# netstat (legacy, may need apt install net-tools)
netstat -tlnp                          # TCP listening
netstat -an | grep ESTABLISHED
```

---

## ping & traceroute

```shell
ping example.com
ping -c 4 example.com                  # send 4 packets
ping -i 0.2 example.com                # interval 0.2s (flood-like)

traceroute example.com
traceroute -n example.com              # no DNS resolution (faster)

# mtr — live traceroute (combines ping + traceroute)
mtr example.com
mtr --report example.com              # non-interactive report
```

---

## curl tips

```shell
# Follow redirects, show final URL
curl -Ls -o /dev/null -w "%{url_effective}\n" http://example.com

# Show response headers only
curl -I https://example.com

# Show headers + body
curl -i https://example.com

# Time a request
curl -o /dev/null -s -w "dns:%{time_namelookup}s  connect:%{time_connect}s  total:%{time_total}s\n" https://example.com

# POST JSON
curl -X POST https://api.example.com/endpoint \
    -H "Content-Type: application/json" \
    -d '{"key": "value"}'

# With auth
curl -u user:pass https://example.com
curl -H "Authorization: Bearer <token>" https://api.example.com
```
