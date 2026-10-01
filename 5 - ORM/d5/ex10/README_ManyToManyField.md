# Relations plusieurs-à-plusieurs (Many-to-Many)

Ce document explique comment relier deux tables quand **chaque élément d'un côté peut être lié à plusieurs éléments de l'autre côté**, et inversement. On prend comme exemple les films et les personnages de Star Wars.

---

## 1. La situation

- Un **film** contient **plusieurs** personnages.
- Un **personnage** apparaît dans **plusieurs** films.

```
        FILMS                          PERSONNAGES
  ┌──────────────────┐            ┌──────────────────┐
  │ A New Hope       │──────┬────▶│ Luke Skywalker   │
  │                  │──┐   │ ┌──▶│ Leia Organa      │
  │                  │─┐│   │ │┌─▶│ Darth Vader      │
  └──────────────────┘ ││   │ ││  └──────────────────┘
  ┌──────────────────┐ ││   │ ││
  │ Empire Strikes   │─┼┼───┘ ││
  │ Back             │─┼┼─────┘│
  │                  │─┼┼──────┘
  └──────────────────┘ │└──▶ (Leia)
                       └───▶ (Vader)
```

Luke est lié à **deux** films, et chaque film est lié à **trois** personnages. C'est une relation **plusieurs-à-plusieurs**.

---

## 2. Rappel : la relation un-à-plusieurs (ForeignKey)

Pour comparer, voici une relation plus simple : un personnage n'a **qu'une seule** planète d'origine, mais une planète peut avoir **plusieurs** habitants.

```
     PLANETS                     PEOPLE
  ┌────┬──────────┐        ┌────┬────────────────┬───────────┐
  │ id │ name     │        │ id │ name           │ homeworld │
  ├────┼──────────┤        ├────┼────────────────┼───────────┤
  │ 1  │ Tatooine │◀───────│ 1  │ Luke Skywalker │ 1         │
  │    │          │◀───────│ 2  │ Darth Vader    │ 1         │
  │ 2  │ Alderaan │◀───────│ 3  │ Leia Organa    │ 2         │
  └────┴──────────┘        └────┴────────────────┴───────────┘
```

Une seule colonne (`homeworld`) suffit, parce que chaque personnage n'a **qu'une** valeur à stocker.

Pour les films, ça ne marche plus : un film a **plusieurs** personnages, et une case ne peut contenir qu'**une** valeur.

---

## 3. Fausse bonne idée n°1 : plusieurs colonnes

```
┌────┬────────────┬─────────────┬─────────────┬─────────────┐
│ id │ title      │ character_1 │ character_2 │ character_3 │
├────┼────────────┼─────────────┼─────────────┼─────────────┤
│ 1  │ A New Hope │ 1           │ 3           │ 2           │
└────┴────────────┴─────────────┴─────────────┴─────────────┘
```

❌ Combien de colonnes prévoir ? 3 ? 50 ? Et comment chercher « tous les films de Luke » sans tester chaque colonne une par une ?

---

## 4. Fausse bonne idée n°2 : un tableau dans une case

PostgreSQL accepte les colonnes de type tableau (`INTEGER[]`) :

```
┌────┬────────────┬────────────┐
│ id │ title      │ characters │
├────┼────────────┼────────────┤
│ 1  │ A New Hope │ {1, 3, 2}  │
│ 2  │ Empire...  │ {1, 3, 2}  │
└────┴────────────┴────────────┘
```

Ça fonctionne, mais avec de vrais inconvénients :

| Problème | Conséquence |
|---|---|
| Pas de clé étrangère sur les éléments du tableau | On peut y mettre l'id `999` d'un personnage qui n'existe pas |
| Recherche inverse lente | « Les films de Luke » oblige à parcourir **tous** les tableaux |
| Modification pénible | Retirer un personnage oblige à réécrire tout le tableau |
| Contraire à la normalisation | Une case devrait contenir **une seule** valeur |

👉 Les tableaux sont utiles pour des listes **simples et indépendantes** (des tags, des numéros de téléphone), mais pas pour relier deux tables.

