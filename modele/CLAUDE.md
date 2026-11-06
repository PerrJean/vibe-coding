# Règles du projet

Modèle vibe-coding 4.1

## Avant d'agir
- Lis PASSATION.md et le dernier commit. Rien d'autre sans raison.
- Avant de me poser une question, cherche la réponse dans registre/ (sections « Tranché »).
- Une tâche par demande. Si la tâche touche plus de deux fichiers, dis-le.

## Code
- Fichier de code : 500 lignes maximum, tous langages. Au-delà, scinde selon les responsabilités.
- Fonction : au-delà de 80 lignes, scinde ou justifie.
- Sépare récupération des données, calculs et affichage.
- Passe connexions, clients et horloge en paramètre.
- Pas de valeur métier en dur : table de référence.
- Pas d'abstraction avant le deuxième cas réel. Pas d'option non demandée.
- Noms : vocabulaire du glossaire. Mot absent : demande.
- Avant d'écrire un utilitaire, cherche une bibliothèque.

## Tests
- Tests dans tests/, jamais dans src/.
- Sur données réelles anonymisées. Date fixée. Ordre explicite.
- Règle métier non tranchée par la donnée : test ignoré marqué ARBITRAGE.

## Preuve
- Lance ./verifier avant de déclarer une tâche finie. Colle sa sortie.
- Tout chiffre cité sort d'une commande. Jamais de compte de mémoire.

## Git
- Toute session qui écrit travaille dans son propre worktree.
- Commit après chaque étape qui marche, avec tes seuls fichiers.
- Fichier entièrement à toi et déjà suivi : git commit -- <chemins>. Nouveau script, ou fichier dont le mode change : vérifie que l'index ne contient rien d'autre, git add --chmod=+x <fichier>, puis git commit sans chemin, puis git ls-files -s <fichier> doit afficher 100755.
- Les fichiers interdits sont dans .gitignore et refusés par le hook. Ne jamais utiliser --no-verify.
- Ne défais jamais un réglage git fait par une autre session : signale-le.
- Fusionne avec git merge --no-ff : une avance rapide ne joue aucun hook.

## Fin de session
- Au-delà de 80 % de contexte : commit, mets à jour PASSATION.md, arrête.
