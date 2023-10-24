+++
title = "Run plotly in JupyterLab"
description = ""
tags = [
    "jupyter",
    "development",
]
date = "2023-10-24"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
+++


```shell
    1  ! pip uninstall plotly
    2  jupyter labextension uninstall @jupyterlab/plotly-extension
    3  jupyter labextension uninstall jupyterlab-plotly 
    4  jupyter labextension uninstall plotlywidget
    5  jupyter labextension update --all
    6  pip install plotly==5.17.0
    7  pip install "jupyterlab>=3" "ipywidgets>=7.6"
    8  pip install jupyter-dash
```
## Useful Links 
- What is Right extension for Plotly in JupyterLab? 
https://stackoverflow.com/questions/62604893/what-is-right-extension-for-plotly-in-jupyterlab
- https://jupyter-docker-stacks.readthedocs.io/en/latest/
