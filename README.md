# Les commandements d'un projet vibe codé

*Version 4.1, mise à jour le 5 novembre 2026.*

Ce guide s'adresse à toute personne qui fait écrire du code par un agent d'IA (Claude Code, Cursor, Codex ou un autre) sans être développeur. Il tient en quatorze règles, chacune avec son pourquoi.

Il vient de la pratique : le retour d'expérience d'un premier projet vibe codé, la relecture d'un développeur, deux mois de rapports d'usage, et l'audit qualité de trois projets. Le premier projet, écrit avant ces règles, est gonflé : une fonction de 1 768 lignes, 33 fichiers de plus de 800 lignes. Les deux suivants, écrits en les appliquant, ne le sont pas : aucun fichier de code au-delà de 500 lignes, une duplication sous 1 %. Les règles marchent quand elles sont appliquées dès le premier jour.

## Comment lire ce dépôt

| Fichier | Pour qui | Quand |
| --- | --- | --- |
| Ce README | Tout le monde | Avant le premier projet |
| [POUR-ALLER-PLUS-LOIN.md](POUR-ALLER-PLUS-LOIN.md) | Qui a un projet qui grossit, dure ou doit être repris | Après quelques semaines |
| [modele/](modele/) | L'agent | À copier au jour 0 : règles courtes, contrôles déjà branchés |
| [global/](global/) | L'agent, dans tous les projets | Skills et hooks communs, à installer une fois |
| [LEXIQUE.md](LEXIQUE.md) | Tout le monde | Quand un mot technique bloque |
| [ANNEXE.md](ANNEXE.md) | Qui veut savoir d'où vient une règle | Les chiffres qui justifient chaque règle |

Le pourquoi sert l'humain et coûte du contexte à l'agent. Il reste donc dans ces pages, pas dans les fichiers que l'agent lit.

Les pratiques qui n'ont pas encore marché dans deux projets sont rangées à part, dans la section [À tester](POUR-ALLER-PLUS-LOIN.md#g-à-tester) : chacune y dit ce qu'on en attend et comment on le mesure. Les règles de ce README y renvoient quand elles en ont une.

## Le socle

### Avant de coder

