---
description: "systemd cheatsheet: systemctl service management, journalctl logs, unit files, timers and troubleshooting."
---

# systemd

## systemctl — service management

```shell
systemctl start <service>
systemctl stop <service>
systemctl restart <service>
systemctl reload <service>          # reload config without stopping (if supported)
systemctl reload-or-restart <service>

systemctl status <service>
systemctl is-active <service>       # exits 0 if running
systemctl is-enabled <service>      # exits 0 if enabled at boot

systemctl enable <service>          # enable at boot
systemctl disable <service>
systemctl enable --now <service>    # enable + start immediately
systemctl disable --now <service>   # disable + stop immediately

systemctl mask <service>            # prevent starting entirely
systemctl unmask <service>
```

---

## Inspect services

```shell
systemctl list-units                        # all active units
systemctl list-units --type=service         # services only
systemctl list-units --state=failed         # failed units
systemctl list-unit-files --type=service    # all installed services + state

systemctl cat <service>                     # show unit file
systemctl show <service>                    # all properties (machine-readable)
systemctl show -p Restart,ExecStart <service>

# Dependencies
systemctl list-dependencies <service>
systemctl list-dependencies --reverse <service>   # who depends on it
```

---

## journalctl — logs

```shell
journalctl -u <service>                    # logs for a service
journalctl -u <service> -f                 # follow
journalctl -u <service> -n 50             # last 50 lines
journalctl -u <service> --since "1h ago"
journalctl -u <service> --since "2024-01-01" --until "2024-01-02"

journalctl -b                              # current boot
journalctl -b -1                           # previous boot
journalctl --list-boots

journalctl -p err                          # errors and above
journalctl -p err -u nginx

journalctl --disk-usage
journalctl --vacuum-time=7d               # keep only last 7 days
journalctl --vacuum-size=500M
```

---

## Unit files

Unit files live in:

- `/lib/systemd/system/` — installed by packages (don't edit)
- `/etc/systemd/system/` — local overrides and custom units ✅

### Service unit example

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My Application
After=network.target

[Service]
Type=simple
User=myapp
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/bin/server --port 8080
Restart=on-failure
RestartSec=5s
Environment=NODE_ENV=production
EnvironmentFile=/etc/myapp/env

[Install]
WantedBy=multi-user.target
```

```shell
# After creating or editing a unit file
systemctl daemon-reload
systemctl enable --now myapp
```

### Drop-in override (preferred over editing the original)

```shell
systemctl edit <service>          # opens editor, creates drop-in automatically
# or manually:
mkdir -p /etc/systemd/system/<service>.d/
vim /etc/systemd/system/<service>.d/override.conf
```

```ini
# override.conf — only put what you want to change
[Service]
Environment=LOG_LEVEL=debug
Restart=always
```

---

## Timers (cron replacement)

```ini
# /etc/systemd/system/cleanup.timer
[Unit]
Description=Run cleanup daily

[Timer]
OnCalendar=daily
Persistent=true                   # run missed jobs after reboot

[Install]
WantedBy=timers.target
```

```ini
# /etc/systemd/system/cleanup.service
[Unit]
Description=Cleanup old files

[Service]
Type=oneshot
ExecStart=/usr/local/bin/cleanup.sh
```

```shell
systemctl enable --now cleanup.timer
systemctl list-timers                     # all timers + next run time
```

OnCalendar syntax: `hourly`, `daily`, `weekly`, `monthly`, `*-*-* 02:00:00`

---

## System state

```shell
systemctl poweroff
systemctl reboot
systemctl suspend
systemctl hibernate

# Targets (runlevels)
systemctl get-default                      # current default target
systemctl set-default multi-user.target    # no GUI on next boot
systemctl isolate rescue.target            # switch to rescue mode now
```

---

## Troubleshoot failed services

```shell
# Overview of what failed
systemctl --failed

# Why did it fail?
systemctl status <service>
journalctl -u <service> -n 50 --no-pager

# Common fix: unit file edited → reload daemon
systemctl daemon-reload && systemctl restart <service>
```
