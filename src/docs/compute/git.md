# Git

## Sign commits with a given key for a given repo

```shell
$ vim .git/config
# add
[user]
    name = John Doe
    email = john.doe@gmail.com
    signingkey = E9C202EE8524306B1859990FCF3873C85DD3C6E7
```

## Sign old commits

```shell
# Just the last commit
$ git commit -S --amend
# 5 last commits
$ git rebase --signoff HEAD~5
```

## Check git log with signature status

```shell
$ git log --show-signature
commit 389a7fd3390dbe8310085a5444233c6e955f0d89 (HEAD -> master)
gpg: Signature made Thu 16 Jan 2025 05:36:41 PM CET
gpg:                using EDDSA key E9C202EE8524306B1859990FCF3873C85DD3C6E7
gpg: Good signature from "Pierre Frayer <pfrayer@xmail.com>" [ultimate]
Author: Pierre Frayer <pfrayer@xmail.com>
Date:   Thu Jan 16 2025 @ 5:33 PM

    feat: git commit signature

    Signed-off-by: Pierre Frayer <pfrayer@xmail.com>
```

## Fail to sign git commit

When doing `git commit` with GPG signature enabled, you encounter this error:

```shell
$ git commit
error: gpg failed to sign the data
fatal: failed to write commit object
```

Get more details about the error by enabling GIT_TRACE:

```shell
$ GIT_TRACE=1 git commit
...
trace: built-in: git commit --amend --no-edit -n -S
trace: run_command: gpg --status-fd=2 -bsau E9C202EE8524306B1859990FCF3873C85DD3C6E7
```

Most of the time, the solution will be:

```shell
$ export GPG_TTY=$(tty)
$ git commit
```

## Delete local branches that are merged in the remote repo

Save this somewhere (eg. `~/bin/clean-local-branches.sh`):

```bash
#!/usr/bin/env bash

WHITELIST="master|prod"

git fetch --prune
TO_REMOVE=$(git branch --merged | egrep -v "(^\*|${WHITELIST})")

if [ -z "${TO_REMOVE}" ]; then
  echo "No branches to remove."
else
  echo "Branches to remove:"
  echo "${TO_REMOVE}"
  echo ""
  read -n1 -s -r -p $'Press any key to continue...\n' KEY
  if [ "${KEY}" = '' ]; then
    echo "${TO_REMOVE}" | xargs -n 1 git branch -d
  fi
fi
```

Then in your `~/.gitconfig`:

```bash
[alias]
    autoremove = "!bash ~/bin/clean-local-branches.sh"
```

Use it:

```shell
$ git autoremove
Branches to remove:
  dev/me/dockerfile_build_and_slim
  dev/me/troitreze

Press any key to continue...
Deleted branch dev/me/dockerfile_build_and_slim (was a795e10).
Deleted branch dev/me/troitreze (was 03341ac).
```
