# curl

## Basics

```shell
curl https://example.com                       # GET, print body
curl -o file.html https://example.com          # save to file
curl -O https://example.com/file.tar.gz        # save with remote filename
curl -L https://example.com                    # follow redirects
curl -s https://example.com                    # silent (no progress bar)
curl -f https://example.com                    # fail on HTTP error (exit 22)
curl -sf https://example.com                   # silent + fail (common in scripts)
```

---

## Headers & inspection

```shell
# Show response headers only
curl -I https://example.com

# Show headers + body
curl -i https://example.com

# Show verbose output (full request + response headers)
curl -v https://example.com

# Show only the HTTP status code
curl -o /dev/null -s -w "%{http_code}\n" https://example.com

# Time a request
curl -o /dev/null -s -w \
  "dns:%{time_namelookup}s  connect:%{time_connect}s  ttfb:%{time_starttransfer}s  total:%{time_total}s\n" \
  https://example.com

# Show final URL after redirects
curl -Ls -o /dev/null -w "%{url_effective}\n" http://example.com
```

---

## Request methods & body

```shell
# POST with form data
curl -X POST -d "name=alice&age=30" https://api.example.com/users

# POST JSON
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "alice", "age": 30}'

# POST JSON from file
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d @payload.json

# PUT
curl -X PUT https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "alice"}'

# DELETE
curl -X DELETE https://api.example.com/users/1

# PATCH
curl -X PATCH https://api.example.com/users/1 \
  -H "Content-Type: application/json" \
  -d '{"age": 31}'
```

---

## Authentication

```shell
# Basic auth
curl -u user:password https://example.com
curl -u user https://example.com               # prompts for password

# Bearer token
curl -H "Authorization: Bearer <token>" https://api.example.com

# API key header
curl -H "X-API-Key: abc123" https://api.example.com

# Client certificate
curl --cert cert.pem --key key.pem https://example.com
```

---

## Headers & cookies

```shell
# Custom request header
curl -H "Accept: application/json" https://api.example.com
curl -H "X-Custom: value" -H "Another: header" https://example.com

# Send cookies
curl -b "session=abc123" https://example.com
curl -b cookies.txt https://example.com        # from file

# Save + send cookies (login flows)
curl -c cookies.txt -b cookies.txt https://example.com/login \
  -d "user=alice&pass=secret"
```

---

## TLS

```shell
# Skip certificate verification (dev only)
curl -k https://self-signed.example.com

# Specify CA bundle
curl --cacert ca.pem https://example.com

# Use a specific TLS version
curl --tls-max 1.2 https://example.com
curl --tlsv1.3 https://example.com
```

---

## File upload

```shell
# Upload a file (multipart form)
curl -F "file=@/path/to/file.txt" https://example.com/upload

# Upload with custom field name and mime type
curl -F "data=@report.pdf;type=application/pdf" https://example.com/upload

# Upload binary (PUT)
curl -T file.bin https://example.com/upload
```

---

## Useful patterns

```shell
# Download and pipe to tar
curl -sL https://example.com/archive.tar.gz | tar xz

# Check public IP
curl ifconfig.me
curl ip.pateenchroot.ovh
curl ipinfo.io

# Retry on failure
curl --retry 3 --retry-delay 2 https://example.com

# Set timeout
curl --connect-timeout 5 --max-time 30 https://example.com

# Use a proxy
curl -x http://proxy:8080 https://example.com
```
