# Règles communes à tous les projets

Ce fichier vaut pour toutes les sessions. Les règles propres à un projet vivent dans le CLAUDE.md du projet et priment.

## Environnement
À remplir une fois, puis à garder à jour. L'agent ne devine rien de cette section.
- Système : <Windows 11 | macOS | Linux>
- Shell utilisé par l'agent : <PowerShell 7 | Git Bash | WSL2 bash | zsh>. N'écris aucune commande d'un autre shell.
- Dossier des projets : <$env:USERPROFILE\projets | ~/projets>
- Langages installés : <Python 3.x avec uv, Node xx, ...>
- Dépôt distant : <GitHub | GitLab>, connexion testée le <AAAA-MM-JJ>
- Droits d'administration : <oui | non>. Sans droits, n'installe rien qui en demande.
- Outils disponibles : <git, gh, uv, ruff, ...>
- Langue des échanges : <français>

## Avant d'agir
- Une tâche par demande. Si elle touche plus de deux fichiers, dis-le avant de commencer.
- Une décision déjà prise est dans un fichier du projet (registre/, SPEC.md, CONTRAT.md). Cherche-la avant de me poser la question.
- Ce que la donnée ne tranche pas est une question pour moi, jamais une hypothèse.

## Preuve
- Avant de déclarer une tâche finie, lance la commande de vérification du projet et colle sa sortie.
- Tout chiffre cité sort d'une commande. Jamais de compte de mémoire.

## Git
- Toute session qui écrit travaille dans son propre worktree.
- Commit après chaque étape qui marche, avec tes seuls fichiers (git commit -- <chemins>).
- Ne jamais utiliser --no-verify. Un hook qui refuse se corrige, ou se signale.
- Ne défais jamais un réglage git fait par une autre session : signale-le.
- Rien n'est envoyé sur le dépôt distant sans ma demande.

## Secrets et données
- Aucun secret dans le code ni dans git : fichier local ignoré, ou variable d'environnement.
- Données réelles de personnes : anonymisées dans les tests, absentes de git et des sorties qui n'en ont pas besoin.

## Skills
- Propose une skill en fin de tâche quand le même enchaînement, aux conventions stables, a été refait trois fois. Ne l'écris qu'après validation.
- Une skill commune ne cite aucun fichier en dur : elle découvre les conventions du projet courant.

## Fin de session
- Au-delà de 80 % de contexte : commit, note de passation, arrêt.
