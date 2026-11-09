# Historique

## 4.3, 9 novembre 2026

- Installation vérifiée sous Linux (WSL2) : liens à la place des jonctions, hooks déclarés avec python3, bit exécutable conservé au clone. `outils/tester_installateur.sh` rejoue ces contrôles dans un HOME jetable, sous macOS et Linux.
- Skill verification-prealable : le dépôt du modèle est trois niveaux au-dessus du lien de la skill, pas deux. Avec deux, le contrôle de dérive cherchait `modele/` dans `global/`.
- Modèle : `.github/workflows/verifier.yml` lance `./verifier` à chaque push, sur Ubuntu. En CI, `./verifier` saute les tests nommés dans `tests/locaux.txt` (données locales, secret) et le contrôle des termes interdits si leur liste est absente, et l'annonce ; sur le poste, tout est lancé. Le CLAUDE.md du modèle le dit à l'agent.
- Dépôt : un workflow lance la garde de publication et le test de l'installateur, sur Ubuntu et macOS. Sans liste privée en CI, la garde y reçoit une liste au terme introuvable : les termes privés restent contrôlés par le hook, sur le poste.

## 4.2, 9 novembre 2026

- Partie G du guide, « À tester » : une pratique y entre avec ce qu'on en attend, sa mesure et le projet où elle sera essayée, et passe dans les règles quand elle a marché dans deux projets. Le README l'annonce ; les règles 1, 3, 5 et 7, le jour 0 et les parties A, C et F y renvoient.
- À tester : partir de l'existant (la question de plus à l'interview, le gabarit officiel, ne pas coder ce qui ne différencie pas, où chercher d'abord une bibliothèque et sur quelles preuves la choisir), les décisions irréversibles du jour 0 et la revue de sécurité à chaque seuil d'exposition, le niveau de contrôle (builder, éditeur, agent) avec l'export du code vérifié avant de commencer.
- À tester aussi : la séparation du plan et de l'exécution, à l'essai dans la skill chantier, et l'effort par étape, prévu après cet essai.
- Skill chantier, à l'essai : un modèle de plan (spec, revue) et un modèle d'exécution (tests, code), déclarés dans le CLAUDE.md global ; l'exécutant remonte au modèle de plan après deux échecs, un écart ou une question non tranchée ; la fiche close note les modèles et le nombre de remontées. Le CLAUDE.md global du dépôt gagne la section Modèles à remplir.
- Skill chercher-l-existant : avant de coder un composant, chercher ce qui existe et vérifier chaque candidat avec ses sources, sans rien installer.
- Skill passation : signaler les écarts du dépôt de configuration personnelle déclaré dans le CLAUDE.md global.
- Partie F : les outils durables s'installent hors d'AppData, où une application empaquetée peut rediriger les écritures.
- Lexique : builder, décision irréversible, gabarit, seuil d'exposition.

## 4.1, 5 novembre 2026

- Première publication en dépôt public. Le guide, le modèle de projet, les skills et les hooks communs vivent désormais au même endroit et évoluent dans les mêmes commits.
- Rendue généraliste : plus de nom de projet, d'outil interne ni de chemin personnel. Le guide vaut pour tout agent de code.
- Ajouts issus de la pratique : la partie sur le travail en parallèle (index, configuration et hooks partagés entre sessions, une session ne défait pas le réglage d'une autre, hooks committés pour les worktrees), les fichiers générés livrés distingués des jetables, la règle de création et de revue des skills, un sixième champ « statut » au registre.
- Partie C : un contrôle se range selon sa durée (commit, fusion, envoi), sinon il finit désactivé.
- Le bit exécutable : `git commit -- <chemins>` reste la règle pour un fichier déjà suivi ; un nouveau script passe par `git add --chmod=+x` et un commit sans chemin. Le pre-commit du modèle refuse un hook qui n'est pas en 100755 dans l'index ; le jour 0 du README donne la commande qui les y met.

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
