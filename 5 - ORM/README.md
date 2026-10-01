<a id="top"></a>

<div align="center">

# 🌌 d05 — L'ORM de Django, une base de données très très lointaine…

*Piscine Python-Django · Jour 05 · SQL brut 🆚 ORM*

![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-psycopg2-4169E1?logo=postgresql&logoColor=white)
![Exercices](https://img.shields.io/badge/exercices-11%2F11-success)

```
        .           *        A long time ago, in a database far,
   *         .            far away…
        _____________________________________________________
       |  ex00 ─ ex02 ─ ex04 ─ ex06 ─ ex08   →  SQL  (psycopg2)
       |  ex01 ─ ex03 ─ ex05 ─ ex07 ─ ex09 ─ ex10 → ORM (Django)
        ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾
```

</div>

---

## 🧭 Sommaire

| | Section | |
|---|---|---|
| 🎯 | [Le principe](#principe) | SQL 🆚 ORM, exercice par exercice |
| 🧠 | [Compétences mobilisées](#competences) | ce que le projet fait pratiquer |
| 🗺️ | [Le modèle de données](#modele) | planètes, personnages, films |
| 🚀 | [Démarrage rapide](#demarrage) | de zéro au serveur lancé |
| 🧰 | [Le Makefile](#makefile) | `init`, `run`, `stop`, `migrate`, `delete` |
| 🐍 | [Commandes Django](#django) | serveur, migrations, remplissage, shell |
| 🐘 | [Commandes PostgreSQL](#psql) | `psql`, méta-commandes, requêtes |
| 🗂️ | [Les exercices en détail](#exercices) | URLs et points à vérifier |
| 🐛 | [Les pièges du côté obscur](#pieges) | erreurs rencontrées et solutions |
| 📁 | [Structure](#structure) | arborescence du rendu |

---

<a id="principe"></a>

## 🎯 Le principe

Chaque notion est vue **deux fois** : d'abord à la main, en SQL avec `psycopg2`, puis avec l'**ORM de Django**, sans écrire une seule ligne de SQL. Les données ? Les films, les personnages et les planètes de Star Wars. 🚀

| | 🛠️ SQL (psycopg2) | 🪄 ORM (Django) |
|---|---|---|
| **Créer une table** | [ex00](#ex-sql-orm) | [ex01](#ex-sql-orm) |
| **Insérer** | [ex02](#ex-sql-orm) | [ex03](#ex-sql-orm) |
| **Supprimer** | [ex04](#ex-sql-orm) | [ex05](#ex-sql-orm) |
| **Mettre à jour** | [ex06](#ex-sql-orm) *(+ trigger)* | [ex07](#ex-sql-orm) *(`auto_now`)* |
| **Clé étrangère** | [ex08](#ex-sql-orm) *(`copy_from`)* | [ex09](#ex-sql-orm) *(fixtures)* |
| **Many-to-Many** | — | [ex10](#ex10) *(recherche multi-critères)* |

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="competences"></a>

## 🧠 Compétences mobilisées

| Domaine | Ce qui a été pratiqué |
|---|---|
| 🐘 **PostgreSQL** | `CREATE TABLE IF NOT EXISTS`, contraintes (`UNIQUE`, `NOT NULL`, `PRIMARY KEY`, `FOREIGN KEY`), `JOIN`, `LIKE`, fonctions et **triggers PL/pgSQL** |
| 🔌 **psycopg2** | connexions, curseurs, transactions (`commit` / `rollback`), requêtes paramétrées `%s` (anti-injection SQL), chargement massif avec `copy_from` |
| 🧬 **Modèles Django** | `CharField`, `BigIntegerField`, `FloatField`, `DateTimeField(auto_now…)`, `ForeignKey(to_field=…)`, `ManyToManyField`, modèles abstraits |
| 🔎 **QuerySets** | `filter`, `values_list`, `order_by`, `distinct`, lookups `__gte` / `__contains` / `__range`, traversée de relations `a__b__c`, évaluation paresseuse |
| 📝 **Formulaires** | `forms.Form`, `ChoiceField` aux choix dynamiques, héritage de formulaires, `cleaned_data`, pattern *POST → redirect* |
| 📦 **Données** | fixtures JSON, `loaddata`, **commandes de management personnalisées** (`load_ex09`, `load_ex10`) |
| ⚙️ **Outillage** | Makefile, `.env`, migrations, `psql` |

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="modele"></a>

## 🗺️ Le modèle de données

```
   ┌──────────────────┐          ┌──────────────────────┐          ┌──────────────────┐
   │     PLANETS      │          │        PEOPLE        │          │      MOVIES      │
   ├──────────────────┤          ├──────────────────────┤          ├──────────────────┤
   │ id          PK   │          │ id             PK    │          │ episode_nb  PK   │
   │ name     UNIQUE  │◀────────┐│ name        UNIQUE   │          │ title    UNIQUE  │
   │ climate          │  1    N ││ gender               │          │ director         │
   │ diameter         │         └┤ homeworld  FK → name │          │ producer         │
   │ population       │          │ height, mass, …      │          │ release_date     │
   │ created/updated  │          │ created/updated      │          │ opening_crawl    │
   └──────────────────┘          └──────────┬───────────┘          └────────┬─────────┘
                                            │ N                           N │
                                            │   ┌───────────────────────┐   │
                                            └──▶│ movies_characters     │◀──┘
                                                │ movies_id | people_id │
                                                └───────────────────────┘
                                                  table intermédiaire
                                                  créée par Django 🪄
```

- **Une planète ↔ plusieurs habitants** : `ForeignKey` (ex08, ex09, ex10)
- **Plusieurs films ↔ plusieurs personnages** : `ManyToManyField` (ex10)

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="demarrage"></a>

## 🚀 Démarrage rapide

```bash
# 1. Environnement : venv, dépendances et variables, tout est dans le script
source my_script

# 2. Base de données + migrations
make init        # démarre PostgreSQL, crée le rôle et la base
make migrate     # génère et applique les migrations

# 3. Données des exercices ORM avec fixtures
python manage.py load_ex09 ex09/ressources/ex09_initial_data.json
python manage.py load_ex10 ex10/ressources/ex10_initial_data.json

# 4. Lancement
make run         # → http://127.0.0.1:8000/
```

> 💡 `source`, et non `./my_script` : le script doit s'exécuter **dans le shell courant** pour que l'environnement virtuel reste activé après.

➡️ Le détail des commandes : [Makefile](#makefile) · [Django](#django) · [PostgreSQL](#psql)

### 🔐 Le fichier `.env`

Le Makefile et `settings.py` lisent les identifiants dans un fichier `.env` à la racine :

```env
POSTGRES_DB=formationdjango
POSTGRES_USER=djangouser
POSTGRES_PASSWORD=secret
```

> 📌 Le sujet impose la base **`formationdjango`**, le rôle **`djangouser`** et le mot de passe **`secret`**.

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="makefile"></a>

## 🧰 Le Makefile

```makefile
include .env
export

init:
	sudo service postgresql start
	sudo -u postgres psql -c "DO \$$\$$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$(POSTGRES_USER)') THEN CREATE USER $(POSTGRES_USER) WITH PASSWORD '$(POSTGRES_PASSWORD)'; END IF; END \$$\$$;"
	sudo -iu postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$(POSTGRES_DB)'" | grep -q 1 || sudo -iu postgres psql -c "CREATE DATABASE $(POSTGRES_DB) OWNER $(POSTGRES_USER);"
	pg_lsclusters

run:
	python manage.py runserver

stop:
	sudo service postgresql stop

migrate:
	python manage.py makemigrations
	python manage.py migrate

delete:
	sudo -iu postgres psql -c "DROP DATABASE IF EXISTS $(POSTGRES_DB) WITH (FORCE);"
	sudo -iu postgres psql -c "DROP USER IF EXISTS $(POSTGRES_USER);"
	find . -path "*/migrations/0*.py" -delete
	find . -path "*/migrations/__pycache__" -type d -exec rm -rf {} +
```

| Commande | Ce qu'elle fait |
|---|---|
| `make init` | 🟢 Démarre PostgreSQL, crée le rôle **seulement s'il n'existe pas** (bloc `DO $$ … $$`), crée la base **seulement si elle n'existe pas**, puis affiche l'état des clusters. Peut être relancée sans risque. |
| `make run` | ▶️ Lance le serveur de développement sur `127.0.0.1:8000`. |
| `make stop` | ⏹️ Arrête le service PostgreSQL. |
| `make migrate` | 🔄 Génère les migrations depuis les modèles, puis les applique en base. |
| `make delete` | 💣 Supprime la base **et** le rôle, puis efface toutes les migrations générées. Repart d'une page blanche (le sujet interdit de rendre des migrations). |

> ⚠️ Dans un Makefile, les lignes de commande commencent par une **tabulation**, jamais par des espaces. Sinon : `missing separator. Stop.`

### 🔁 Cycle de vie typique

```
  source my_script ──▶ make init ──▶ make migrate ──▶ load_ex09 / load_ex10 ──▶ make run
                           ▲                                                      │
                           └─────────────── make delete (reset total) ◀───────────┘
```

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="django"></a>

## 🐍 Commandes Django utiles

### Serveur et état du projet

```bash
python manage.py runserver              # lance le serveur
python manage.py check                  # vérifie la configuration sans démarrer
python manage.py showmigrations         # migrations appliquées [X] ou non [ ]
python manage.py showmigrations ex10    # … pour une seule app
```

### Migrations

```bash
python manage.py makemigrations         # génère les migrations de toutes les apps
python manage.py makemigrations ex09    # … d'une seule app
python manage.py migrate                # applique tout
python manage.py sqlmigrate ex10 0001   # 👀 affiche le SQL généré par une migration
```

### Remplissage de la base

```bash
# Fixture standard
python manage.py loaddata chemin/vers/fichier.json

# Commandes personnalisées : convertissent les homeworld (pk → name)
# et ajoutent created/updated absents, sans modifier le fichier fourni
python manage.py load_ex09 ex09/ressources/ex09_initial_data.json
python manage.py load_ex10 ex10/ressources/ex10_initial_data.json
```

> 🤔 Pourquoi des commandes personnalisées ? Voir [les pièges](#pieges).

### Explorer à la main

```bash
python manage.py shell                  # console Python avec Django chargé
python manage.py dbshell                # ouvre psql directement sur la base du projet
```

```python
>>> from ex10.models import People, Movies
>>> People.objects.count()
>>> People.objects.filter(homeworld__climate__contains="windy").order_by("name")
>>> Movies.objects.get(episode_nb=4).characters.all()
```

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="psql"></a>

## 🐘 Commandes PostgreSQL (`psql`)

### Se connecter

```bash
psql -h localhost -U djangouser -d formationdjango
```

### Méta-commandes (sans `;`)

| Commande | Effet |
|---|---|
| `\l` | liste les bases |
| `\du` | liste les rôles |
| `\dt` | liste les tables |
| `\d ex10_people` | structure d'une table (colonnes, types, contraintes, FK) |
| `\df` | liste les fonctions (le trigger de l'ex06 !) |
| `\x` | affichage vertical, pratique pour les longues lignes |
| `\r` | vide la requête en cours |
| `\q` | quitte |

### Requêtes SQL (avec `;` !)

```sql
-- Toutes les données d'une table
SELECT * FROM ex02_movies;

-- Vérifier le trigger de l'ex06 : updated doit changer, pas created
UPDATE ex06_movies SET opening_crawl = 'Test' WHERE episode_nb = 1;
SELECT title, created, updated FROM ex06_movies WHERE episode_nb = 1;

-- La jointure de l'ex08 : les personnages des planètes venteuses
SELECT ex08_people.name, ex08_people.homeworld, ex08_planets.climate
FROM ex08_people
JOIN ex08_planets ON ex08_people.homeworld = ex08_planets.name
WHERE ex08_planets.climate LIKE '%windy%'
ORDER BY ex08_people.name;

-- La table intermédiaire Many-to-Many de l'ex10
\d ex10_movies_characters
SELECT * FROM ex10_movies_characters LIMIT 10;

-- Repartir de zéro sur une table
DROP TABLE ex08_people;
```

> 💡 Si l'invite devient `formationdjango->` (avec un tiret), c'est que `psql` attend la fin de la requête : il manque le `;`.

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="exercices"></a>

## 🗂️ Les exercices en détail

<a id="ex-sql-orm"></a>

| Ex | Type | URLs | Ce qu'il faut voir |
|---|---|---|---|
| **00** | 🛠️ SQL | `/ex00/init` | Création de table, `OK` ou message d'erreur |
| **01** | 🪄 ORM | — | Le modèle `Movies`, visible après `make migrate` |
| **02** | 🛠️ SQL | `/ex02/init` → `/populate` → `/display` | Un `OK` par film, erreurs de doublon au 2ᵉ appel |
| **03** | 🪄 ORM | `/ex03/populate` → `/display` | Même chose avec `Movies.objects.create` |
| **04** | 🛠️ SQL | `/ex04/init` → `/populate` → `/display` → `/remove` | Liste déroulante, suppression, liste mise à jour |
| **05** | 🪄 ORM | `/ex05/populate` → `/display` → `/remove` | Même chose avec `.delete()` |
| **06** | 🛠️ SQL | `/ex06/init` → `/populate` → `/display` → `/update` | Le **trigger** met à jour `updated` ([vérifier en psql](#psql)) |
| **07** | 🪄 ORM | `/ex07/populate` → `/display` → `/update` | `auto_now` via `.save()` (et non `.update()`) |
| **08** | 🛠️ SQL | `/ex08/init` → `/populate` → `/display` | `copy_from` + `JOIN` sur les planètes venteuses |
| **09** | 🪄 ORM | `/ex09/display` | Fixture + `ForeignKey` vers `Planets.name` ([chargement](#django)) |
| **10** | 🪄 ORM | `/ex10/` | Recherche multi-critères à travers FK **et** M2M ([exemple](#ex10)) |

<a id="ex10"></a>

### 🔍 Exemple ex10

> Genre `female`, films sortis entre `1900-01-01` et `2000-01-01`, planète de diamètre ≥ `11000` :

| Personnage | Genre | Film | Planète | Diamètre |
|---|---|---|---|---|
| Padmé Amidala | female | The Phantom Menace | Naboo | 12120 |
| Leia Organa | female | A New Hope | Alderaan | 12500 |
| Leia Organa | female | The Empire Strikes Back | Alderaan | 12500 |
| Leia Organa | female | Return of the Jedi | Alderaan | 12500 |
| Mon Mothma | female | Return of the Jedi | Chandrila | 13500 |

```python
People.objects.filter(
    gender=gender,
    homeworld__diameter__gte=diameter,
    movies__release_date__range=(date_min, date_max),
).values_list("name", "gender", "movies__title", "homeworld__name", "homeworld__diameter")
```

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="pieges"></a>

## 🐛 Les pièges du côté obscur

*Ce qui a résisté, et ce qu'on en a appris.*

| 💥 Symptôme | 🧘 Explication |
|---|---|
| L'erreur SQL échappe au `try/except` | Les QuerySets sont **paresseux** : la requête part quand le template les lit. ➜ `list(queryset)` dans le `try`. |
| `not enough values to unpack (expected 2, got 1)` | Les `choices` d'un `ChoiceField` doivent être des paires `(valeur, texte)`. |
| `Cannot resolve keyword 'characters_gender'` | Traverser une relation demande **deux** underscores : `characters__gender`. |
| `null value in column "created"` au `loaddata` | `loaddata` enregistre en mode *raw* : `auto_now` et `auto_now_add` ne s'appliquent pas. ➜ commande `load_ex10`. |
| `Key (homeworld_id)=(214) is not present` | La fixture référence les planètes par `pk`, le modèle par `name`. ➜ conversion à la volée dans `load_ex09`. |
| `invalid input syntax for type bigint: "NULL"` | Le texte `"NULL"` du CSV doit devenir `None`, ou passer par `copy_from(null="NULL")`. |
| `ModuleNotFoundError: No module named 'google'` | Import fantôme ajouté par l'auto-import de l'éditeur. 👻 |
| `/ex05/ex05/remove` en 404 | URL relative sans `/` initial. ➜ `{% url 'ex05:remove' %}` ou `redirect(request.path)`. |
| `missing separator. Stop.` | Des espaces au lieu d'une tabulation dans le [Makefile](#makefile). |

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<a id="structure"></a>

## 📁 Structure

```
d5/
├── d5/                 # configuration du projet (settings, urls)
├── ex00/ … ex10/       # une app Django par exercice
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── ex09/ressources/ex09_initial_data.json
├── ex10/ressources/ex10_initial_data.json
├── .env
├── Makefile
├── my_script           # venv + dépendances + variables
└── manage.py
```

<div align="right"><a href="#top">⬆️ Sommaire</a></div>

---

<div align="center">

*Que la Force (et l'ORM) soit avec toi.* ✨

</div>
