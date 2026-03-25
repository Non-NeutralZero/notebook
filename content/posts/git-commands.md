+++
title = "Git commands I often use"
description = ""
tags = [
    "git",
]
date = "2020-01-20"
categories = [
    "reference",
]
menu = "main"
parent = "tutorials"
+++


## Add
```shell
# only add files with .scala extension
git ls-files [path] | grep '\.scala$' | xargs git add
git stash --keep-index
```

## Log & History
```shell
# compact, visual branch graph
git log --oneline --graph --decorate --all

# search commits by message
git log --grep="keyword"

# show changes introduced by each commit
git log -p --follow -- path/to/file

# who changed what line
git blame -L 10,20 file.txt
```

## Diff
```shell
# diff staged changes (what's about to be committed)
git diff --staged

# diff between two branches
git diff main..feature-branch
```

## Undo / Fix
```shell
# undo last commit but keep changes staged
git reset --soft HEAD~1

# amend last commit (message or content)
git commit --amend --no-edit

# discard changes in a file
git checkout -- file.txt

# recover a dropped stash or deleted commit
git reflog
```

## Branches
```shell
# delete remote branch
git push origin --delete branch-name

# rename current branch
git branch -m new-name

# show which branch a commit is in
git branch --contains <commit-hash>
```

## Stash
```shell
# stash with a name
git stash push -m "wip: auth refactor"

# apply specific stash
git stash apply stash@{2}

# list stashes
git stash list
```

## Productivity
```shell
# find which commit introduced a bug (binary search)
git bisect start
git bisect bad        # current is broken
git bisect good v1.0  # last known good

# apply a single commit from another branch
git cherry-pick <commit-hash>

# rebase interactively (squash, reorder, edit)
git rebase -i HEAD~3
```
