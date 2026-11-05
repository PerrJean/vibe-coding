# Annexe. Ce que chaque règle a coûté

Les chiffres viennent de trois sources : le retour d'expérience d'un premier projet vibe codé (233 points de décision, 30 millions de tokens sur 4 semaines), deux mois de rapports d'usage d'un agent de code (79 sessions), et l'audit qualité en lecture seule de trois projets. Le premier projet a été écrit avant ces règles, les deux autres en les appliquant.

## Le premier projet face aux deux suivants

| Mesure | Premier projet | Deuxième projet | Troisième projet |
| --- | --- | --- | --- |
| Fichiers de code au-delà de la limite | 33 de plus de 800 lignes sur 72 | aucun au-delà de 500 | aucun au-delà de 500 (hors une page HTML de 2 612 lignes) |
| Plus grosse fonction | 1 768 lignes, complexité 274 | 221 lignes, complexité 64 | 175 lignes (dans une page HTML) |
| Fonctions de plus de 80 lignes | 90 | 4 | 8 |
| Tests intégrés aux fichiers de code | 21,8 % des lignes de code | 0 | 0 |
| Duplication | 0,27 % | 0,69 % (12,1 % en SQL) | 4,63 % (scripts annexes) |
| Lignes supprimées par ligne ajoutée | 0,23 | non mesuré | 0,06 (documentation) |
| Part de défauts parmi les points clos | 31,2 % | 18,1 % | 9,4 % |
| Part du dépôt occupée par des fichiers produits | 96,1 % des octets | deux fichiers générés | 63 % des octets |

## Règle par règle

| Règle | Ce que son absence a coûté |
| --- | --- |
| 4. Git dès le premier fichier | 14 jours de travail hors historique, donc non mesurables |
| 6. Lire la donnée | Un nom de champ supposé trois fois le même jour, 51 % d'artefacts sur une mesure. 21 des 209 points clos étaient des arbitrages découverts en route |
| 8. Frontière de session | Des sessions poussées à 97 ou 98 % de contexte, avec des lots sautés |
| 9. Décisions consultées | Des questions déjà tranchées rouvertes par l'agent dans au moins deux sessions |
| 10. Pas de fichiers produits dans git | Jusqu'à 96,1 % du poids du dépôt, et un volume de « code » mal compris de l'extérieur |
| 13. Un chiffre se calcule | 33 décisions annoncées au lieu de 27, 499 verdicts au lieu de 504, 11 traductions au lieu de 10 |
| 14. Retour arrière avant l'écriture | 21 % du budget et un tiers des défauts concentrés sur l'étape d'écriture |
| Plafond de taille | Trois fichiers entre 5 400 et 7 600 lignes, les trois plus réécrits. Deux fichiers multipliés par 7 en 57 jours |
| Plafond tous langages | Une page HTML de 2 612 lignes que la règle limitée au Python ne voyait pas |
| La ligne de commande n'orchestre pas | Une fonction principale de 1 285 puis 1 768 lignes, avec un défaut de commit caché dedans |
| Fichier de règles court | Un fichier de règles de 1 306 lignes et 26 000 tokens lu par 46 prompts sur 70. Un chantier ouvrait 80 000 tokens de contexte avant de commencer |
| Règle devenue test ou hook | Sur six formes de défaut déclarées, trois sans garde-fou, dont une revenue quatre fois. Une règle « ne jamais committer » écrite en prose, ignorée par une session lancée avant son ajout |
| Un worktree par session | Des lignes indexées par une session emportées dans le commit d'une autre, et un hook activé sans validation, dans le même dossier partagé |
| Contrôle de la taille du diff | Une réécriture de fichier en diff de 1 287 lignes, des fins de ligne converties par erreur |
| Recalibrer l'estimation | Ratio réel sur estimé médian de 1,70, 88 % de dépassements sur 119 points |
| Arrêts tous les 30 points | Les indicateurs viraient au rouge vers le point 150, le ralentissement n'a été ressenti que vers le point 230 |
| Environnement réglé au jour 0 | Au moins quatre sessions réussies arrêtées au dernier envoi, faute de connexion au dépôt distant |
| Relecteur distinct de l'auteur | Ailleurs : sur sept projets vibe codés étudiés, une suite de tests d'authentification au vert avec un login cassé |
| Secrets et entrées | Ailleurs : 970 vulnérabilités sur sept projets vibe codés, dont plus de 70 % en chemins, secrets en dur et entrées non validées |

## Sources

- [Best practices for Claude Code, documentation officielle](https://code.claude.com/docs/en/best-practices)
- [AGENTS.md, format ouvert](https://agents.md/)
- [Spec-driven development, Microsoft for Developers](https://developer.microsoft.com/blog/spec-driven-development-ai-native-engineering/)
- [Vibe Coding in Practice: Flow, Technical Debt (arXiv 2512.11922)](https://arxiv.org/pdf/2512.11922)
- [Lecture du rapport DORA 2026](https://ingenire.com/blog/dora-2026-ai-amplifier)
- [Design Tokens Community Group](https://github.com/design-tokens/community-group)
