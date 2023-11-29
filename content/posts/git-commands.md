+++
title = "Git commands I often use"
description = ""
tags = [
    "git",
    "shell",
    "development",
]
date = "2020-01-20"
categories = [
    "Utils",
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
