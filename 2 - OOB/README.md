<div align="center">

# 🐍 Python-Django — Module 1 : Librairies

### Formation 42 — Apprivoiser l'écosystème Python avant de plonger dans Django

![42](https://img.shields.io/badge/42-000000?style=for-the-badge&logo=42&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Bash](https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white)
![Status](https://img.shields.io/badge/Status-Validé-brightgreen?style=for-the-badge)

*« Rien ne sert de courir, il faut installer les bonnes librairies. »*

</div>

---

## 📖 Sommaire

- [Présentation](#-présentation)
- [Le clin d'œil du sujet](#-le-clin-dœil-du-sujet)
- [Règles du jeu](#-règles-du-jeu)
- [Les 6 exercices](#️-les-6-exercices)
- [Compétences acquises](#-compétences-acquises)
- [Structure du rendu](#-structure-du-rendu)
- [Installation & Utilisation](#-installation--utilisation)
- [Auteur](#-auteur)

---

## 🎯 Présentation

Ce projet est le premier module de la formation **Python-Django** à 42. L'objectif n'est pas encore de construire une application complète, mais d'apprendre à **maîtriser l'écosystème de librairies Python** : installation, gestion d'environnements, consommation d'API, scraping HTML — bref, tout l'outillage indispensable avant d'attaquer Django sérieusement le lendemain.

En six exercices progressifs, on part d'un simple easter egg (`import antigravity`) pour arriver à un vrai **« Hello World » sous Django**, en passant par l'installation de librairies tierces, le requêtage de l'API Wikipédia et un petit crawler qui vérifie une légende bien connue du web.

## 🧭 Le clin d'œil du sujet

Le sujet s'ouvre sur une référence au *geohashing*, cette activité inspirée d'un webcomic xkcd où l'on part à la recherche de coordonnées générées aléatoirement, sans autre but que l'aventure elle-même. Une manière assumée de dire : ce module n'a pas un objectif "produit" spectaculaire, mais chaque exercice est un prétexte pour explorer un outil ou une librairie utile — et s'amuser en chemin.

## 📜 Règles du jeu

| Contrainte | Détail |
|---|---|
| 🖥️ Environnement | Développement en machine virtuelle, avec un dossier partagé pour le rendu |
| 🧱 Code propre | Aucun code dans le scope global — tout passe par des fonctions |
| 🚪 Point d'entrée | Chaque fichier se termine par un bloc `if __name__ == '__main__':` |
| 📦 Imports | Uniquement les librairies explicitement autorisées par exercice |
| 🐍 Interpréteur | `python3` exclusivement |
| 💥 Robustesse | Aucun crash toléré (segfault, bus error, double free...) sous peine de 0 au projet |

## 🗂️ Les 6 exercices

| # | Nom | Objectif | Librairies clés |
|---|-----|----------|------------------|
| 00 | **Antigravity** | Exercice d'échauffement : calcul et affichage d'un géohash | `sys`, `antigravity` |
| 01 | **Pip** | Script Bash d'installation + programme Python utilisant `path.py` | `path.py` |
| 02 | **Requêter une API** | Interroger l'API Wikipédia et nettoyer le résultat (JSON/Wiki Markup) | `requests`, `json`, `dewiki` |
| 03 | **Parser du HTML** | Vérifier la légende *"tous les chemins mènent à Philosophie"* via scraping | `requests`, `BeautifulSoup` |
| 04 | **Virtualenv** | Préparer un environnement virtuel Django + psycopg2 | `virtualenv` |
| 05 | **Hello World** | Premier projet Django fonctionnel sur `/helloworld` | `Django` |

### 🔎 Détail par exercice

**Ex00 — Antigravity**
`geohashing.py` calcule un géohash typique à partir des paramètres fournis, avec une gestion d'erreur propre.

**Ex01 — Pip**
`my_script.sh` affiche la version de pip, installe `path.py` en local (`local_lib/`), journalise l'installation, puis lance `my_program.py`, qui crée un dossier, écrit un fichier, puis le relit.

**Ex02 — Requêter une API**
`request_wikipedia.py "<recherche>"` interroge l'API Wikipédia, nettoie le résultat de tout balisage et l'écrit dans un fichier `nom_de_la_recherche.wiki` — sans jamais créer de fichier en cas d'erreur.
```
$ python3 request_wikipedia.py "chocolatine"
$ cat chocolatine.wiki
Une chocolatine designe : ...
```

**Ex03 — Parser du HTML**
`roads_to_philosophy.py "<recherche>"` remonte de lien en lien depuis un article Wikipédia jusqu'à l'article *Philosophy*, en gérant redirections, impasses et boucles infinies.
```
$ python3 roads_to_philosophy.py "42 (number)"
...
17 roads from 42 (number) to philosophy !
```

**Ex04 — Virtualenv**
Un `requirement.txt` (dernières versions stables de Django et psycopg2) et un script Bash qui crée le venv `django_venv`, y installe les dépendances, et le laisse activé.

**Ex05 — Hello World**
Premier projet Django, suivant le tutoriel officiel, qui affiche `Hello World !` sur `http://localhost:8000/helloworld`.

## 🛠️ Compétences acquises

- ⚙️ Installation et gestion de librairies Python tierces (pip, dépôts GitHub)
- 🐚 Scripting Bash pour automatiser une installation et journaliser ses logs
- 🌐 Consommation d'API REST et parsing de réponses JSON
- 🕷️ Web scraping avec BeautifulSoup et gestion des cas limites (redirection, boucle, impasse)
- 🧪 Isolation des dépendances via `virtualenv`
- 🎸 Premiers pas avec le framework **Django** (routes, vues)
- 🧹 Rigueur de code : gestion d'erreurs propre, pas de crash, structure modulaire

## 📦 Structure du rendu

```
.
├── ex00/
│   └── geohashing.py
├── ex01/
│   ├── my_script.sh
│   └── my_program.py
├── ex02/
│   ├── request_wikipedia.py
│   └── requirement.txt
├── ex03/
│   ├── roads_to_philosophy.py
│   └── requirement.txt
├── ex04/
│   ├── requirement.txt
│   └── my_script.sh
└── ex05/
    └── <projet Django>
```

## 🚀 Installation & Utilisation

```bash
# Ex00 — Antigravity
python3 ex00/geohashing.py <paramètres>

# Ex01 — Pip
./ex01/my_script.sh

# Ex02 — Requêter Wikipédia
python3 ex02/request_wikipedia.py "chocolatine"

# Ex03 — Roads to Philosophy
python3 ex03/roads_to_philosophy.py "42 (number)"

# Ex04 — Virtualenv Django
./ex04/my_script.sh

# Ex05 — Hello World Django
python3 ex05/manage.py runserver
# puis ouvrir http://localhost:8000/helloworld
```

## 👤 Auteur

Projet réalisé dans le cadre du cursus **42**.

---

<div align="center">

*Formation Python-Django - 1 : Librairies — 42*

</div>