---

## 5. ✅ La bonne solution : une table intermédiaire

On crée une **troisième table**, dont chaque ligne représente **un lien** entre un film et un personnage.

```
      FILMS                FILMS_CHARACTERS               PEOPLE
 ┌────┬────────────┐     ┌──────────┬───────────┐     ┌────┬────────────────┐
 │ id │ title      │     │ films_id │ people_id │     │ id │ name           │
 ├────┼────────────┤     ├──────────┼───────────┤     ├────┼────────────────┤
 │ 1  │ A New Hope │◀────│ 1        │ 1         │────▶│ 1  │ Luke Skywalker │
 │    │            │◀────│ 1        │ 2         │────▶│ 2  │ Darth Vader    │
 │    │            │◀────│ 1        │ 3         │────▶│ 3  │ Leia Organa    │
 │ 2  │ Empire...  │◀────│ 2        │ 1         │──┐  └────┴────────────────┘
 │    │            │◀────│ 2        │ 2         │  │
 │    │            │◀────│ 2        │ 3         │  └─▶ (Luke, encore)
 └────┴────────────┘     └──────────┴───────────┘
```

Une ligne `(1, 1)` signifie : « Luke apparaît dans A New Hope ».

Chaque colonne est une **clé étrangère** : PostgreSQL vérifie que le film et le personnage existent bien.

### En SQL

```sql
CREATE TABLE films (
    id SERIAL PRIMARY KEY,
    title VARCHAR(64) NOT NULL
);

CREATE TABLE people (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL
);

CREATE TABLE films_characters (
    films_id  INTEGER REFERENCES films(id)  ON DELETE CASCADE,
    people_id INTEGER REFERENCES people(id) ON DELETE CASCADE,
    PRIMARY KEY (films_id, people_id)       -- interdit les doublons
);
```

Ajouter un lien :

```sql
INSERT INTO films_characters (films_id, people_id) VALUES (1, 1);
```

Les personnages d'un film :

```sql
SELECT people.name
FROM people
JOIN films_characters ON films_characters.people_id = people.id
WHERE films_characters.films_id = 1;
```

Les films d'un personnage (la recherche inverse, aussi simple) :

```sql
SELECT films.title
FROM films
JOIN films_characters ON films_characters.films_id = films.id
WHERE films_characters.people_id = 1;
```

---

## 6. Avec Django : `ManyToManyField`

Django crée la table intermédiaire **tout seul**. Il suffit de déclarer le champ :

```python
class Movies(models.Model):
    title = models.CharField(max_length=64)
    characters = models.ManyToManyField(People, related_name="movies")
```

⚠️ **Aucune colonne `characters`** n'est ajoutée dans la table des films. Django crée une table `<app>_movies_characters`, exactement comme celle de la section 5.

### Utilisation

```python
film = Movies.objects.get(title="A New Hope")
luke = People.objects.get(name="Luke Skywalker")

film.characters.add(luke)       # ajoute un lien  (INSERT dans la table intermédiaire)
film.characters.remove(luke)    # retire un lien  (DELETE dans la table intermédiaire)
film.characters.all()           # les personnages du film

luke.movies.all()               # les films de Luke (grâce à related_name)
```

### Filtrer à travers la relation

```python
# Les films où apparaît au moins un personnage féminin
Movies.objects.filter(characters__gender="female").distinct()
```

`.distinct()` évite d'obtenir le même film plusieurs fois s'il contient plusieurs personnages qui correspondent.

---

## 7. Résumé

| Relation | Exemple | Outil SQL | Outil Django |
|---|---|---|---|
| Un-à-plusieurs | Une planète ↔ ses habitants | Une colonne clé étrangère | `ForeignKey` |
| Plusieurs-à-plusieurs | Des films ↔ des personnages | Une table intermédiaire | `ManyToManyField` |

**À retenir :** une case contient **une seule valeur**. Dès qu'un élément doit être lié à **plusieurs** autres, et inversement, on passe par une **table intermédiaire**, où chaque ligne représente un lien.
