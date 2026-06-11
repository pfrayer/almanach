# Logs

## journalctl

→ See [systemd — journalctl](systemd.md#journalctl----logs)

---

## tail & follow

```shell
tail -f /var/log/syslog
tail -f /var/log/syslog -n 200                 # start with last 200 lines
tail -f file1.log file2.log                    # follow multiple files

# multitail — follow multiple files in split panes
apt install multitail
multitail file1.log file2.log
multitail -s 2 file1.log file2.log             # side by side
```

---

## grep / awk on logs

```shell
# Search for a pattern
grep "ERROR" app.log
grep -i "error" app.log                        # case-insensitive
grep -v "DEBUG" app.log                        # exclude lines
grep -A3 -B3 "Exception" app.log               # 3 lines of context

# Count occurrences per pattern
grep -c "ERROR" app.log

# Extract and count unique IPs (e.g. Apache logs)
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head 20

# Count HTTP status codes
awk '{print $9}' access.log | sort | uniq -c | sort -rn

# Show lines between two timestamps
awk '/2024-01-01 10:00/,/2024-01-01 11:00/' app.log

# Sum a numeric field (e.g. response time in column 10)
awk '{sum += $10} END {print sum/NR " avg"}' access.log
```

---

## JSON logs with jq

```shell
# Pretty-print JSON logs
cat app.log | jq .

# Filter by log level
cat app.log | jq 'select(.level == "error")'

# Filter and extract fields
cat app.log | jq 'select(.level == "error") | {time, message}'

# Follow and parse live JSON logs
tail -f app.log | jq --unbuffered 'select(.level == "error")'

# Count errors by type
cat app.log | jq -r 'select(.level == "error") | .error_type' \
    | sort | uniq -c | sort -rn
```

---

## tailspin

[tailspin](https://github.com/bensadeh/tailspin){target=_blank} is a log highlighter that colorizes any log file with zero config — highlights dates, IPs, URLs, UUIDs, HTTP methods, log levels, numbers.

```shell
# Install
cargo install tailspin
# or
brew install tailspin

# Highlight a file
tspin app.log

# Follow a file
tspin -f app.log

# Pipe from stdin
tail -f app.log | tspin
journalctl -f | tspin
kubectl logs -f <pod> | tspin
```

---

## lnav

[lnav](https://lnav.org){target=_blank} is a terminal log viewer with automatic format detection, filtering, SQL queries, and timeline navigation.

```shell
apt install lnav

lnav app.log
lnav /var/log/                                 # directory of log files
lnav app.log access.log                        # multiple files, merged timeline

# Inside lnav:
# / — search
# ; — SQL query (e.g. SELECT count(*) FROM logs WHERE log_level = 'error')
# :filter-in <pattern>
# :filter-out <pattern>
# :hide-lines-before 1h ago
# i — toggle histogram view
# ? — help
```

---

## logrotate

Config example — `/etc/logrotate.d/myapp`:

```
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 www-data adm
    sharedscripts
    postrotate
        systemctl reload myapp
    endscript
}
```

```shell
logrotate -d /etc/logrotate.d/myapp            # dry run
logrotate -f /etc/logrotate.d/myapp            # force rotate now
```

---

## Docker logs

```shell
docker logs <container>
docker logs <container> -f
docker logs <container> --tail 100
docker logs <container> --since 1h

docker compose logs -f
docker compose logs -f <service>

# JSON log driver — logs stored as JSON on the host
# /var/lib/docker/containers/<id>/<id>-json.log
cat /var/lib/docker/containers/<id>/<id>-json.log | jq '.log'
```

---

## Generate fake logs

```shell
# 1 MB of fake logs
docker run -it --rm mingrammer/flog -b 1048576 > 1_mega.log

# Continuous Apache logs, one per 2s
docker run -it --rm mingrammer/flog -f apache_combined -t stdout -n 2 -l
```

Supports multiple formats (`apache_combined`, `apache_error`, `rfc3164`, `rfc5424`, `json`). See the [README](https://github.com/mingrammer/flog/blob/master/README.md){target=_blank}.
