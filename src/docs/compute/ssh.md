---
description: "SSH cheatsheet: keys, the ~/.ssh/config file, jump hosts, port forwarding, SOCKS tunnels and ssh-agent."
---

# SSH

## Keys

```shell
# Generate a key pair (Ed25519 recommended)
ssh-keygen -t ed25519 -C "john@example.com"
ssh-keygen -t ed25519 -C "work key" -f ~/.ssh/id_work

# Generate a key pair (RSA fallback for legacy systems)
ssh-keygen -t rsa -b 4096 -C "john@example.com"

# Recover public key from private key
ssh-keygen -f ~/.ssh/id_ed25519 -y > ~/.ssh/id_ed25519.pub

# Show fingerprint of a key
ssh-keygen -lf ~/.ssh/id_ed25519.pub
ssh-keygen -lf ~/.ssh/id_ed25519.pub -E md5   # MD5 format (for older systems)

# Copy public key to remote host
ssh-copy-id user@host
ssh-copy-id -i ~/.ssh/id_work.pub user@host
```

---

## Connect

```shell
ssh user@host
ssh user@host -p 2222                   # custom port
ssh user@host -i ~/.ssh/id_work         # specific key
ssh user@host -v                        # verbose (debug level 1)
ssh user@host -vvv                      # very verbose (debug level 3)

# Run a remote command
ssh user@host "df -h"
ssh user@host "sudo systemctl restart nginx"

# Force password auth (bypass key)
ssh -o PreferredAuthentications=password user@host
```

---

## ~/.ssh/config

Avoid typing options every time — define aliases:

```
Host myserver
    HostName 192.168.1.10
    User ubuntu
    Port 2222
    IdentityFile ~/.ssh/id_work

Host bastion
    HostName bastion.example.com
    User ec2-user
    IdentityFile ~/.ssh/id_ed25519

# Jump through bastion to reach internal host
Host internal
    HostName 10.0.0.5
    User ubuntu
    ProxyJump bastion

# Shared options for all hosts
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
    AddKeysToAgent yes
```

```shell
ssh myserver                            # uses config above
ssh internal                            # jumps through bastion automatically
```

---

## Jump hosts & tunnels

```shell
# Jump through a bastion (one-liner)
ssh -J bastion.example.com user@10.0.0.5

# Local port forward — access remote service locally
# http://localhost:8080 → remote:80
ssh -L 8080:localhost:80 user@host

# Access a host behind a bastion
ssh -L 5432:db.internal:5432 user@bastion

# Remote port forward — expose local port on remote
ssh -R 9090:localhost:3000 user@host

# Dynamic SOCKS proxy
ssh -D 1080 user@host
# then: curl --socks5 localhost:1080 http://example.com

# Keep tunnels alive in background
ssh -fNL 8080:localhost:80 user@host
# -f: background  -N: no command  -L: local forward
```

---

## ssh-agent

```shell
# Start agent
eval "$(ssh-agent -s)"

# Add a key (prompted for passphrase once)
ssh-add ~/.ssh/id_ed25519
ssh-add ~/.ssh/id_work

# Add with TTL (forget after 8 hours)
ssh-add -t 8h ~/.ssh/id_ed25519

# List loaded keys
ssh-add -l

# Remove all keys
ssh-add -D
```

---

## scp & rsync

```shell
# Copy file to remote
scp file.txt user@host:/remote/path/

# Copy from remote
scp user@host:/remote/file.txt ./local/

# Copy directory
scp -r ./dir user@host:/remote/

# rsync (preferred — faster, resumable)
rsync -avz ./dir user@host:/remote/
rsync -avz --progress --delete ./dir user@host:/remote/
rsync -avz -e "ssh -p 2222 -i ~/.ssh/id_work" ./dir user@host:/remote/
```

---

## Server side (sshd)

```shell
# Config file
/etc/ssh/sshd_config

# Key options to harden
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers ubuntu deploy

# Reload config without dropping connections
systemctl reload sshd

# Check config syntax
sshd -t

# Show active connections
ss -tnp | grep :22
who
```

---

## Debug & troubleshoot

```shell
# Client-side verbose output (most useful first step)
ssh -v user@host      # level 1 — shows which keys are tried, auth methods
ssh -vvv user@host    # level 3 — full protocol trace

# Test connection without logging in
ssh -o BatchMode=yes -o ConnectTimeout=5 user@host echo ok

# Check server host key
ssh-keyscan -H host >> ~/.ssh/known_hosts   # add host key without prompt

# Remove a stale known_hosts entry (host key changed)
ssh-keygen -R host
ssh-keygen -R [host]:2222                   # custom port

# Permission issues — SSH is strict about file permissions
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
chmod 600 ~/.ssh/authorized_keys
chmod 600 ~/.ssh/config

# Server-side: check auth log
journalctl -u ssh -f
tail -f /var/log/auth.log
```

!!! tip "Common reasons a key is refused"
    - Wrong permissions on `~/.ssh/` or `authorized_keys` (must not be group/world writable)
    - `authorized_keys` contains the **public** key but it doesn't match the private key used
    - `PasswordAuthentication no` + no valid key → use `-v` to see which key is tried
    - `AllowUsers` on the server doesn't include your user
