# 0001 — ./verifier et les scripts du modèle sous le bash 3.2 de macOS

| nature | etape | statut | cout_estime | cout_reel | modele |
|---|---|---|---|---|---|
| `defaut` | `modele` | `en cours` | 150 | | `claude-opus-5-5` |

## Constat

macOS fournit `/bin/bash` 3.2. `./verifier` y échouait sans le dire : `mapfile` n'existe pas,
la liste des tests restait vide, et le mode complet comme la fusion finissaient à 0 échec sans
lancer un seul test. La CI ne le voyait pas : `./verifier` n'y tournait que sous Ubuntu.

## Fait

- `mapfile` remplacé par `while IFS= read -r`.
- Boucles sur `fichiers` protégées pour un tableau vide sous `set -u` (erreur avant bash 4.4).
- Expressions régulières de `[[ =~ ]]` rangées dans des variables.
- Script Python des longueurs de fonction sorti de la substitution de processus, dans une fonction.
- `sauf` : `grep -E` au lieu de `\|`, alternance propre à GNU grep, absente du grep de macOS.
- Aucun autre usage de bash 4 dans `modele/` (`readarray`, `declare -A`, `${var,,}`, `${var^^}`,
  `&>>`, `|&`).
- `outils/tester_verifier.sh` : `./verifier` dans un projet jetable, quatre modes, en CI simulée.
- Workflow `verifier-depot` : ce test lancé avec `/bin/bash` sous macOS, avec `bash` sous Ubuntu.

## Tranché

- 2026-11-09, l'auteur du dépôt : `mapfile` remplacé par une boucle `while IFS= read -r` ; `./verifier` lancé
  dans le job macOS de la CI ; pas de push sans sa validation.
