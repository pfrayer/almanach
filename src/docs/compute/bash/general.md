---
description: "Bash scripting cheatsheet: strict mode, variable substitution, test operators, loops, trap cleanup and heredocs."
---

# Bash

## Strict mode

Start scripts with this to catch errors early:
```bash
#!/usr/bin/env bash
set -euo pipefail
```

| Flag | Effect |
|------|--------|
| `-e` | Exit on error |
| `-u` | Error on undefined variable |
| `-o pipefail` | Fail if any command in a pipe fails |

## Variable substitution

```bash
${var:-default}    # Use default if var is unset/empty
${var:=default}    # Assign default if var is unset/empty
${var:?error msg}  # Exit with error if var is unset/empty
${#var}            # Length of var
${var%suffix}      # Remove shortest suffix match
${var%%suffix}     # Remove longest suffix match
${var#prefix}      # Remove shortest prefix match
${var##prefix}     # Remove longest prefix match
${var/old/new}     # Replace first match
${var//old/new}    # Replace all matches
```

## Test operators

### Files

```bash
[ -f file ]   # File exists and is regular
[ -d dir ]    # Directory exists
[ -s file ]   # File exists and is not empty
[ -r file ]   # File is readable
[ -w file ]   # File is writable
[ -x file ]   # File is executable
[ -L file ]   # File is a symlink
```

### Strings & numbers

```bash
[ -z "$str" ]       # String is empty
[ -n "$str" ]       # String is not empty
[ "$a" = "$b" ]     # Strings are equal
[[ "$a" =~ regex ]] # Regex match (bash only)
[ "$a" -eq "$b" ]   # Integers equal (-ne, -lt, -gt, -le, -ge)
```

## Loops

```bash
# Iterate over files
for f in /var/log/*.log; do
    echo "Processing $f"
done

# Read file line by line
while IFS= read -r line; do
    echo "$line"
done < input.txt

# C-style for loop
for ((i=0; i<10; i++)); do
    echo "$i"
done
```

## Trap & cleanup

```bash
cleanup() {
    rm -f "$tmpfile"
}
trap cleanup EXIT

tmpfile=$(mktemp)
```

## `cat EOF` syntax

```shell
$ cat <<EOF > script.sh
#!/usr/bin/env bash
echo \$PWD
echo $PWD
EOF
```
`script.sh` content will be:
```bash
#!/usr/bin/env bash
echo $PWD
echo /home/user
```

## Replace line breaks with `\n` in bash

```shell
$ sed ':a;N;$!ba;s/\n/\n/g'
```

Example with a GPG key:
```shell
$ cat my-pub-key.gpg
-----BEGIN PGP PUBLIC KEY BLOCK-----

mDMEY0U3WBYJKwYBBAHaRw8BAQdA/+X92euriYPzQiFAnll233epEjIrRg5NjvX9
GI2ubAi0KmF6ZXphZV/Dp3kgYXpldSA8aXV6ZXLDoMOndXplcmFAw6Z6ZXphLmZy
PoiQBBMWCAA4FiEErm9qR639pFyOCR3lkjAjOeRHFXIFAmNFN1gCGwMFCwkIBwIG
FQoJCAsCBBYCAwECHgECF4AACgkQkjAjOeRHFXJVqAD9HBET1rSmvR7T0g+AytMC
bRhA5nuAhUAiZLZBPi7YzegA/2oiUfH+RqNrWmTogAuC4DnOlysRDF4ETM5dpzIm
pKMCuDgEY0U3WBIKKwYBBAGXVQEFAQEHQARwYrThl0KXvNaypSPMRSpI7knavFxH
ouJhP07bEAEuAwEIB4h4BBgWCAAgFiEErm9qR639pFyOCR3lkjAjOeRHFXIFAmNF
N1gCGwwACgkQkjAjOeRHFXI5/gEAq04angadKntUSMpJAVd3L/Wwkt41Xw7lfo/k
WeKoJDwBAPKeat0p8zbLIPDQvmcxsfjJ/GnapH206f+VVO/nZcAP
=4EN5
-----END PGP PUBLIC KEY BLOCK-----

$ gpg --armor --export AE6F6A47ADFDA45C8E091DE592302339E4471572 | sed ':a;N;$!ba;s/\n/\\n/g'
-----BEGIN PGP PUBLIC KEY BLOCK-----\n\nmDMEY0U3WBYJKwYBBAHaRw8BAQdA/+X92euriYPzQiFAnll233epEjIrRg5NjvX9\nGI2ubAi0KmF6ZXphZV/Dp3kgYXpldSA8aXV6ZXLDoMOndXplcmFAw6Z6ZXphLmZy\nPoiQBBMWCAA4FiEErm9qR639pFyOCR3lkjAjOeRHFXIFAmNFN1gCGwMFCwkIBwIG\nFQoJCAsCBBYCAwECHgECF4AACgkQkjAjOeRHFXJVqAD9HBET1rSmvR7T0g+AytMC\nbRhA5nuAhUAiZLZBPi7YzegA/2oiUfH+RqNrWmTogAuC4DnOlysRDF4ETM5dpzIm\npKMCuDgEY0U3WBIKKwYBBAGXVQEFAQEHQARwYrThl0KXvNaypSPMRSpI7knavFxH\nouJhP07bEAEuAwEIB4h4BBgWCAAgFiEErm9qR639pFyOCR3lkjAjOeRHFXIFAmNF\nN1gCGwwACgkQkjAjOeRHFXI5/gEAq04angadKntUSMpJAVd3L/Wwkt41Xw7lfo/k\nWeKoJDwBAPKeat0p8zbLIPDQvmcxsfjJ/GnapH206f+VVO/nZcAP\n=4EN5\n-----END PGP PUBLIC KEY BLOCK-----
```

To do the opposite (replace the `\n` string with a real line breaks):
```shell
$ echo "my\ntext\nis\nhere" | sed 's/\\n/\n/g'
my
text
is
here
```
[Source and details](https://stackoverflow.com/questions/1251999/how-can-i-replace-each-newline-n-with-a-space-using-sed/1252191#1252191){target=_blank}
