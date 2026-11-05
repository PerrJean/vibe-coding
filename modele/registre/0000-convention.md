# 0000 — Convention

Un point = un fichier : `registre/NNNN-titre-court.md`, où NNNN est le plus
grand numéro existant plus un. Aucun index tenu à la main : la liste se
calcule (`ls registre/`, `grep`).

Chaque fichier commence par son titre, `# NNNN — Titre`, puis six champs
obligatoires en tableau :

| nature | etape | statut | cout_estime | cout_reel | modele |
|---|---|---|---|---|---|
| `chantier` | `<etape>` | `ouvert` | 120 | | `<modele>` |

| champ | valeurs |
|---|---|
| **nature** | `chantier` · `defaut` · `arbitrage` |
| **etape** | une des étapes du projet, déclarées ci-dessous |
| **statut** | `ouvert` · `en cours` · `gelé` · `clos AAAA-MM-JJ` · `écarté AAAA-MM-JJ` · `remplacé par NNNN`, toujours écrit, jamais déduit |
| **cout_estime** | un nombre seul, en milliers de tokens, avant de commencer |
| **cout_reel** | un nombre seul, en milliers de tokens, à la clôture, relevé dans les compteurs de l'outil, jamais déclaré par l'agent |
| **modele** | le modèle qui a fait le chantier |

`cout_reel` reste vide tant que le point n'est pas clos. Un chantier mené en
session principale n'a **aucun coût mesurable** : il passe par un sous-agent.

Ce qui est décidé s'écrit sous une section `## Tranché`, que l'agent consulte
avant toute question. Un point remplacé garde son fichier.

## Étapes de ce projet

La convention commune ne les fixe pas : chaque projet déclare les siennes ici,
au jour 0.

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
