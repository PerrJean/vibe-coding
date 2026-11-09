# 0000 — Convention

Modèle vibe-coding 4.3

Commune à tous les projets qui suivent le modèle. **En vigueur depuis le
2026-11-05** : les fiches antérieures gardent leur forme, leurs coûts et leur
numéro ; rien n'est renormalisé ni renuméroté.

## Un point = un fichier

`registre/NNNN-titre-court.md`, numéro à quatre chiffres, le plus grand
existant plus un, **un numéro par fichier** pour tout nouveau point. Un
sous-chantier reste une section de sa fiche. Une annexe vit hors de
`registre/`. Aucun index tenu à la main : la liste se calcule (`ls registre/`,
`grep`).

La fiche commence par :

```
# NNNN — Titre

| nature | etape | statut | cout_estime | cout_reel | modele |
|---|---|---|---|---|---|
| `chantier` | `<étape>` | `ouvert` | 120 | | `claude-opus-5-5` |
```

## Les six champs

| champ | valeurs |
|---|---|
| **nature** | `chantier` · `defaut` · `arbitrage` — trois, pas d'autre |
| **etape** | une valeur de la liste que ce projet déclare, ci-dessous |
| **statut** | `ouvert` · `en cours` · `gelé` · `clos AAAA-MM-JJ` · `écarté AAAA-MM-JJ` · `remplacé par NNNN`, toujours écrit, jamais déduit |
| **cout_estime** | un nombre seul, en milliers de tokens, posé avant de commencer |
| **cout_reel** | un nombre seul, en milliers de tokens, relevé à la clôture dans les compteurs de l'outil, jamais déclaré par l'agent |
| **modele** | l'identifiant exact (`claude-opus-5-5`) ; plusieurs séparés par une virgule |

- Une cellule de coût ne porte **qu'un nombre** ; le détail par sous-chantier
  va sous le tableau.
- `cout_reel` reste vide tant que le point n'est pas clos. Le coût d'un
  sous-agent se relève par la session qui l'a lancé. Un chantier mené en
  session principale n'a aucun coût mesurable : il passe par un sous-agent.
- `remplacé par NNNN` marque une règle ou un arbitrage obsolète : on ne
  l'applique plus, on lit le point qui le remplace. Le point remplacé garde
  son fichier.

## Le tranché

Chaque fiche qui a reçu des réponses porte une section `## Tranché` : une
ligne par réponse, datée, avec qui a tranché. L'agent la consulte avant toute
question, et une question qui y figure n'est plus jamais présentée comme
ouverte.

## Étapes de ce projet

La convention commune n'en définit aucune : chaque projet déclare ici les
siennes, et `etape` ne prend que ces valeurs.

- `<etape-1>` : <ce qu'elle couvre>
- `<etape-2>` : <ce qu'elle couvre>

## Mesure

**Recalibrage tous les 30 points clos**, avec cinq chiffres et un arrêt
possible :

1. ratio coût réel sur coût estimé (seuil 2) ;
2. part de défauts parmi les points clos (seuil 30 %) ;
3. taille du plus gros fichier (seuil : toute croissance continue) ;
4. durée de l'exécution la plus lente ;
5. lignes supprimées par ligne ajoutée.

Budget de l'outil qui sert à faire l'outil : **plafond 15 %**.
