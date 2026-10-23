# 📰 The Journal

> *« J’ai voulu construire une petite étagère à condiments.
> On m’a vendu une fabrique de fabrique de fabrique de marteaux. »*
> — Le préambule de ce sujet, et honnêtement, un bon résumé de Django.

**The Journal** est un site de publication d’articles réalisé pendant la **Piscine Python-Django de 42 (jour 7 – Avancé)**.
On y lit des articles, on en publie, on garde ses préférés en favoris… et tout ça en anglais **ou** en français, d’un simple clic sur un drapeau. 🇬🇧 🇫🇷

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2_LTS-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-4169E1?logo=postgresql&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-7952B3?logo=bootstrap&logoColor=white)
![i18n](https://img.shields.io/badge/i18n-EN%20%7C%20FR-e8b021)
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)

---

## 🎯 Le pitch en 30 secondes

| Tu es…              | Tu peux…                                                                 |
|---------------------|--------------------------------------------------------------------------|
| 👀 Simple visiteur   | Parcourir les articles, lire leur détail, créer un compte                |
| ✍️ Utilisateur connecté | Publier un article, retrouver tes publications, gérer tes favoris ⭐ |
| 🌍 Polyglotte        | Basculer tout le site entre `/en/` et `/fr/` sans perdre ta page        |

---

## 🧱 Les règles du jeu (et comment je les ai respectées)

Le sujet impose des contraintes strictes. Les voici, avec la façon dont le projet y répond :

- **Zéro vue sous forme de fonction** → uniquement des vues génériques (`ListView`, `DetailView`, `CreateView`, `RedirectView`, `TemplateView`, `LoginView`, `LogoutView`).
- **Zéro URL en dur** → chaque lien passe par `{% url 'nom' %}` dans les templates et par `reverse()` / les noms de routes dans les vues. Indispensable avec les préfixes de langue !
- **L’anglais par défaut** → `LANGUAGE_CODE = "en"`, avec un choix de langue mémorisé par cookie.
- **L’admin Django conservée** → disponible sur `/en/admin/`.

---

## 🗺️ Fonctionnalités, exercice par exercice

| Ex. | Thème | Ce qui a été construit |
|-----|-------|------------------------|
| **00** | Modèles & vues génériques | Modèles `Article` et `UserFavouriteArticle`, liste des articles en tableau, redirection de la Home, page de connexion avec gestion des erreurs, données d’exemple générées par `make data` |
| **01** | Vues génériques v2 | Publications de l’utilisateur, page Détail, déconnexion, liste des favoris |
| **02** | `CreateView` | Inscription, publication d’article (auteur rempli côté serveur), ajout aux favoris via un formulaire sans champ visible |
| **03** | Tags & filtres | Menu présent sur toutes les pages (avec formulaire de login intégré), synopsis tronqué à 20 caractères, tri par date, colonne « publié depuis » |
| **04** | Bootstrap | Navbar sombre fidèle à la maquette, onglet actif mis en valeur, menu responsive |
| **05** | Internationalisation | Traduction EN / FR selon le préfixe d’URL, drapeaux pour changer de langue sur la même page |
| **06** | Tests | Batterie de tests automatisés couvrant les accès, l’inscription et les favoris |

---

## 🛠️ Stack technique

- **Back** : Python 3.10, Django 5.2 LTS
- **Base de données** : PostgreSQL 14, via l’ORM de Django
- **Front** : templates Django, Bootstrap 5.3, un soupçon de JavaScript (`fetch`) pour les favoris
- **i18n** : GNU gettext (`.po` / `.mo`), `i18n_patterns`, `LocaleMiddleware`
- **Outillage** : Makefile, environnement virtuel Python, framework de tests intégré à Django

---

## 🏗️ Architecture

Le projet est découpé en applications aux responsabilités claires :

```
d7/
├── d7/            ⚙️  configuration (settings, urls racine, i18n)
├── home/          🏠 base.html, navbar, page d’accueil, middleware de langue
├── accounts/      🔐 inscription, connexion, déconnexion
├── articles/      📰 liste, détail, publication, favoris
├── profileUser/   👤 espace perso : publications & favoris
├── locale/        🌍 traductions françaises
└── Makefile       🤖 installation et lancement en une commande
```

Les templates reposent sur l’héritage (`base.html` → `profile_base.html` → pages) et sur des fragments réutilisables (`navbar.html`, `favorite.html`) inclus avec `{% include %}`.

---

## 🚀 Lancer le projet

Trois étapes, et le journal est sous presse. 🗞️

### 1. Préparer l’environnement

Depuis la racine du dépôt, un seul script installe tout ce qu’il faut (paquets système, environnement virtuel, dépendances Python) :

```bash
source my_script.sh
```

Il installe `python3-venv`, PostgreSQL et GNU gettext, crée l’environnement virtuel `django_venv`, l’active et y installe les dépendances de `requirements.txt`.

> ⚠️ Utilise bien `source` et non `bash` : le script active l’environnement virtuel, et seul `source` permet à cette activation de rester effective dans ton terminal.

### 2. Configurer les accès à la base

Crée un fichier `.env` à côté du `Makefile`. Il est lu à la fois par le `Makefile` (création de la base) et par Django (connexion) :

```env
POSTGRES_DB=djangodb
POSTGRES_USER=djangouser
POSTGRES_PASSWORD=un_mot_de_passe
```

### 3. Démarrer

```bash
make
```

