+++
title = "How to document your code?"
description = ""
tags = [
    "scala",
    "templates",
    "development",
]
date = "2014-04-02"
categories = [
    "Development",
    "Tutorials",
]
menu = "main"
parent = "tutorials"
weight = 10
+++

## Comment documenter ?
Les mêmes principes et critères d’un bon code devraient s’appliquer à la documentation:
- Conventionnelle
- Simple
- Facile à comprendre

En plus des critères d’un bon code, une bonne documentation devrait aussi être:
- Explicative (intention du code, règles métiers, clarification du code, mise en garde sur les conséquences d’une mauvaise
utilisation, indications pour le testing)
- Non-redondante

```scala
/**
* Returns the temperature.
*/
int get_temperature(void) {
return temperature;
}
```

- Non-bruitée
```scala
/**
* Always returns true.
*/
public boolean isAvailable()
{ return false;}
```

## Bonnes pratiques
### Introduire son code.
Décrire le contexte ou le background du code est une bonne pratique qui permettra aux lecteurs de se positionner par
rapport aux conditions dans lesquelles le code a été généré et à ses objectifs.
### Connaître son public!
Avant de documenter, le développeur doit se poser la question: “qui sont/seront mes lecteurs?”. Une documentation visant
un nettoyeur de données (focus ici sur les règles métiers par exemple) est différente d’une documentation visant un
analyste de donnée (focus sur comment utiliser le code par exemple)
Alerter sur les dépendances. Lister et décrire les perspectives du code.
### “No comment out”, i.e. Ne jamais retirer des lignes de documentation!
Si la documentation est bien faite et le code ne suit pas (à cause d’un refactor ou d’une modification), cela veut dire que le
code ne fonctionne plus et qu’il devrait être supprimé ou lourdement remanié.
### Être gentil 
Être gentil en laissant des exemples! Nice developers leave nice examples :)
### KID - keep it documented!
Un refactor ou modification sans revue de documentation veut juste dire que le développeur n’a rien compris à ce
document !

## Quelques bons exemples de documentation
### Instruction sur l’utilisation et renseignement sur le format de l’output

```scala
/**
* Returns the temperature in tenth degrees Celsius
* in range [0..1000], or -1 in case of an error.
*
* The temperature itself is set in the periodically
* executed read_temperature() function.
*
* Make sure to call init_adc() before calling this
* function here, or you will get undefined data.
*/
int get_temperature(void) {
return temperature; }
```

### Contextualisation du code et restriction sur son utilisation

```scala
/**
*
* This is for testing purposes only and should
* never be called from a real program.
*/
int get_temperature(void) {
return temperature;}
```


