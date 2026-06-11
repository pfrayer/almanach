# Git

## Configuration

```shell
git config --global user.name "John Doe"
git config --global user.email "john@example.com"
git config --global core.editor vim
git config --global init.defaultBranch main
git config --global pull.rebase true          # rebase on pull by default

git config --list                             # show all config
git config --list --show-origin               # show config + file source
```

Per-repo override — edit `.git/config`:

```ini
[user]
    name = John Doe
    email = work@example.com
    signingkey = E9C202EE8524306B1859990FCF3873C85DD3C6E7
```

---

## Repository

```shell
git init
git clone <url>
git clone <url> <dir>
git clone --depth 1 <url>                     # shallow clone (last commit only)
git clone --branch <branch> <url>
```

---

## Staging & committing

```shell
git status
git status -s                                 # short format

git add <file>
git add .                                     # stage all changes
git add -p                                    # interactive hunk staging

git diff                                      # unstaged changes
git diff --staged                             # staged vs last commit

git commit -m "message"
git commit -am "message"                      # stage tracked files + commit
git commit --amend                            # edit last commit (message or content)
git commit --amend --no-edit                  # amend without changing message
```

---

## Branches

```shell
git branch                                    # list local branches
git branch -a                                 # list all (local + remote)
git branch <name>                             # create branch
git branch -d <name>                          # delete (safe)
git branch -D <name>                          # force delete
git branch -m <old> <new>                     # rename

git switch <branch>                           # switch branch
git switch -c <name>                          # create + switch
git checkout -b <name> origin/<branch>        # track remote branch
```

---

## Remote

```shell
git remote -v
git remote add origin <url>
git remote set-url origin <url>
git remote remove <name>

git fetch                                     # fetch all remotes
git fetch origin
git fetch --prune                             # fetch + delete stale remote refs

git pull                                      # fetch + merge/rebase
git pull --rebase                             # fetch + rebase

git push origin <branch>
git push -u origin <branch>                   # set upstream + push
git push --force-with-lease                   # safe force push
git push origin --delete <branch>             # delete remote branch
git push --tags                               # push all tags
```

---

## Log & history

```shell
git log
git log --oneline
git log --oneline --graph --all               # visual branch graph
git log --oneline -10                         # last 10 commits
git log --author="John"
git log --since="2 weeks ago"
git log -- <file>                             # history of a file
git log -p <file>                             # history with diffs

git show <commit>
git show HEAD~2                               # 2 commits before HEAD

git blame <file>
git blame -L 10,20 <file>                     # blame specific lines
```

---

## Undo

```shell
# Unstage a file (keep changes)
git restore --staged <file>

# Discard working directory changes
git restore <file>

# Undo last commit, keep changes staged
git reset --soft HEAD~1

# Undo last commit, keep changes unstaged
git reset --mixed HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Safe undo — create a new "revert" commit
git revert <commit>

# Remove untracked files
git clean -fd                                 # files + directories
git clean -fdn                                # dry run first
```

---

## Rebase & merge

```shell
git merge <branch>
git merge --no-ff <branch>                    # always create merge commit
git merge --squash <branch>                   # squash all commits into one staged diff

git rebase <branch>
git rebase -i HEAD~5                          # interactive rebase (squash, reword…)
git rebase --abort
git rebase --continue

git cherry-pick <commit>
git cherry-pick <commit1>..<commit2>
```

---

## Stash

```shell
git stash                                     # stash tracked changes
git stash push -m "description"
git stash push -u                             # include untracked files

git stash list
git stash pop                                 # apply latest + drop
git stash apply stash@{2}                     # apply without dropping
git stash drop stash@{0}
git stash clear                               # remove all stashes
```

---

## Tags

```shell
git tag                                       # list tags
git tag <name>                                # lightweight tag
git tag -a <name> -m "message"               # annotated tag
git tag -a <name> <commit>                    # tag a past commit

git push origin <tag>
git push origin --tags

git tag -d <name>                             # delete local tag
git push origin --delete <tag>               # delete remote tag
```

---

## GPG signing

```shell
# Sign a commit
git commit -S -m "message"

# Sign last commit (amend)
git commit -S --amend --no-edit

# Sign the last 5 commits
git rebase --signoff HEAD~5

# Check signature in log
git log --show-signature
```

!!! tip "gpg failed to sign the data"
    If you get `error: gpg failed to sign the data`, run:
    ```shell
    export GPG_TTY=$(tty)
    ```
    Add it to your shell profile (`~/.bashrc`, `~/.zshrc`) to make it permanent.

    Debug with `GIT_TRACE=1 git commit`.

---

## Useful aliases

Add to `~/.gitconfig`:

```ini
[alias]
    lg = log --oneline --graph --all --decorate
    st = status -s
    aliases = config --get-regexp alias
    autoremove = "!bash ~/bin/clean-local-branches.sh"
```

### Delete merged local branches

Save as `~/bin/clean-local-branches.sh`:

```bash
#!/usr/bin/env bash

WHITELIST="master|main|prod"

git fetch --prune
TO_REMOVE=$(git branch --merged | grep -Ev "(^\*|${WHITELIST})")

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

```shell
$ git autoremove
Branches to remove:
  dev/me/my-old-branch

Press any key to continue...
Deleted branch dev/me/my-old-branch (was a795e10).
```
