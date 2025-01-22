# PGP / GPG

(reminder: PGP is the protocol, GPG is the tool using this protocol)

## Generate a key-pair

```shell
$ gpg --expert --full-generate-key
```

## List keys

```shell
# Public keys
$ gpg -k
# Private keys
$ gpg -K
```

## Trust a key

```shell
$ gpg --edit-key 7D438CA8D0C6D57EA163751C2C800B246796CFC9
gpg> trust
Please decide how far you trust this user to correctly verify other users' keys
(by looking at passports, checking fingerprints from different sources, etc.)

  1 = I don't know or won't say
  2 = I do NOT trust
  3 = I trust marginally
  4 = I trust fully
  5 = I trust ultimately
  m = back to the main menu

Your decision? 5

gpg> save
```

## Fail to sign git commit

When trying to `git commit` with GPG signature, you could encounter the following error:
```
error: gpg failed to sign the data
fatal: failed to write commit object
```
Get more details about the error by enabling `GIT_TRACE`:
```shell
$ GIT_TRACE=1 git commit
...
trace: built-in: git commit --amend --no-edit -n -S
trace: run_command: gpg --status-fd=2 -bsau E9C202EE8524306B1859990FCF3873C85DD3C6E7
...
```
If you have this output, most of the time the solution will be:
```shell
$ export GPG_TTY=$(tty)
$ git commit
```

## Inspect a PGP key with hokey

```shell
# Install hokey (https://hackage.haskell.org/package/hopenpgp-tools)
$ sudo apt install hopenpgp-tools

# Get the available PGP keys on your machine. Retrieve the fingerprint or the user ID:
$ gpg --list-key
--------------------------------
pub   ed25519 2022-04-06 [SC]
      7D438CA8D0C6D57EA163751C2C800B246796CFC9
uid           [ultimate] John Doe <john.doe@example.org>
sub   cv25519 2022-04-06 [E]

# Now, simply export the key and pipe it to hokey lint:
gpg --export 7D438CA8D0C6D57EA163751C2C800B246796CFC9 | hokey lint
# Or
gpg --export "John Doe" | hokey lint

# Output:
hokey (hopenpgp-tools) 0.22
Copyright (C) 2012-2019  Clint Adams
hokey comes with ABSOLUTELY NO WARRANTY. This is free software, and you are welcome to redistribute it under certain conditions.

Key has potential validity: good
Key has fingerprint: 7D43 8CA8 D0C6 D57E A163  751C 2C80 0B24 6796 CFC9
Checking to see if key is OpenPGPv4: V4
Checking to see if key is RSA or DSA (>= 2048-bit): EdDSA 256
Checking user-ID- and user-attribute-related items:
  Jogn Doe <john.doe@example.org>:
    Self-sig hash algorithms: [SHA-256]
    Preferred hash algorithms: [SHA-512, SHA-384, SHA-256, SHA-224, SHA-1]
    Key expiration times: []
    Key usage flags: [[sign-data, certify-keys]]
Checking subkeys:
  one of the subkeys is encryption-capable: True
  fpr: 43C3 C78E 95BA 7170 4B4B  2342 F324 1786 F03A DAF0
    version: v4
    timestamp: 20220406-140557
    algo/size: ECDH 256
    binding sig hash algorithms: [SHA-256]
    usage flags: [[encrypt-storage, encrypt-communications]]
    embedded cross-cert: False
    cross-cert hash algorithms: [SHA-256]
```
