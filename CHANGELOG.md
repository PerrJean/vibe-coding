# Historique

## 4.1, 5 novembre 2026

- Première publication en dépôt public. Le guide, le modèle de projet, les skills et les hooks communs vivent désormais au même endroit et évoluent dans les mêmes commits.
- Rendue généraliste : plus de nom de projet, d'outil interne ni de chemin personnel. Le guide vaut pour tout agent de code.
- Ajouts issus de la pratique : la partie sur le travail en parallèle (index, configuration et hooks partagés entre sessions, une session ne défait pas le réglage d'une autre, hooks committés pour les worktrees), les fichiers générés livrés distingués des jetables, la règle de création et de revue des skills, un sixième champ « statut » au registre.
- Partie C : un contrôle se range selon sa durée (commit, fusion, envoi), sinon il finit désactivé.
- Le bit exécutable : `git commit -- <chemins>` reste la règle pour un fichier déjà suivi ; un nouveau script passe par `git add --chmod=+x` et un commit sans chemin. Le pre-commit du modèle refuse un hook qui n'est pas en 100755 dans l'index.

## 4, 5 novembre 2026

- Structure en trois parties selon le lecteur : un socle de 14 règles, une partie pour aller plus loin, et un modèle pour l'agent. La v3 était organisée par thème, en 29 commandements.
- Le pourquoi reste côté humain ; les règles côté agent sont à l'impératif et sans justification. Les contrôles sont fournis plutôt que décrits.
- Les chiffres passés en annexe.
- Nouvelles règles du socle : décider personnel ou à reprendre (3), un prompt une tâche et la passation (8), décisions consultées avant toute question (9), pas de fichiers produits dans git (10), un chiffre se calcule (13).
- Règles nuancées après relecture par un développeur : les valeurs hors du code mais pas d'abstraction avant le deuxième cas (7), un circuit du premier jour concret et non une architecture (5), des plafonds de taille qui valent pour tous les langages et sont des détecteurs de principes non respectés.

## 3, 2 octobre 2026

- Confrontation à un kit interne de contribution encadré par une équipe tech : ajout du squelette du premier jour, des tests déterministes, du test des tests, des droits minimum, du budget d'exécution et d'une commande de vérification unique.

## 2, 22 septembre 2026

- Confrontation à la documentation officielle de Claude Code, au format AGENTS.md, à la pratique spec-driven et à deux sources empiriques de 2026.

## 1, septembre 2026

- Première version, tirée des mesures d'un projet d'audit de contenu : 69 modules, 69 555 lignes, 233 points de décision, 30 millions de tokens sur 4 semaines.
