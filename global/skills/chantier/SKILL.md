---
name: chantier
description: Dérouler de bout en bout un chantier du registre du projet courant, de sa fiche à sa clôture, à partir de son identifiant. À charger quand l'utilisateur demande « /chantier <id> », « fais le chantier <id> » ou « lance <id> ».
argument-hint: <identifiant du chantier>
---

# Chantier $ARGUMENTS

Les règles du projet priment sur cette skill. Avant tout, repérer dans le `CLAUDE.md` du projet, et dans `PASSATION.md` s'il existe :
- le **registre** : où vivent les fiches ouvertes et closes (parfois une archive figée en plus du registre vivant : lire les deux), et la forme d'une fiche, `registre/0000-convention.md` s'il existe ;
- la **commande de vérification** complète ;
- la **façon de clore** : commande, champs, d'où vient le coût réel ;
- les règles de **délégation** (qui code, fichier de prompt, modèles, chantiers simultanés) et de **git** (commit, push).
Ce qui manque se demande à l'utilisateur, rien ne s'invente. Un format se recopie d'une fiche close récente, jamais de mémoire.

## Déroulé
1. **Lire** `PASSATION.md`, la fiche $ARGUMENTS et deux fiches closes récentes. Fiche introuvable ou déjà close : s'arrêter et le dire.
1 bis. **Isoler** : créer la branche `chantier/<id>` dans un worktree à part (`git worktree add <chemin> -b chantier/<id>`) et y faire tout le travail ; chaque prompt de sous-agent donne ce chemin. Les fichiers ignorés par git n'y sont pas : si le code ou la vérification en ont besoin, demander à l'utilisateur, ne rien copier d'office. Puis, dans le worktree, jouer la commande de vérification complète et noter dans la fiche l'état de référence, vert ou rouge par test : les étapes 8 et 9 s'y comparent, dans ce même worktree.
2. **Le tranché** : chercher dans le registre (ouvert et clos), les décisions et `PASSATION.md` ce qui est déjà décidé. Une question tranchée n'est jamais présentée comme ouverte ; une règle marquée obsolète, remplacée ou écartée n'est jamais appliquée.
3. **Les questions ouvertes**, et elles seules, en un seul questionnaire. Reporter les réponses dans la section `## Tranché` de la fiche, datées et attribuées à l'utilisateur.
4. **La spec** : si la fiche ne pointe pas une spec avec ses critères d'acceptation, la faire écrire par un sous-agent au format du projet, puis la faire valider par l'utilisateur.
5. **Les tests d'abord** : un sous-agent écrit un test qui échoue par critère. Les jouer : chaque échec doit venir du comportement absent, jamais d'un import, d'un nom ou d'un fichier manquant. Sinon, renvoyer.
6. **Le code** : un autre sous-agent code jusqu'au vert. Il ne touche pas aux tests ; s'il doit le faire, il dit lequel et pourquoi, et le rapporter à l'utilisateur.
7. **La revue** : un sous-agent neuf, qui n'a vu ni tests ni code s'écrire, lit le diff contre la spec et rend PASSE ou NE PASSE PAS, avec la liste des problèmes. Il casse aussi le code de deux ou trois façons, puis le rétablit : une cassure qu'aucun test ne voit rougir est un problème de la liste. NE PASSE PAS : retour au codeur, trois tours au plus, puis s'arrêter et exposer à l'utilisateur ce qui reste.
8. **Vérifier** : jouer la commande de vérification complète et la comparer à l'état de référence de l'étape 1 bis, pour savoir quels rouges sont les siens. Tout chiffre donné (tests, verdicts, lignes, coût) sort d'une commande ou du harnais, et la commande l'accompagne.
9. **Committer** sur la branche les seuls fichiers du chantier (`git add <fichiers>`, jamais `-A` ; un nouveau script suit la règle du bit exécutable du `CLAUDE.md`), contrôler `git diff --cached --stat` avant, l'identifiant dans le message. Avant la fusion, jouer la vérification complète dans le worktree. Un rouge absent de l'état de référence : ne pas fusionner, retour à l'étape 6. Vert : `git merge --no-ff chantier/<id>` dans la branche principale, pour que les hooks jouent, puis `git worktree remove <chemin>` et `git branch -d chantier/<id>`. Pousser selon la règle du projet ; si l'authentification échoue, donner la commande exacte (`git push origin <branche>`) sans réessayer.
10. **Clore** par la voie du projet, selon `registre/0000-convention.md` s'il existe : `statut` à `clos AAAA-MM-JJ`, coût réel relevé au harnais, nature, étape, modèle. Montrer à l'utilisateur la fiche close et le commit, avec le nombre de tests, le nombre de tours de revue et toute décision prise hors spec. Puis lancer la skill `passation`.

## Modèles (à l'essai)
Le CLAUDE.md global déclare un modèle de plan et un modèle d'exécution. S'il n'en déclare pas, tout se fait avec le modèle courant.
- Modèle de plan : la spec (étape 4) et la revue (étape 7).
- Modèle d'exécution : les tests (étape 5) et le code (étape 6). Son prompt contient le plan en entier : il ne voit rien d'autre.
- Remontée : l'exécutant échoue deux fois, ou s'écarte du plan, ou découvre une question que le plan ne tranche pas : retour au modèle de plan, qui complète le plan.
- Petite correction (un fichier, quelques lignes) : pas de relais, le modèle courant la fait.
- À la clôture, le champ modele liste les modèles utilisés, et la fiche note le nombre de remontées.

## Garde-fous
- Avant chaque sous-agent : committer un point d'étape sur la branche du chantier ; nommer dans son prompt les fichiers qu'il ne touche pas ; interdire `git stash`, `checkout`, `reset`. Ne jamais utiliser `--no-verify`.
- Au-delà de 80 % de contexte : committer un point d'étape sur la branche, lancer `passation` en nommant l'étape où reprendre, et s'arrêter.
- Chaque prompt nomme la base sur laquelle mesurer, la plus petite qui suffise à la décision.
- Le coût d'un sous-agent se relève au harnais dès qu'il rend, jamais en le lui demandant ; la clôture en fait la somme.
- Un pas sauté ou non joué se dit ; rien n'est déclaré vert sans avoir été joué.
- Environnement : la section du `CLAUDE.md` global de l'utilisateur fait foi, ne pas la recopier ici.
