+++
title = "Install python packages offline"
description = "How to Install Python packages offline"
tags = [
    "pip",
    "^python",
]
date = "2023-06-08"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
+++

1- Download packages locally using a requirements file or download a single package
```shell
pip download -r requirements.txt
```

```shell
## Example - single package
python -m pip download \
--only-binary=:all: \
--platform manylinux1_x86_64 --platform linux_x86_64 --platform any \
--python-version 39 \
--implementation cp \
--abi cp39m --abi cp39 --abi abi3 --abi none \
scipy
```

2- Copy them to the a temporary folder in your remote machine
3- On your machine, Activate conda and then install them using pip - specify installation options
```shell
conda activate base
## Example of pip install
pip install scipy-1.7.1-cp39-cp39-manylinux_2_5_x86_64.manylinux1_x86_64.whl
```