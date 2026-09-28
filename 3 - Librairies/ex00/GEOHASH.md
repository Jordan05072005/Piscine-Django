<div align="center">

# 🗺️ C'est quoi un GeoHash ?

### Expliqué simplement, pour tout le monde (même les plus jeunes !)

🌍 📍 🔤 ➡️ `u09tvw7c`

</div>

---

## 🎯 En une phrase

Un **GeoHash**, c'est un petit **code magique** fait de lettres et de chiffres qui dit exactement où se trouve un endroit sur Terre — un peu comme une adresse, mais en version toute compacte !

Par exemple, au lieu d'écrire *"je suis à 48.117 de latitude et -1.677 de longitude"*, on peut simplement écrire un petit code du genre `gbvyz` 😄

## 🧩 Comment on fabrique ce code ? Le jeu du découpage

Imagine que la Terre entière est une immense feuille de papier.

1. ✂️ On la coupe en 2, dans un sens (gauche / droite)
2. ✂️ On la coupe encore en 2, dans l'autre sens (haut / bas)
3. 🔎 On regarde dans quel petit morceau se trouve l'endroit qu'on cherche
4. 🔁 Et on **recommence** : on recoupe ce morceau en 4, encore et encore...

À chaque découpage, on ajoute un petit bout au code. Plus on découpe de fois, plus le morceau devient petit — et plus notre adresse devient précise !

```
🌍 Le monde entier
        │
   ┌────┴────┐
  case A    case B
   │            │
┌──┴──┐      ┌──┴──┐
A1   A2      B1   B2
```

Chaque nouvelle coupe = une nouvelle lettre ou un nouveau chiffre ajouté au code.

## 📮 Un code qui zoome sur la carte

