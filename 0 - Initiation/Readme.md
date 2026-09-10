# Formation Python-Django - 00 : Initiation



> Projet réalisé dans le cadre du cursus École 42.

> Version du sujet : 1



## 📋 Résumé



Ce premier sujet aborde les bases du développement Web : **HTTP**, **HTML**, **CSS**, et l'intégration de scripts **JavaScript** existants dans une page.



## 📚 Règles communes



- Aucun comportement indéfini toléré (le projet est sinon considéré non fonctionnel).

- Des tests personnels sont recommandés mais ne sont ni rendus ni notés.



## 🗂️ Structure du rendu



```

.

├── ex00/

│   └── myawesomescript.sh

├── ex01/

│   └── cv.html

├── ex02/

│   ├── form.html

│   └── popup.js          (fourni, non modifiable)

├── ex03/

│   ├── copy.html

│   └── style.css         (fourni, non modifiable)

├── ex04/

│   ├── snippets.html

│   ├── file1.js          (fourni, non modifiable)

│   ├── file2.js          (fourni, non modifiable)

│   ├── file3.js          (fourni, non modifiable)

│   └── file4.js          (fourni, non modifiable)

└── ex05/

&#x20;   └── index.html

```



## 📝 Exercices



### Exercice 00 — Premier script shell

- **Rendu :** `ex00/myawesomescript.sh`

- **Commandes autorisées :** `curl`, `grep`, `cut`

- Script `/bin/sh` exécutable qui affiche l'adresse réelle vers laquelle redirige une URL `bit.ly` passée en argument.

&#x20; ```bash

&#x20; $> ./myawesomescript.sh bit.ly/1O72s3U

&#x20; http://42.fr/

&#x20; ```



### Exercice 01 — CV en HTML

- **Rendu :** `ex01/cv.html`

- Contenu minimum imposé : nom, prénom, compétences, parcours.

- Au moins un titre `<title>` et un `<h1>`.

- Au moins un tableau (`table`, `th`, `tr`, `td`) : bordures visibles (`solid`) et fusionnées (`collapse`), cellule en bas à droite en `#424242`.

- Au moins une liste `<ul>` et une liste `<ol>` (avec `<li>`).

- Séparation fond/forme et sémantique HTML respectées.

- Contrainte de syntaxe : la règle des bordures visibles/fusionnées doit être posée via une balise `<style>` dans le `<head>` ; la couleur `#424242` de la dernière cellule doit être posée via un attribut `style` inline sur la balise concernée (deux solutions syntaxiques différentes imposées).



### Exercice 02 — Formulaire d'envoi d'emails

- **Rendu :** `ex02/form.html`

- Champs requis : `Firstname` (texte), `Name` (texte), `Age` (`type="number"`), `Phone` (`type="tel"`), `Email` (`type="email"`), `Student at 42 ?` (checkbox), `Gender` (radio : Male / Female / Other).

- Bouton de soumission avec `onclick="displayFormContents();"`.

- Le fichier `popup.js` fourni (dans `d00.tar.gz/ex02/`) doit être intégré **tel quel**, sans modification, pour faire apparaître la popup avec les valeurs saisies au clic sur le bouton.



### Exercice 03 — Reproduction d'une page web

- **Rendu :** `ex03/copy.html`

- Reproduire le plus fidèlement possible la page dont le screenshot et le fichier `.css` sont fournis dans `d00.tar.gz/ex03/`.

- Le fichier CSS fourni doit être utilisé **sans modification** (une version "fraîche" sera réutilisée en soutenance).

- Séparation fond/forme, sémantique des balises et structure logique du document à respecter.



### Exercice 04 — Intégration de snippets JS

- **Rendu :** `ex04/snippets.html`

- Importer les quatre scripts fournis (`file1.js` à `file4.js`, dans `d00.tar.gz/ex04/`) de façon à ce que la popup s'affiche **correctement** (pas de caractères mal encodés).

- Contrainte stricte : uniquement importer les scripts fournis — interdiction de les modifier ou d'ajouter du JavaScript dans le HTML.



### Exercice 05 — Validation W3C

- **Rendu :** votre `ex05/index.html` corrigé.

- Corriger le fichier HTML fourni (`d00.tar.gz/ex05/`) pour qu'il passe la [validation W3C](https://validator.w3.org/) sans aucune erreur ni aucun warning.

- Le fichier doit être **corrigé**, pas tronqué : tout le contenu d'origine doit rester présent dans le rendu.



## 📤 Rendu et peer-évaluation



- Rendu via le dépôt Git assigné, avec des noms de dossiers/fichiers strictement conformes au sujet.

- Évaluation réalisée sur l'ordinateur du groupe évalué.



## 👤 Auteur



**Jordan Guaglio**

Étudiant École 42 — Perpignan

