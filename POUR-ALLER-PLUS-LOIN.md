# Pour aller plus loin

À lire quand le projet dépasse quelques semaines, quelques milliers de lignes, ou qu'il doit être repris. Les termes techniques sont définis dans le [lexique](LEXIQUE.md), les chiffres cités dans l'[annexe](ANNEXE.md).

## A. La forme du code

Cinq principes d'architecture, issus de la pratique des développeurs :

- **Responsabilité unique.** Un fichier ou une fonction a une seule raison de changer. On sépare la récupération des données, les calculs et l'affichage.
- **Le métier au centre.** Les règles métier ne dépendent ni de la base, ni de l'API, ni de l'interface.
- **Les outils passés en paramètre.** Le code reçoit sa connexion, son client d'API et son horloge au lieu de les fabriquer. C'est ce qui permet de tester sans la vraie base et à date fixée.
- **Le plus simple qui marche (KISS, YAGNI).** Rien pour un besoin hypothétique.
- **Le vocabulaire du métier.** Les noms dans le code sont ceux du glossaire. Un mot absent du glossaire est une question à poser.

Un principe ne se vérifie pas, une limite chiffrée si. Les plafonds qui suivent ne sont donc pas des objectifs en soi : ce sont des détecteurs. Un fichier ou une fonction qui dépasse signale presque toujours un principe non respecté, le plus souvent la responsabilité unique. Quand un plafond saute, on ne se contente pas de couper : on cherche quel principe a lâché, et c'est lui qu'on corrige. Trois plafonds, contrôlés automatiquement avant chaque commit par le [modèle](modele/) :

- **Un fichier de code plafonne à 500 lignes, 800 en limite dure, quel que soit son langage.** HTML et JavaScript compris : dans un projet audité, une page de 2 612 lignes échappait à la règle parce qu'elle ne visait que le Python. Le fichier qui dépasse se scinde dans le chantier qui l'a fait dépasser, selon ses responsabilités (données, calculs, affichage), pas en tranches de 500 lignes.
- **Une fonction de plus de 80 lignes pose question.** Exceptions légitimes : une table de données littérale, un gabarit de rendu. Non négociable : la ligne de commande lit les arguments et appelle une fonction, elle n'orchestre pas.
- **Les règles valent pour tout le dépôt**, pas seulement pour le dossier principal. Dans les projets audités, la duplication se concentrait dans les scripts annexes : 16 % de lignes copiées dans des scripts d'images, une requête SQL recopiée entre deux fichiers.

Deux règles d'organisation :

- **Un artefact, un lecteur.** Un tableau de bord ou un rapport se découpe par question posée et par personne qui la pose, pas par taille.
- **Si le projet a une interface, il part d'un design system**, celui de l'organisation si possible. Chaque décision y porte sa raison, et un contrôle refuse une couleur ou un composant hors catalogue.

