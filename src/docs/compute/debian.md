---
description: "Debian cheatsheet: apt and dpkg, repositories and keys, package pinning, holding versions and system info."
---

# Debian

## apt

### Install & remove

```shell
apt install <package>
apt install <package>=<version>    # pin to a specific version
apt install --no-install-recommends <package>

apt remove <package>               # remove but keep config files
apt purge <package>                # remove + config files
apt autoremove                     # remove unused dependencies
```

### Update & upgrade

```shell
apt update                         # refresh package index
apt upgrade                        # upgrade installed packages (no removals)
apt full-upgrade                   # upgrade + allow removals (dist-upgrade alias)
```

### Search & inspect

```shell
apt search <keyword>               # search package names/descriptions
apt show <package>                 # full package metadata
apt list --installed               # all installed packages
apt list --installed | grep <name> # filter installed
apt list --upgradable              # packages with available upgrades
```

### Package cache

```shell
apt-cache showpkg <package>        # show package versions and deps
apt-cache depends <package>        # direct dependencies
apt-cache rdepends <package>       # reverse dependencies (who depends on it)
apt-cache policy <package>         # installed vs candidate version, pinning
```

---

## dpkg

```shell
# Install a local .deb
dpkg -i package.deb

# List all installed packages
dpkg -l
dpkg -l | grep <name>

# List files installed by a package
dpkg -L <package>

# Which package owns a file
dpkg -S /usr/bin/cwebp
# webp: /usr/bin/cwebp

# Package status / info
dpkg -s <package>

# Reconfigure an installed package
dpkg-reconfigure <package>
```

---

## Repositories

```shell
# Sources list
/etc/apt/sources.list
/etc/apt/sources.list.d/*.list      # drop-in files (preferred)

# Format (old style)
deb http://deb.debian.org/debian bookworm main contrib non-free non-free-firmware
deb-src http://deb.debian.org/debian bookworm main

# Add a repo key (modern way)
curl -fsSL https://example.com/repo.gpg | gpg --dearmor \
    -o /usr/share/keyrings/example.gpg

# Reference the key in sources.list.d
echo "deb [signed-by=/usr/share/keyrings/example.gpg] \
    https://example.com/debian stable main" \
    > /etc/apt/sources.list.d/example.list

apt update
```

---

## Package pinning

Prioritize or hold back packages via `/etc/apt/preferences.d/`.

```
# /etc/apt/preferences.d/hold-nginx
Package: nginx
Pin: version 1.22.*
Pin-Priority: 1001
```

```shell
# Hold a package at current version (simpler)
apt-mark hold <package>
apt-mark unhold <package>
apt-mark showhold               # list held packages
```

---

## System info

```shell
# Debian version
cat /etc/debian_version           # e.g. 12.5
lsb_release -a

# Which codename maps to what
# bookworm = Debian 12  |  bullseye = 11  |  buster = 10

# Kernel
uname -r
```

---

## Useful packages

| Package | Provides |
|---------|----------|
| `procps` | `ps`, `top`, `free`, `vmstat` |
| `net-tools` | `netstat`, `ifconfig` |
| `iproute2` | `ip`, `ss` |
| `dnsutils` | `dig`, `nslookup` |
| `curl` / `wget` | HTTP clients |
| `build-essential` | `gcc`, `make`, `g++` |
| `lsof` | list open files/sockets |
| `strace` | trace system calls |
| `htop` | interactive process viewer |
| `jq` | JSON processor |
