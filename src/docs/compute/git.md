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
```
```
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
