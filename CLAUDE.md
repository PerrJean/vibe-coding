# Règles du dépôt

Ce dépôt est public. Tout ce qui y entre devient public, et reste dans l'historique même après suppression.

## Avant d'agir
- Lis PASSATION.md s'il existe (note locale, jamais committée) et le dernier commit. Rien d'autre sans raison.
- Une décision déjà prise est dans PASSATION.md, le CHANGELOG ou un commit. Cherche-la avant de me poser la question.
- Une tâche par demande. Si la tâche touche plus de deux fichiers, dis-le.

## Rien de personnel
- Aucun nom de personne ni d'organisation privée (seule exception : l'auteur, dans LICENSE), chemin personnel, adresse e-mail, nom de projet, de client ou d'outil interne, secret. Les noms d'outils et de sources publiques restent permis. Écris `<projet>`, `$env:USERPROFILE`, `~`.
- La garde de publication (.githooks/pre-commit, pre-merge-commit pour une fusion, commit-msg pour le message et les identités) le contrôle à chaque commit, pre-push sur chaque commit envoyé. Auteur et validateur : adresse masquée GitHub. Ne la contourne jamais : ni --no-verify, ni core.hooksPath changé, ni liste retirée de vibe.listes.
- Un refus de la garde se corrige dans le fichier, ou se signale. Une liste privée ne se lit pas et ne s'affiche jamais.

## Git
- Toute session qui écrit travaille dans son propre worktree.
- Commit après chaque étape qui marche, avec tes seuls fichiers. Un commit par point demandé.
- Fichier entièrement à toi et déjà suivi : git commit -- <chemins>. Nouveau script, ou fichier dont le mode change : vérifie que l'index ne contient rien d'autre, git add --chmod=+x <fichier>, puis git commit sans chemin, puis git ls-files -s <fichier> doit afficher 100755.
- Ne défais jamais un réglage git fait par une autre session : signale-le.
- Fusionne avec git merge --no-ff : une avance rapide ne joue aucun hook.

## Push
- Push libre quand : le pre-push passe (garde sur la plage), les tests passent, et le diff relu ne contient aucune donnée personnelle, même absente des listes.
- Sur main : seulement par git merge --no-ff d'une branche dont la CI est verte.
- Demande toujours avant : push --force ou réécriture d'historique, suppression d'une branche distante, modification de .githooks/ ou des listes de vibe.listes, LICENSE*, et tout doute sur une donnée personnelle.

## Contenu
- Textes (README, guides, lexique, annexe, CHANGELOG) sous CC BY 4.0 ; code (modele/, global/, outils/) sous MIT. Un nouveau dossier de code s'ajoute à la phrase de licence du README.
- LICENSE-TEXTES est le texte officiel : ne le modifie jamais.
- Le pourquoi vit dans les textes. modele/ et global/ sont lus par l'agent : impératif, sans justification.
- Tout changement visible s'inscrit au CHANGELOG. Nouvelle version : relance python outils/estampiller_modele.py.
- global/skills/ et global/hooks/ sont reliés à ~/.claude sur ce poste : une modification y est active aussitôt, dans toutes les sessions.
- Une skill de global/skills/ se modifie dans le dépôt, sur une branche et dans un worktree, jamais à travers ~/.claude : la jonction mène au dossier principal et contourne le worktree.

## Code
- Fichier de code : 500 lignes maximum. Fonction : au-delà de 80 lignes, scinde ou justifie.
- Un script de modele/ ou de global/ se teste dans un dépôt ou un dossier jetable du scratchpad, jamais sur ce dépôt ni sur ~/.claude.
- Après une modification de global/hooks/ : py_compile, puis un essai sur un fichier jetable. Une erreur y coupe la garde de diff en silence.
- Une modification de global/skills/ n'est terminée qu'après avoir marché dans deux projets.

## Preuve
- Avant de déclarer une tâche finie : python .githooks/garde_publication.py --disque. Colle sa sortie.
- Tout chiffre cité sort d'une commande. Jamais de compte de mémoire.

## Fin de session
- Au-delà de 80 % de contexte : commit, mets à jour PASSATION.md, arrête.
