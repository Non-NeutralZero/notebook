+++
title = "LaTex"
description = "Misc Setups and Configurations for LaTex"
tags = [
    "latex",
    "bibtex",
]
date = "2023-11-29"
categories = [
    "Utils",
]
menu = "main"
parent = "tutorials"
+++

## BibTex 
### Limit number of authors in IEEEtran
In the .bib file configure your IEEEtran as follows:

```latex
@IEEEtranBSTCTL{IEEEexample:BSTcontrol,
CTLuse_forced_etal       = "yes",
CTLmax_names_forced_etal = "3",
CTLnames_show_etal       = "2" }
```

### Cheat-sheets
- [Overleaf BibTex](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex)