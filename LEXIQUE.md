# Lexique

| Terme | Définition |
| --- | --- |
| Agent | Le modèle qui lit, écrit et exécute du code pour toi (Claude Code, Cursor, Codex, par exemple) |
| AGENTS.md, CLAUDE.md | Le fichier de règles que l'agent lit au début de chaque session |
| Arbitrage | Une règle métier que la donnée ne tranche pas, et que seul l'humain peut décider |
| Branche | Une ligne de travail parallèle dans git, fusionnée ensuite dans la branche principale |
| Branche principale (main) | La version de référence du projet |
| CI, intégration continue | Une machine qui relance les contrôles à chaque envoi de code, indépendamment de ton poste |
| Commit | Un instantané enregistré du projet, auquel on peut revenir |
| Complexité | Le nombre de chemins possibles dans une fonction. Au-delà de quelques dizaines, elle devient difficile à comprendre et à tester |
| Contexte | Tout ce que l'agent a en mémoire pendant une session. Il coûte à chaque échange et se dégrade quand il est plein |
| Contrat | Ce qui entre dans l'outil, ce qui en sort, et ce qui est hors périmètre |
| Dépôt | Le dossier du projet suivi par git, avec tout son historique |
| Diff | La différence entre deux versions d'un fichier, ligne par ligne |
| Duplication | Du code copié à plusieurs endroits. Une correction faite à un endroit ne passe pas aux autres |
| Hook | Un contrôle déclenché automatiquement, par exemple avant chaque commit ou après chaque modification de l'agent |
| Index | La zone où git prépare le prochain commit. Elle est commune à toutes les sessions qui travaillent dans le même dossier |
| KISS, YAGNI | « Fais simple » et « tu n'en auras pas besoin » : ne rien construire pour un besoin hypothétique |
| Mutation | Une erreur introduite volontairement dans le code pour vérifier que les tests la détectent |
| Passation | La note qui permet à la session suivante de reprendre sans tout relire |
| Push | L'envoi des commits locaux vers le dépôt distant |
| Registre | La liste des chantiers, défauts et arbitrages, un fichier par point, avec leur statut et leur coût |
| Session | Une conversation avec l'agent, avec son propre contexte |
| Skill | Un ensemble d'instructions que l'agent charge seulement quand la tâche le demande |
| Sous-agent | Un agent lancé par l'agent principal pour une tâche précise, dans un contexte neuf |
| Spec | La description de ce que l'outil doit faire, écrite avant de coder |
| Survie du code | La part des lignes écrites qui existent encore. Une survie faible signale du code écrit puis refait |
| Test | Un petit programme qui vérifie qu'un comportement donne le résultat attendu |
| Token | L'unité de mesure du texte traité par le modèle, et donc de son coût |
| Worktree | Une seconde copie de travail du même dépôt, avec son propre index, pour qu'une session parallèle ne touche pas les fichiers d'une autre |