Et une règle d'économie : **avant d'écrire une fonction utilitaire, chercher si une bibliothèque le fait déjà.** Générer du HTML par concaténation de chaînes, par exemple, se remplace par un moteur de gabarits. À tester : où chercher d'abord, et sur quelles preuves choisir une dépendance ([partir de l'existant](#partir-de-lexistant)).

## B. Le contexte, qui est le vrai budget

- **Le fichier de règles plafonne à 300 lignes**, et s'imbrique par dossier (format AGENTS.md ou CLAUDE.md). Test par ligne : son retrait ferait-il faire une erreur ? Sinon, elle sort.
- **Ce qui ne sert que parfois devient une skill**, chargée à la demande. C'est le cas de la connaissance d'une base de données (tables, jointures, définitions validées), à partager entre projets plutôt qu'à reconstruire dans chacun.
- **Une skill se crée quand un même enchaînement de plusieurs étapes, aux conventions stables, a été refait au moins trois fois.** L'agent la propose en fin de tâche et ne l'écrit qu'après validation. Une dizaine de skills au plus, revues chaque trimestre : celle qui n'a pas servi depuis un mois, ou qu'on a dû corriger deux fois sur le même point, est mise à jour ou supprimée. Une skill commune à plusieurs projets ne cite aucun fichier en dur : elle découvre les conventions du projet courant au moment où elle s'exécute, et elle n'est terminée qu'après avoir marché dans deux projets.
- **Une règle vérifiable devient un test, une règle de processus devient un hook.** Ce qui reste en prose coûte du contexte à chaque session, pour toujours, et une session lancée avant son ajout l'ignore.
- **Une leçon vit dans son fichier, datée et mesurée.** On la lit pour changer une règle, pas pour agir.
- **Les dépendances sont déclarées.** Le contrat liste les tables et les fichiers que le projet lit et écrit, et un test vérifie que le code n'en touche pas d'autres.
- **Les fichiers tenus à la main restent petits.** Un fichier de correspondances de 413 Ko, modifié par 48 commits avec des lignes de plus de 5 000 caractères, doit être généré ou découpé.

## C. La vérification avancée

- **Un test donne le même résultat à chaque exécution.** Ni heure, ni ordre non spécifié, ni appel à un modèle : on fixe la date, on trie, on enregistre la réponse du modèle.
- **Un test qui reste vert quand on casse le code ne compte pas.** On casse volontairement le code de petites façons et on regarde si un test le détecte.
- **Les tests vivent à côté du code, et restent plus simples que lui.** Dans un projet audité, les tests intégrés aux fichiers de code occupaient 21,8 % des lignes, et les deux fonctions les plus complexes du dépôt étaient des tests.
- **Un contrôle se range selon sa durée** : quelques secondes au commit, une dizaine de minutes à la fusion, la liste complète à l'envoi. Un contrôle trop long à un moment fréquent finit désactivé.
- **L'agent travaille avec les droits minimum.** Lecture seule par défaut, écriture seulement à l'étape qui l'exige, jamais d'abord en production.
- **Les données personnelles, dès que le projet manipule des données réelles de personnes.** Structure réelle mais valeurs anonymisées dans les tests, rien dans git, rien dans les fichiers produits qui ne soit nécessaire. La taille du projet ne change rien : un prototype qui exporte des personnes est concerné.
- **Un audit qualité à intervalles réguliers**, avec un prompt fixe et en lecture seule : composition du dépôt, taille, complexité, duplication, code mort, survie du code. Le premier projet audité aurait dû s'arrêter bien plus tôt : ses signaux étaient mesurables. La skill [audit-qualite](global/skills/) le fait.

## D. Les sessions et le travail en parallèle

- **La frontière de session se prévoit.** Au-delà de 80 % de contexte, on termine : commit, note de passation, session neuve.
- **Une session qui écrit, un chantier, une copie du dépôt (worktree).** Deux sessions dans le même dossier partagent tout ce que git y garde : l'index, la configuration, les hooks actifs. Ce qu'elles partagent, chacune peut le modifier sans que les autres le sachent. Dans un projet audité, une session a emporté dans son commit les lignes qu'une autre venait d'indexer, et une troisième a activé un hook sans validation.
- **Une session ne défait pas le réglage d'une autre.** Elle le signale, et l'humain tranche.
- **Deux chantiers parallèles ne touchent pas les mêmes fichiers.** Sinon, on les enchaîne. On fusionne un chantier à la fois.
- **Aucun fichier modifié par toutes les sessions.** Un registre unique écrit à chaque commit devient le point de conflit garanti : un fichier par décision, sans index tenu à la main.
- **Les hooks utilisés par les worktrees sont committés.** Un worktree ne voit que ce qui est dans git : un hook modifié mais pas committé ne s'y applique pas.
- **À plusieurs** : une branche par chantier, et personne ne pousse directement sur la branche principale.

## E. La mesure et les arrêts

- **Un chantier s'inscrit avec son coût estimé et se clôt avec son coût réel.** Six champs : statut, coût estimé, coût réel, nature (chantier, défaut, arbitrage), étape, modèle. Le statut est explicite (ouvert, en cours, clos, écarté, remplacé), jamais déduit. Le coût réel se relève dans les compteurs de l'outil, jamais déclaré par l'agent.
- **On recalibre l'estimation tous les 30 points.**
- **On traite par lot borné**, et chaque exécution affiche le nombre d'éléments traités, sa durée et les lignes modifiées, avec un plafond par lot. La taille du code ne dit rien de la durée.
- **L'outil qui sert à faire l'outil a un budget**, plafonné à 15 %.
- **Tous les 30 points clos, cinq chiffres et un arrêt possible** : ratio réel sur estimé (seuil 2), part de défauts (seuil 30 %), taille du plus gros fichier (toute croissance continue), durée de l'exécution la plus lente, et part de lignes supprimées par ligne ajoutée. Ce dernier chiffre est le signal d'accumulation : dans le premier projet audité, on supprimait 0,23 ligne par ligne ajoutée.
- **Une skill se juge sur les erreurs évitées, pas sur les tokens.** On compare le coût réel et le nombre de corrections humaines sur cinq chantiers avant et cinq après.

## F. Les outils et l'environnement

- **L'environnement se règle au jour 0.** Connexion au dépôt distant, shell, droits d'installation : ce qui manque arrête la dernière étape d'une session réussie, pas la première. La skill [verification-prealable](global/skills/) le contrôle avant une passe longue.
- **Sous Windows**, un shell Linux (WSL2) évite la plupart des commandes qui échouent. À défaut, déclarer le shell dans le fichier de règles global pour que l'agent n'écrive pas de syntaxe incompatible.
- **Les outils Python de base** : uv pour les environnements, ruff pour le format et les erreurs simples, pre-commit pour les contrôles, un vérificateur de types. Aucun ne demande de droits d'administration.
- **Un fichier .gitattributes** fixe les fins de ligne une fois pour toutes.
- **Une intégration continue** relance la commande de vérification à chaque envoi.
- **Côté agent** : les skills pour les enchaînements répétés, les hooks pour les contrôles, les worktrees pour le parallèle, les environnements distants pour les passes longues, le bac à sable et le mode automatique pour les passes sans surveillance.
- **Le langage se choisit d'après la destination de l'outil** : celui de l'équipe qui le reprendra, ou à défaut le plus adapté au problème.

## G. À tester

Une pratique éprouvée a marché dans au moins deux projets, et sa preuve est dans l'[annexe](ANNEXE.md). Une pratique à tester dit ce qu'on en attend, comment on le mesure et sur quel projet elle sera essayée. Elle passe dans les règles quand elle a marché dans deux projets, et pas avant : une idée qui paraît juste n'a encore rien prouvé.

### Partir de l'existant

*À tester.*

Ce qui ne te différencie pas ne se code pas : un tableau de bord, une synchronisation ou un calcul standard viennent d'un outil ou d'une bibliothèque existante. Ce qui est propre au métier se code.

- À l'interview (règle 1), une question de plus : « Quels outils de l'organisation, produits ou projets open source font déjà l'essentiel de ce besoin ? »
- Le circuit du premier jour (règle 5) part du gabarit officiel d'un framework, ou d'un projet existant, quand il y en a un. Deux réserves : vérifier la licence, et ne pas partir d'un code mal fait, dont on hérite la dette.
- On cherche d'abord une bibliothèque là où l'erreur coûte cher : découpage (SQL, HTML), protection des caractères, validation d'un format. Une dépendance se choisit sur preuves : nom exact vérifié, maintenance, adoption, failles connues, licence, dépendances ajoutées.
- En fin de projet, demande à l'agent ce qu'une bibliothèque aurait remplacé, pour le savoir au projet suivant.

Première observation : l'audit d'un projet a relevé trois découpages de SQL faits à la main, et trois défauts déjà payés. C'est une observation dans un seul projet, pas encore une preuve.

- Attendu : moins de code écrit pour des besoins banals, et moins de défauts dans le découpage et la validation.
- Mesure : ce qu'une bibliothèque aurait remplacé, d'après la question de fin de projet, et les défauts du registre dans ces zones.
- Essai : le prochain projet démarré.

### Séparer le plan de l'exécution

*À l'essai dans la skill [chantier](global/skills/chantier/SKILL.md).*

Un modèle de plan écrit la spec et fait la revue. Un modèle d'exécution écrit les tests et le code, avec le plan pour seul contexte. Il rend la main au modèle de plan quand il échoue deux fois, s'écarte du plan ou tombe sur une question que le plan ne tranche pas. Une petite correction se fait sans relais.

- Attendu : un coût réel plus bas sans plus de défauts, et un plan assez complet pour que l'exécutant remonte rarement.
- Mesure : le coût réel, les défauts ouverts après la clôture et le nombre de remontées, notés dans chaque fiche du registre.
- Essai : les prochains chantiers menés avec la skill chantier.

### L'effort par étape

*Prévu, pas encore à l'essai.*

Un effort de raisonnement élevé pour la spec, le plan et la revue, normal pour les tests et le code.

- Attendu : moins de défauts, le surcoût restant sur les étapes qui décident.
- Mesure : le coût réel et les défauts du registre.
- Essai : après celui de la séparation du plan et de l'exécution, pour ne pas mesurer deux changements à la fois.
