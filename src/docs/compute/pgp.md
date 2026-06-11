---
description: "PGP/GPG cheatsheet: generate and manage keys, keyservers, encrypt and decrypt, sign and verify files."
---

# PGP / GPG

> PGP is the protocol, GPG (`gnupg`) is the implementation.

## Keys

### Generate

```shell
gpg --expert --full-generate-key    # interactive, recommended (choose Ed25519)
gpg --gen-key                       # quick mode (RSA 3072, no expiry)
```

### List

```shell
gpg -k                              # public keys
gpg -K                              # secret keys
gpg -k --fingerprint                # show fingerprints
gpg -k --with-colons                # machine-readable output
```

Output anatomy:

```
pub   ed25519 2022-04-06 [SC]
      7D438CA8D0C6D57EA163751C2C800B246796CFC9
uid           [ultimate] John Doe <john@example.org>
sub   cv25519 2022-04-06 [E]
```

`[SC]` = Sign + Certify (primary key) · `[E]` = Encrypt (subkey)

### Export & import

```shell
# Export public key (shareable)
gpg --armor --export john@example.org > john.pub.asc

# Export secret key (keep safe!)
gpg --armor --export-secret-keys john@example.org > john.sec.asc

# Import a key
gpg --import john.pub.asc
gpg --import john.sec.asc           # restores on a new machine

# Refresh from keyserver
gpg --refresh-keys
```

### Trust

```shell
gpg --edit-key <fingerprint>
gpg> trust
# 1=unknown 2=no 3=marginal 4=full 5=ultimate
Your decision? 5
gpg> save
```

### Revocation

```shell
# Generate a revocation certificate immediately after key creation
gpg --gen-revoke john@example.org > revoke.asc

# Apply it later if the key is compromised
gpg --import revoke.asc
gpg --keyserver keys.openpgp.org --send-keys <fingerprint>
```

### Expiry & editing

```shell
gpg --edit-key <fingerprint>
gpg> expire            # change expiry on primary key
gpg> key 1             # select subkey 1
gpg> expire            # change subkey expiry
gpg> passwd            # change passphrase
gpg> save
```

---

## Keyservers

```shell
# Upload your public key
gpg --keyserver keys.openpgp.org --send-keys <fingerprint>

# Search & download
gpg --keyserver keys.openpgp.org --search-keys john@example.org
gpg --keyserver keys.openpgp.org --recv-keys <fingerprint>
```

---

## Encrypt & decrypt

```shell
# Encrypt for a recipient (they can decrypt with their private key)
gpg --encrypt --armor --recipient john@example.org file.txt
# → produces file.txt.asc

# Encrypt for multiple recipients
gpg --encrypt --armor -r alice@example.org -r bob@example.org file.txt

# Symmetric encryption (passphrase only, no keys needed)
gpg --symmetric --armor file.txt

# Decrypt
gpg --decrypt file.txt.asc
gpg --decrypt file.txt.asc > file.txt
```

---

## Sign & verify

```shell
# Detached signature (signature in a separate file)
gpg --detach-sign --armor file.tar.gz
# → produces file.tar.gz.asc

# Verify a detached signature
gpg --verify file.tar.gz.asc file.tar.gz

# Clearsign (signature + plaintext in one file)
gpg --clearsign message.txt
# → produces message.txt.asc

# Sign + encrypt in one step
gpg --sign --encrypt --armor --recipient john@example.org file.txt
```

---

## Git signing

```shell
# Configure Git to use your key
git config --global user.signingkey <fingerprint>
git config --global commit.gpgsign true     # always sign commits
git config --global tag.gpgsign true

# Sign a commit manually
git commit -S -m "message"

# Verify commits
git log --show-signature
```

!!! tip "gpg failed to sign the data"
    ```shell
    export GPG_TTY=$(tty)
    ```
    Add to `~/.bashrc` or `~/.zshrc`. Debug with `GIT_TRACE=1 git commit`.

---

## Inspect a key with hokey

```shell
apt install hopenpgp-tools

gpg --export john@example.org | hokey lint
```

Checks key validity, algorithm strength, subkey bindings, and usage flags.

---

## Backup & restore

```shell
# Full backup (run on source machine)
gpg --armor --export > all-public.asc
gpg --armor --export-secret-keys > all-secret.asc
gpg --export-ownertrust > trust.txt

# Restore (on new machine)
gpg --import all-public.asc
gpg --import all-secret.asc
gpg --import-ownertrust trust.txt
```
