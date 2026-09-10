# Python-Django : 00 - Starting



Projet d'introduction à Python, réalisé dans le cadre de la piscine 42 Python-Django.

Objectif : découvrir la syntaxe et la sémantique de base de Python à travers une série

de courts exercices manipulant variables, dictionnaires, fichiers et génération HTML.



## Règles générales



- Aucune fonction ne doit quitter de manière inattendue (segfault, bus error, double

&#x20; free...) — hors comportements indéfinis.

- Seul le contenu du dépôt git est évalué.



## Règles spécifiques à ce projet



- Pas de code dans le scope global : tout passe par des fonctions.

- Chaque fichier rendu doit se terminer par :

&#x20; ```python

&#x20; if \_\_name\_\_ == '\_\_main\_\_':

&#x20;     your\_function(whatever, parameters, are, required)

&#x20; ```

- Aucun import n'est autorisé, sauf ceux explicitement mentionnés dans la section

&#x20; "Allowed functions" de chaque exercice.

- Les exceptions levées par `open()` n'ont pas besoin d'être gérées.

- Utiliser l'interpréteur `python3`.



## Structure du projet



| Dossier | Fichier            | Import autorisé | Description                                                        |

|---------|---------------------|------------------|----------------------------------------------------------------------|

| ex00/   | `var.py`             | —                | Déclare 9 variables de types différents et affiche leur type.       |

| ex01/   | `numbers.py`         | —                | Lit `numbers.txt` et affiche les nombres un par ligne, sans virgules.|

| ex02/   | `var\_to\_dict.py`     | —                | Convertit une liste de tuples `(nom, année)` en dictionnaire.       |

| ex03/   | `capital\_city.py`    | `sys`            | Affiche la capitale d'un état donné en argument.                    |

| ex04/   | `state.py`           | `sys`            | Affiche l'état correspondant à une capitale donnée en argument.     |

| ex05/   | `all\_in.py`          | `sys`            | Identifie, pour chaque terme d'une liste, s'il s'agit d'une capitale, d'un état, ou d'aucun des deux. |

| ex06/   | `my\_sort.py`         | —                | Trie les musiciens par année de naissance, puis alphabétiquement.   |

| ex07/   | `periodic\_table.py`  | `sys`            | Génère `periodic\_table.html`, une page HTML du tableau périodique.  |



## Détail des exercices



### ex00 — my first variables

Déclare 9 variables de types différents (`int`, `str`, `float`, `bool`, `list`, `dict`,

`tuple`, `set`, ...) et affiche pour chacune sa valeur et son type, sans jamais écrire

le type explicitement dans le code.



### ex01 — Numbers

Lit un fichier `numbers.txt` contenant les nombres de 1 à 100 séparés par des virgules,

et les affiche un par ligne, sans virgules.



### ex02 — My first dictionary

Transforme une liste de tuples `(musicien, année)` en dictionnaire `{année: musicien}`

et l'affiche sur la sortie standard.



### ex03 — Key search

Prend un état en argument et affiche sa capitale à partir d'un dictionnaire `states`

et d'un dictionnaire `capital\_cities`. Affiche `Unknown state` si l'état est inconnu ;

ne fait rien si le nombre d'arguments n'est pas exactement un.



### ex04 — Search by value

Même principe que l'ex03, mais dans l'autre sens : prend une capitale en argument et

affiche l'état correspondant.



### ex05 — Search by key or value

Prend une chaîne contenant plusieurs termes séparés par des virgules et indique, pour

chacun, s'il s'agit d'une capitale, d'un état, ou ni l'un ni l'autre. Insensible à la

casse et aux espaces multiples.



### ex06 — Dictionary sorting

Affiche les musiciens d'un dictionnaire `{nom: année}`, triés par année croissante puis

alphabétiquement en cas d'égalité.



### ex07 — Periodic table of the elements

Lit `periodic\_table.txt` et génère un fichier `periodic\_table.html` reproduisant la

disposition du tableau périodique de Mendeleïev, avec pour chaque élément une cellule

de tableau contenant son nom en `<h4>` et ses attributs (numéro atomique, symbole,

masse atomique...) dans une liste `<ul>`. Le HTML généré doit être valide W3C.



## Utilisation



```bash

python3 ex00/var.py

python3 ex01/numbers.py

python3 ex02/var\_to\_dict.py

python3 ex03/capital\_city.py Oregon

python3 ex04/state.py Salem

python3 ex05/all\_in.py "New jersey, Trenton, toto"

python3 ex06/my\_sort.py

python3 ex07/periodic\_table.py

```



## Soumission



Le rendu se fait via le dépôt git assigné. Seul le contenu du dépôt est évalué lors de

la soutenance ; des programmes de test personnels sont encouragés mais ne sont ni rendus

ni notés.