Cette seule commande démarre PostgreSQL, crée l’utilisateur et la base s’ils n’existent pas, applique les migrations et lance le serveur. Ouvre ensuite **http://127.0.0.1:8000** : tu atterris directement sur la liste des articles. 🎉

Pour remplir le site d’articles, d’utilisateurs et de favoris d’exemple :

```bash
make data
```

### 🤖 Les commandes du Makefile

| Commande | Ce qu’elle fait |
|----------|-----------------|
| `make` ou `make start` | Enchaîne `init`, `migrate` et `run` : de zéro à un site en ligne en une commande |
| `make init` | Démarre PostgreSQL, crée l’utilisateur et la base définis dans `.env` (sans rien écraser s’ils existent déjà), puis affiche l’état du cluster |
| `make migrate` | Génère et applique les migrations des modèles |
| `make run` | Lance le serveur de développement sur `127.0.0.1:8000` |
| `make data` | Peuple la base avec des données d’exemple (commande `seed`) |
| `make test` | Exécute toute la suite de tests |
| `make delete` | 💣 Remet tout à zéro : supprime la base, l’utilisateur PostgreSQL et les fichiers de migration |

> 🧨 `make delete` est irréversible : tous les articles, comptes et favoris disparaissent. Pratique pour repartir d’une base propre, à éviter la veille d’une soutenance.

### Les traductions

```bash
python manage.py makemessages -l fr      # extrait les textes à traduire
python manage.py compilemessages         # compile le .po en .mo
```

---

## 🧪 Les tests

```bash
make test
```

Les tests portent des noms explicites et vérifient que :

- 🔒 **Favourites**, **Publications** et **Publish** (vues *et* templates) ne sont accessibles qu’aux utilisateurs connectés, les autres étant redirigés vers la connexion ;
- 🚪 un utilisateur connecté **ne peut pas** accéder au formulaire d’inscription ;
- ⭐ un utilisateur **ne peut pas** mettre deux fois le même article en favoris.

Chaque test tourne dans une base PostgreSQL éphémère, recréée puis détruite automatiquement : les vraies données ne sont jamais touchées.

> 💡 Le compte PostgreSQL doit avoir le droit `CREATEDB` pour que Django puisse créer cette base de test.

---

## 🐛 Le bestiaire des bugs vaincus

Un projet, c’est aussi les monstres qu’on a terrassés en chemin. Florilège :

| Le monstre | Son pouvoir | Comment il a été vaincu |
|---|---|---|
| 🦎 **La virgule fantôme** | `model = Article,` transforme silencieusement une classe en tuple | Lire les messages d’erreur (`'tuple' object…`) et traquer les virgules en fin de ligne |
| 🌀 **Le POST qui devient GET** | Avec `i18n_patterns`, un formulaire vers `/logout/` est redirigé vers `/en/logout/`… en GET, donc refusé (405) | Remplacer chaque URL en dur par `{% url %}` : la règle du sujet n’était pas là par hasard |
| 👯 **Le favori cloné** | Deux clics = `IntegrityError` sur la contrainte d’unicité | Vérification d’existence avant création, et un test qui verrouille le comportement |
| 🏴‍☠️ **Le squatteur du port 5432** | Un PostgreSQL Windows oublié bloquait celui de WSL | Diagnostic avec `ss`, `netstat` et `tasklist`, puis arrêt du service fautif |
| 🌫️ **L’entrée *fuzzy*** | Une traduction devinée et marquée douteuse, ignorée à la compilation | Relecture du `.po` et suppression du marqueur `#, fuzzy` |
| 🔇 **Le `{% load i18n %}` oublié** | Une page d’inscription qui plante pour tout le monde | Débusqué… par les tests. Exactement leur rôle. |

---

## 💪 Compétences mises en œuvre

**Django en profondeur**
- Vues génériques basées sur les classes et leurs points d’extension (`get_context_data`, `form_valid`, `form_invalid`, `get_success_url`, `dispatch`)
- ORM : clés étrangères, `UniqueConstraint`, requêtes filtrées, `exists()`, tri par défaut
- Authentification : `LoginView`, `LogoutView`, `LoginRequiredMixin`, `login_required`, `redirect_authenticated_user`
- Formulaires : `ModelForm`, champs cachés préremplis, données sensibles remplies côté serveur

**Templates**
- Héritage, blocs, inclusions de fragments
- Filtres et tags natifs : `truncatechars`, `dictsortreversed`, `timesince`, `date`, `linebreaks`, `with`, `url`
- Mise en valeur de l’onglet actif grâce à `request.resolver_match`

**Internationalisation**
- `i18n_patterns`, `LocaleMiddleware`, vue `set_language`
- Chaîne complète gettext : `makemessages`, édition du `.po`, `compilemessages`
- Langue par défaut maîtrisée et choix de l’utilisateur conservé entre les visites

**Qualité & sécurité**
- Tests automatisés avec le client de test, `reverse`, `subTest`, `assertTemplateUsed`
- Protection CSRF, filtrage systématique par `request.user`, champs sensibles exclus des formulaires
- Redirections robustes face aux données inattendues

**Environnement**
- PostgreSQL sous WSL, gestion des rôles et des droits
- Makefile d’installation et de lancement, environnement virtuel, variables dans un `.env`
- Débogage réseau et système (ports, services, configuration WSL)

---

## 🙏 Remerciements

À Django, pour m’avoir vendu une fabrique de fabrique de marteaux…
et pour m’avoir finalement appris à m’en servir. 🔨

*Fait avec ☕, 🐍 et beaucoup de lectures de tracebacks, à 42.*