**1. Fais-toi interviewer, puis fais écrire la spec.** Demande à l'agent de te questionner sur le besoin, les cas limites et ce qui est hors périmètre, puis d'écrire la spec dans un fichier. Ensuite, une session neuve pour coder, avec la spec en référence.
*Pourquoi : personne ne spécifie seul un domaine qu'il découvre. L'entretien fait remonter ce que tu ne savais pas devoir décider.*
À tester : demander ce qui fait déjà l'essentiel du besoin ([partir de l'existant](POUR-ALLER-PLUS-LOIN.md#partir-de-lexistant)).

**2. Écris le contrat : ce qui entre, ce qui sort, ce qui est hors périmètre.** S'il dépasse une centaine de lignes, découpe le projet en plusieurs outils qui se passent des fichiers.
*Pourquoi : c'est la référence qui permet de dire non à l'agent quand il élargit le sujet.*

**3. Décide dès le départ : outil personnel, ou outil à faire reprendre.** S'il doit être repris, nomme qui le reprendra et prends son langage. Sinon, prends le langage le plus adapté au problème.
*Pourquoi : un outil écrit dans le mauvais langage pour sa destination se réécrit au moment de la reprise.*
À tester : choisir aussi son niveau de contrôle, builder, éditeur ou agent ([choisir son niveau de contrôle](POUR-ALLER-PLUS-LOIN.md#choisir-son-niveau-de-contrôle)).

### Les premiers jours

**4. Ouvre git au premier fichier, et committe après chaque étape qui marche.**
*Pourquoi : c'est ton bouton « annuler » quand l'agent casse quelque chose, et ce qui rend le travail mesurable.*

**5. Le premier jour, un circuit complet qui tourne.** La plus petite version qui lit une vraie donnée, produit une vraie sortie et a un test vert. Ce circuit est concret et propre au premier cas : pas de couches, pas d'interfaces, pas de configuration générique. Ensuite, on l'épaissit cas réel par cas réel, sans jamais le casser, et on ne généralise qu'au deuxième cas (règle 7).
*Pourquoi : construire les morceaux un par un et les assembler à la fin fait arriver tous les problèmes ensemble, et tard. Concevoir l'architecture d'avance revient au même : on la bâtit pour des cas qu'on n'a pas encore vus.*
À tester : partir du gabarit officiel d'un framework ou d'un projet existant ([partir de l'existant](POUR-ALLER-PLUS-LOIN.md#partir-de-lexistant)). La skill [chercher-l-existant](global/skills/chercher-l-existant/SKILL.md) fait la recherche et vérifie les candidats.

**6. Lis la donnée avant de la supposer.** Fais afficher vingt enregistrements réels avant de concevoir. Ce que la donnée ne tranche pas est une question pour toi, notée comme telle, jamais une hypothèse de l'agent.
*Pourquoi : un nom de champ supposé au lieu d'être lu coûte des journées.*

**7. Les valeurs hors du code dès le premier cas, la logique simple jusqu'au deuxième.** Un identifiant, un client ou un seuil va dans une table de référence. La logique, elle, reste spécifique au premier cas : on ne la généralise qu'au deuxième cas réel.
*Pourquoi : une valeur en dur se recopie partout. Une abstraction bâtie sur un seul cas se trompe sur le suivant.*
À tester : ce qui ne te différencie pas ne se code pas ([partir de l'existant](POUR-ALLER-PLUS-LOIN.md#partir-de-lexistant)).

### Au quotidien

**8. Un prompt, une tâche. Une session se termine sur un commit et une note de passation.**
*Pourquoi : changer de session réduit le coût du contexte. La note évite que la session suivante redécouvre ce que la précédente savait.*

**9. Ce qui est décidé vit dans un fichier, et l'agent le consulte avant de te poser une question.**
*Pourquoi : une décision qui ne vit que dans une conversation est perdue à la suivante, et l'agent rouvre des questions déjà tranchées.*

**10. Le dépôt contient du code. Ni secret, ni données produites, ni fichiers générés jetables.** Les mots de passe restent dans un fichier local jamais envoyé. Les sorties de l'outil vont dans un dossier exclu de git. Un fichier généré qui est livré (une image servie par un site, par exemple) peut être versionné, s'il est déclaré comme tel.
*Pourquoi : dans les projets audités, les fichiers produits pesaient jusqu'à 96 % du dépôt, et faussaient toute mesure du code.*

### Vérifier

**11. Donne à l'agent de quoi vérifier son travail, en une seule commande.** Des tests, et la même commande pour toi, pour l'agent et pour le contrôle automatique avant chaque commit.
*Pourquoi : sans cela, « ça a l'air fini » est le seul signal, et c'est toi qui fais toute la vérification.*

**12. Le relecteur n'est pas l'auteur.** La revue se fait dans une session neuve, qui ne voit que le résultat et les critères. Celui qui écrit le code n'écrit pas les tests qui le valident.
*Pourquoi : un agent qui relit son propre travail le trouve juste.*

**13. Exige la preuve. Un chiffre se calcule, il ne se tape pas.** La sortie du test, la commande et son résultat. Tout compte cité dans un commit, un résumé ou un message sort d'une commande.
*Pourquoi : un agent annonce de bonne foi 33 décisions quand il y en a 27.*

**14. Si l'outil écrit quelque part, le retour arrière est construit avant l'écriture.** D'abord le registre de ce qui sera écrit, puis un retour arrière testé, puis l'écriture.
*Pourquoi : l'écriture est l'étape où une erreur coûte le plus cher et se répare le plus difficilement.*

## Le jour 0, en une heure

1. **Vérifier l'environnement** : git, connexion au dépôt distant, langage, shell. Ce qui manque se règle maintenant, pas au premier envoi.
2. **Copier le dossier [modele/](modele/)**, puis activer ses hooks avec `git config core.hooksPath .githooks` et les déclarer exécutables avec `git add --chmod=+x .githooks/pre-commit .githooks/pre-merge-commit .githooks/pre-push`. Sans cette dernière commande, le premier commit est refusé sous Windows. Git, le fichier de règles, les contrôles avant commit et l'exclusion des fichiers produits sont alors en place.
3. **Décider : personnel ou à reprendre**, et choisir le langage en conséquence (règle 3). À tester : trancher aussi les décisions irréversibles ([la liste](POUR-ALLER-PLUS-LOIN.md#décisions-irréversibles-et-seuils-dexposition)).
4. **L'interview, puis SPEC.md.** Phrase de départ : « Interviewe-moi sur ce besoin jusqu'à épuisement, puis écris la spec. »
5. **CONTRAT.md**, une centaine de lignes au plus.
6. **Le circuit complet** : une vraie donnée lue, une vraie sortie, un test vert, committé.
7. **Trois tests qui échouent** sur les comportements centraux, et les questions ouvertes notées comme arbitrages à rendre.
8. **Le registre** ouvert dès la première décision.

## Les quatre questions à se reposer chaque mois

1. Le contrat tient-il toujours en une centaine de lignes ?
2. Un changement typique demande-t-il de comprendre un seul fichier ?
3. Puis-je vérifier le résultat sans lire le code ?
4. Le dépôt contient-il surtout du code, et pas des fichiers produits ?

Deux non sur quatre : le projet a changé de régime. Découper, ou le faire auditer (voir [POUR-ALLER-PLUS-LOIN.md](POUR-ALLER-PLUS-LOIN.md)), avant de continuer.

## Historique et licence

Les versions précédentes et ce qui a changé sont dans [CHANGELOG.md](CHANGELOG.md).

Les textes (ce README, les guides, le lexique, l'annexe) sont sous licence [CC BY 4.0](LICENSE-TEXTES) : tu peux les reprendre et les adapter, y compris en entreprise, en citant l'auteur. Le code (les dossiers `modele/`, `global/` et `outils/` : hooks, scripts, skills) est sous licence [MIT](LICENSE).
