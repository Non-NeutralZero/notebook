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
- [Overleaf, Bibliography management with bibtex](https://www.overleaf.com/learn/latex/Bibliography_management_with_bibtex)
- [Sébastien Merkel, Reference sheet for natbib usage](http://merkel.texture.rocks/Latex/natbib.php)
- [LaTeX/Bibliography Management. (2023, June 5). Wikibooks.](https://en.wikibooks.org/wiki/LaTeX/Bibliography_Management)
- [Discipline Specific Listings of BibTeX Journal Styles](https://www.reed.edu/it/help/LaTeX/bibtexstyles.html#:~:text=the%20official%20style.-,Discipline%20Specific%20Listings%20of%20BibTeX%20Journal%20Styles,-Art)