- `u0` → une région énorme (presque aussi grande qu'un grand pays !)
- `u09t` → la taille d'une ville
- `u09tvw7c` → la taille d'un pâté de maisons, voire d'une seule maison

**Plus le code est long, plus on est précis.** C'est comme zoomer sur une carte avec les doigts sur une tablette !

## 🔤 Pourquoi des lettres ET des chiffres ?

Pour écrire ces codes, on utilise 32 petits symboles (des chiffres et des lettres). Certaines lettres qui se ressemblent trop à l'écrit, comme le "l" et le "1", ou le "o" et le "0", ont même été mises de côté — pour éviter toute confusion en les lisant à voix haute !

## 🕵️ Le super pouvoir du GeoHash : repérer qui est proche de qui

Si deux endroits ont un code qui **commence pareil**, alors ils sont proches l'un de l'autre sur la carte !

| Lieu | Code |
|---|---|
| 🏠 Ta maison | `u09tvw7c` |
| 🍕 La pizzeria | `u09tvw7f` |

Les deux codes commencent par les mêmes lettres (`u09tvw7`) → la pizzeria est juste à côté de chez toi !

## 🍕 À quoi ça sert dans la vraie vie ?

- 📱 **Les applis de livraison** (comme celles qui t'apportent une pizza) l'utilisent pour trouver le livreur le plus proche de chez toi, très vite
- 🗺️ **Les cartes et GPS** s'en servent pour ranger des millions de lieux de façon bien organisée, comme des tiroirs classés
- 🔍 Quand tu tapes *"restaurant près de moi"*, ce genre de code aide l'ordinateur à répondre en un clin d'œil

## 🤓 Qui a inventé ça ?

Le GeoHash a été inventé en 2008 par un développeur, **Gustavo Niemeyer**. Son idée : transformer une position sur la carte (latitude + longitude) en un petit code facile à ranger et à retrouver dans un ordinateur.

## ⚠️ Un petit défaut rigolo

Parfois, deux endroits peuvent être vraiment tout proches l'un de l'autre... mais avoir un code complètement différent, juste parce qu'ils sont chacun d'un côté d'une ligne de découpage invisible ! Un peu comme deux voisins de jardin qui se retrouveraient dans deux villes différentes à cause d'une frontière qui passe entre leurs maisons. Pour ne pas les rater, les ordinateurs vérifient toujours aussi les cases juste à côté.

## 🎮 À toi de jouer !

1. Dessine un grand carré sur une feuille : c'est "le monde"
2. Coupe-le en 4 et donne un nom à chaque morceau : A, B, C, D
3. Choisis le morceau où tu voudrais "habiter", coupe-le encore en 4
4. Recommence 3 ou 4 fois

Le nom final de ta toute petite case, c'est ton propre GeoHash fait maison ! 🏆

---

## 🔧 Partie technique : comment calculer un GeoHash à la main

Voici l'algorithme exact utilisé, appliqué à deux vraies coordonnées : le centre de **Rennes** (`48.1173, -1.6778`) et la **Tour Eiffel** (`48.8584, 2.2945`).

### Le principe : une recherche par dichotomie (bissection)

On garde deux intervalles de départ :
- Latitude : `[-90, 90]`
- Longitude : `[-180, 180]`

À chaque étape, on **coupe en deux** l'intervalle courant. Si la coordonnée est dans la moitié haute, on note un bit `1` ; sinon un bit `0`. On **alterne** entre longitude et latitude à chaque bit (longitude en premier), et on **réduit** l'intervalle correspondant à la moitié où se trouve le point.

### Exemple pas à pas — Rennes (lat = 48.1173, lon = -1.6778)

| # | Axe | Milieu de l'intervalle | Comparaison | Bit |
|---|-----|------------------------|--------------|-----|
| 1 | lon | 0.0 | -1.6778 ≤ 0.0 | 0 |
| 2 | lat | 0.0 | 48.1173 > 0.0 | 1 |
| 3 | lon | -90.0 | -1.6778 > -90.0 | 1 |
| 4 | lat | 45.0 | 48.1173 > 45.0 | 1 |
| 5 | lon | -45.0 | -1.6778 > -45.0 | 1 |
| 6 | lat | 67.5 | 48.1173 ≤ 67.5 | 0 |
| 7 | lon | -22.5 | -1.6778 > -22.5 | 1 |
| 8 | lat | 56.25 | 48.1173 ≤ 56.25 | 0 |
| 9 | lon | -11.25 | -1.6778 > -11.25 | 1 |
| 10 | lat | 50.625 | 48.1173 ≤ 50.625 | 0 |

À chaque bloc de **5 bits**, on obtient une valeur entre 0 et 31, qu'on convertit avec l'alphabet base32 du GeoHash :

```
0123456789bcdefghjkmnpqrstuvwxyz
```

(remarque : ni `a`, ni `i`, ni `l`, ni `o` — pour éviter les confusions visuelles évoquées plus haut).

En répétant l'opération jusqu'à obtenir 8 caractères (40 bits, soit 8 × 5), on tombe sur :

```
48.1173, -1.6778  →  gbwc9z6r
```

### Deuxième exemple — Tour Eiffel (lat = 48.8584, lon = 2.2945)

Même mécanique, mais comme la longitude est **positive** cette fois, les premiers bits de longitude basculent à `1` dès le départ :

```
48.8584, 2.2945  →  u09tunqu
```

### Résumé de l'algorithme (pseudo-code)

```
fonction geohash(lat, lon, précision):
    plage_lat = [-90, 90]
    plage_lon = [-180, 180]
    bits = []
    axe = longitude   # on commence toujours par la longitude

    tant que len(bits) < précision * 5:
        milieu = (plage[0] + plage[1]) / 2
        si valeur(axe) > milieu:
            bits.ajoute(1)
            plage[0] = milieu
        sinon:
            bits.ajoute(0)
            plage[1] = milieu
        axe = alterner(axe)   # lon <-> lat

    regrouper les bits par paquets de 5
    convertir chaque paquet en base32 (alphabet ci-dessus)
    retourner la chaîne obtenue
```

Et c'est exactement ce mécanisme de dichotomie qui explique le "défaut rigolo" mentionné plus haut : deux points très proches mais situés juste de part et d'autre d'une frontière de milieu peuvent diverger dès les premiers bits.

---

<div align="center">

📚 *Explication inspirée de l'article [Geohashing](https://medium.com/@krthiak/geohashing-66dfc72e5062) de Karthik*

</div>
