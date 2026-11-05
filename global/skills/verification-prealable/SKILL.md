---
name: verification-prealable
description: Contrôler l'environnement avant une passe longue ou sans surveillance, dans n'importe quel projet, pour qu'elle n'échoue pas sur sa dernière étape (push refusé, verrou git, autre session, tests déjà rouges, outil absent). Rend un tableau. À charger quand l'utilisateur dit « vérification préalable », « vérifie avant de lancer », ou avant une vague, une nuit, une fenêtre où il ne surveille pas.
---
# Vérification préalable

Lecture seule, sauf les tests de l'étape 5 : ni `fetch`, ni `stash`, ni `commit`, ni verrou retiré.
Un point bloquant arrête la skill : dire à l'utilisateur quoi faire, ne pas réparer.

## 0. Lire le projet courant
- Son `CLAUDE.md`, puis `PASSATION.md` s'il existe : la commande de tests, le vérificateur et sa durée, le shell où les lancer, la branche et le remote, les outils de la passe.
- La section Environnement du `CLAUDE.md` global : outils absents connus, pièges du shell.
- Une commande que ces fichiers ne nomment pas s'inscrit « non trouvée » dans le tableau, jamais devinée.

## 1. Les contrôles
1. GitHub : `git ls-remote origin` avec `GIT_TERMINAL_PROMPT=0` et `GCM_INTERACTIVE=never`. Échec ou demande d'identifiants : bloquant.
2. Écart : sans branche distante suivie (`git rev-parse @{u}` échoue), l'inscrire. Sinon `git rev-list --count @{u}..HEAD` (commits non envoyés), puis `git merge-base --is-ancestor <hash distant de ls-remote> HEAD` : code 0, rien à récupérer ; code 1, les branches ont divergé ; erreur, hash inconnu en local, le distant a avancé. Les deux derniers cas sont bloquants si la passe finit par un push.
3. Verrou : le chemin `git rev-parse --git-path index.lock` existe. Bloquant ; l'utilisateur vérifie qu'aucun git ne tourne avant de le retirer.
4. Autre session : `git status --porcelain`, avec la date de modification des fichiers. Toute entrée vient d'une autre session ou d'un travail non committé. Bloquant seulement si ces fichiers croisent ceux que la passe va écrire.
5. Référence : relever `git status --porcelain` ; lancer les tests et le vérificateur trouvés à l'étape 0, sortie écrite dans un fichier du scratchpad ; lire la fin et le code retour, jamais `Out-Null` ni filtre qui cache l'échec ; en arrière-plan si c'est long. Relever `git status --porcelain` à nouveau : tout écart va dans le tableau. Noter chaque échec : c'est la référence à laquelle la passe se compare. Rouge n'est pas bloquant ; une commande qui ne se lance pas l'est.
6. Outils : `Get-Command` pour chacun ; un écart avec la liste du `CLAUDE.md` global se signale, avec la correction à y faire.
7. Git Bash : si un hook non `.sample` existe (`git config core.hooksPath`, sinon `.git/hooks`), `bash -c "echo ok"`. « cygheap base mismatch » : bloquant, le signaler.
8. Machine : mémoire libre (`Get-CimInstance Win32_OperatingSystem`). Si la passe tourne sans l'utilisateur : rappeler de vérifier la limite d'usage restante et de demander le maintien en éveil au lancement.
9. Contexte : au-delà de 50 % pour cette session, recommander de lancer la passe dans une session neuve. Non bloquant.

## 2. Le tableau
| Contrôle | Résultat | Bloquant |
Résultat = le chiffre ou le message, avec la commande qui l'a produit.
Sous le tableau : la référence des tests (vert, ou la liste des échecs), puis l'action exacte à faire par l'utilisateur pour chaque point bloquant. Ne rien lancer d'autre.
