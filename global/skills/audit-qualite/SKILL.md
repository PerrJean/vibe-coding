---
name: audit-qualite
description: Audit en lecture seule de la qualité du dépôt courant (le code est-il gonflé ou mal conçu ?), en dix mesures chiffrées, avec un rapport au format fixe et comparable d'un audit à l'autre, dans Documents\audit-qualite. À lancer par /audit-qualite.
disable-model-invocation: true
---

# Audit qualité d'un dépôt

But : dire, chiffres à l'appui, si le code est gonflé ou mal conçu. Des faits mesurés, pas une opinion.

## Règles
- Lecture seule stricte : rien n'est modifié, déplacé, supprimé ni committé dans le dépôt. Ni add, ni commit, ni stash, ni checkout, ni reset. Relever `git status --porcelain` au début et à la fin. S'ils diffèrent, montrer l'écart et prouver qu'il ne vient pas de l'audit (une autre session peut travailler dans l'arbre).
- Figer le commit au départ (`git rev-parse HEAD`) : son SHA complet et sa date ouvrent le rapport, et toutes les mesures portent sur lui, même si HEAD avance. Ce qui n'est pas committé est hors périmètre.
- Les mesures 2 et 3 lisent l'historique dans le dépôt, en lecture seule, sur le SHA figé (`git log <sha>`, `git blame <sha> -- <fichier>`). Les mesures 1, 4 à 9 et la lecture du registre (10) portent sur une copie extraite par `git archive <sha>`.
- `<Documents>` est le chemin réel des Documents, `[Environment]::GetFolderPath('MyDocuments')`. Le rapport, les scripts et les sorties brutes vont dans `$D` = `<Documents>\audit-qualite\<depot>-<AAAA-MM-JJ>\`. Jamais `%TEMP%`, jamais le dépôt.
- La copie extraite et les outils vont toujours dans `$env:USERPROFILE\.cache\audit-qualite\`, jamais sous Documents (pas `LOCALAPPDATA`, que l'app Claude redirige vers son propre cache : une session lancée depuis un terminal n'y trouverait pas les outils). La copie dans `<depot>-<AAAA-MM-JJ>\`, supprimée à la fin ; les outils dans `outils\`, gardés d'un audit à l'autre (un venv Python pour radon et vulture, jscpd par npm en version épinglée). Rien ne demande de droits d'administrateur. Appeler les outils Python par `python -m`, car leurs .exe peuvent être bloqués. Si un outil ne s'installe pas, le dire et continuer.
- Chaque chiffre sort d'une commande, écrite à côté de lui. Jamais estimé, jamais de mémoire.
- Toute correction faite en cours de route (règle changée, mesure refaite, chiffre rectifié) est écrite dans le rapport, avec l'ancienne et la nouvelle valeur.

## Étape 0 : classement, puis validation
1. Chercher un rapport précédent sur ce dépôt (`<depot>.md` ou `<depot>-*.md`). S'il en existe un, partir de sa règle de classement.
2. Classer chaque fichier de `git ls-tree -r --name-only <sha>` : code, tests, données, documentation, interface, configuration, généré. Ajouter une catégorie propre au dépôt seulement si elle est justifiée. Les règles sont ordonnées et la première qui correspond l'emporte. « Généré » veut dire écrit par une commande du dépôt.
3. Montrer à l'utilisateur la règle (règle, catégorie, nombre de fichiers), les écarts avec la règle précédente et les cas douteux. **Attendre sa validation avant de mesurer.**

## Les dix mesures (même périmètre pour toutes)
1. Composition : fichiers, lignes et octets par catégorie, en nombre et en %. Les 10 plus gros fichiers, avec leur catégorie.
2. Ajouts et suppressions sur tout l'historique (`git log <sha> --numstat -M`), par catégorie : lignes ajoutées, supprimées, ratio.
3. Survie du code : lignes de code présentes (`git blame <sha> -- <fichier>`) / lignes de code ajoutées. Même calcul sur les fichiers modifiés dans les 21 jours suivant leur création. Donner le chiffre avec et sans le premier commit s'il importe du code existant. Si l'historique fait moins de 90 jours, marquer le chiffre « non interprétable » au lieu de le commenter.
4. Taille, tous langages, HTML compris : fichiers de plus de 500 et de plus de 800 lignes, nommés ; fonctions de plus de 80 lignes, nommées.
5. Complexité : radon cc pour Python (rangs C à F, les 10 plus complexes). Pour les autres langages, l'outil disponible, sinon le dire.
6. Duplication : jscpd sur le code (tests et données exclus), avec `--max-lines` et `--max-size` levés, car ses plafonds par défaut écartent les gros fichiers sans prévenir. Donner le % de lignes dupliquées et les 5 plus gros blocs. Lister les fichiers que jscpd n'a pas su lire, et les reporter dans les limites.
7. Code mort : vulture `--min-confidence 80` pour Python, nombre d'éléments et les 10 premiers. Donner aussi le nombre d'éléments à `--min-confidence 60`, comme piste non vérifiée.
8. Tests : lignes de tests / lignes de code, et tests logés dans les fichiers de code.
9. Fichiers générés ou de données versionnés : taille cumulée et copies identiques. Distinguer les générés **livrés** (versionnés volontairement, déclarés dans la convention du projet : CLAUDE.md, registre, README) des générés **jetables** ; seuls les seconds comptent comme « fichiers qui pourraient ne pas être versionnés ». Citer la ligne de la convention qui déclare chaque groupe livré.
10. Registre de chantiers ou de décisions (decisions.json, PASSATION.md, registre/…) : part des points clos de nature « défaut ». Compter les fiches au statut ambigu (coût noté d'un tiret, statut contradictoire avec le coût), et donner la part de défauts avec et sans elles. S'il n'y a pas de registre, le dire.

## Rapport : `<Documents>\audit-qualite\<depot>-<AAAA-MM-JJ>.md`
Reprendre le format des rapports déjà présents dans le dossier :
1. En-tête : date, SHA complet, branche, périmètre exclu, notations des commandes (`$R`, `$D`, `$PY`…), règle de classement validée.
2. `## Synthèse` : une ligne par mesure, avec la valeur et la commande. Si un audit précédent existe, ajouter une colonne « Évolution » (avant → maintenant) et signaler les lignes qu'un changement de règle rend non comparables.
3. `## Mesures` : les sections 1 à 10.
4. `## Ce que les chiffres disent`, séparé des mesures, en trois sous-sections : signes de gonflement ou de mauvaise conception ; volume expliqué par autre chose que du code ; ce que les mesures ne permettent pas de conclure.
5. `## Limites de l'analyse` : outils qui n'ont pas tourné, fichiers que jscpd n'a pas lus, périmètre exclu, corrections faites en cours de route.

## Avant de rendre
- Comparer le `git status --porcelain` final à l'initial, et écrire le résultat dans le rapport.
- Donner à l'utilisateur le chemin du rapport et les trois constats principaux.
