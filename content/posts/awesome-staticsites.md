+++
title = "Building a website using Hugo and Hosting it on GitHub Pages"
description = ""
tags = [
    "markdown",
    "development",
]
date = "2021-10-20"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
+++

## Installations
- Install Git - [Link](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
- Install Hugo - [Link](https://gohugo.io/installation/)

## Configuration
- To create a new Hugo website, run:
```bash
hugo new site mynewsite
```
- then cd to the directory
```shell
cd mynewsite
```
- Initialize the site as a git repository
```shell
git init
```
- Choose the [hugo theme](https://themes.gohugo.io/) that suits you. 
{{< hint info >}}  
Hugo offer a selection of themes developed by the community. This site for example was built using [Hugo-Book](https://github.com/alex-shpak/hugo-book).
{{< /hint >}}
- Add the theme as a submodule
```shell
# For example:
git submodule add https://github.com/alex-shpak/hugo-book themes/hugo-book
```
- Add the theme to your site configuration file
```shell
# Could be config.toml OR config.yaml OR hugo.toml OR hugo.yaml
echo "theme = 'hugo-book'" >> config.toml
```
- You will be able to see a first version of your website locally by running:
```shell
hugo server --minify 
```
- Edit your configuration file
```shell
baseURL = 'http://example.org/'
languageCode = 'en-us'
title = 'My New Hugo Site'
```

{{< hint warning >}}
**Theme ConfigurationGuidelines**  
Themes' publishers offer guidelines to configure your webiste in accordance to the theme. Check your theme publisher page on [hugo themes](https://themes.gohugo.io/) or their theme github repo for guidance and help.
{{< /hint >}}

## Hosting on Github Pages
- On your project settings, go to Pages. You'll be able to see your site's link.
- Choose a Build and deployment source (Github actions OR deploy from branch).
- You can also choose to publish it on a custom domain.
- Edit your configuration file
```shell
baseURL = 'https://username.github.io/repository'
languageCode = 'en-us'
title = 'My New Hugo Site'
theme = 'hugo-book'
```


## Other Great Tools For Building Static Websites
- Sphinx https://www.sphinx-doc.org/en/master/index.html
- VuePress https://vuepress.vuejs.org/
- Read the docs https://about.readthedocs.com/features/