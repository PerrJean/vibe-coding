---
name: passation
description: Fin de session dans n'importe quel projet : committer les seuls fichiers de cette session, puis mettre à jour PASSATION.md à la racine (fait, reste, décisions, prochaine commande) pour qu'une autre session reprenne. À charger quand l'utilisateur dit « passation », « on s'arrête », « prépare la reprise ».
---
# Passation de session

## 0. Lire les règles du projet courant
- Son `CLAUDE.md` : le registre des points s'il en nomme un, la section des fichiers à ne jamais committer, sa règle de commit et de push. Une règle absente se dit à l'utilisateur, elle ne s'invente pas.
- `git log -3` : le format réel des messages de commit.
- `PASSATION.md` s'il existe : son format fait foi. S'il est absent, le créer au format ci-dessous, et le dire.
- Si le dépôt de configuration personnelle déclaré dans le CLAUDE.md global a des écarts, le signaler.

## 1. Les fichiers de CETTE session
1. `git status --porcelain`. Ne retenir que les chemins que cette session a écrits (ses Edit/Write, les commandes qu'elle a lancées). Un fichier qu'elle n'a pas touché appartient à une autre session : le laisser.
2. Retirer ceux que le projet interdit (étape 0), et tout fichier non suivi que cette session n'a pas créé.
3. Pour un fichier partagé, `git diff -- <chemin>` : s'il porte aussi les changements d'une autre session, n'en committer que les passages (`@@`) de cette session. Garder ces passages du diff dans un correctif et le vérifier par `git apply --cached --check <correctif>` ; il s'applique à l'étape 3, jamais avant ; jamais de mode interactif. Si un passage mêle les lignes des deux sessions, s'arrêter et le montrer à l'utilisateur.
4. Montrer la liste. En cas de doute sur un fichier, demander au lieu de l'ajouter.

## 2. PASSATION.md
Relire le fichier juste avant d'écrire (d'autres sessions l'éditent). Une section par session : remplacer la seule section de cette session, garder les autres.

    ## AAAA-MM-JJ HH:MM — <sujet de la session>
    - Fait : commits (hash court + id du point s'il y en a), ce qui est publié.
    - Reste : par point du registre (id + son état tel qu'écrit), puis ce qui n'est pas inscrit.
    - Décisions de l'utilisateur : date, citation courte, où elle est inscrite.
    - Prochaine commande : UNE ligne exacte, copiable, calculée sur l'état réel au moment d'écrire (voir ci-dessous).
    - Ne pas committer : ce qui traîne dans l'arbre, et à qui c'est.

Chaque chiffre porte entre parenthèses la commande qui l'a produit, jouée pendant cette passation : `(git log -1)`, `(git status --porcelain)`. Sans commande, pas de chiffre.
Supprimer une section dont tout est committé et dont « Reste » est vide : git garde l'histoire.
La prochaine commande ne se recopie pas d'une passation précédente : jouer `git fetch` puis `git log '@{u}..HEAD' --oneline` (en PowerShell, `@{u}` entre guillemets) juste avant d'écrire. Des commits non poussés : la commande est le push, à valider par l'utilisateur. Aucun : la suivante vient du « Reste ». Une seconde fois après le commit de l'étape 3 : si la ligne écrite ne vaut plus, la corriger.

## 3. Commit
L'index est commun à toutes les sessions du dossier : une session qui committe sans nommer de chemins emporte tout ce qui y est indexé. Donc rien n'attend dans l'index. Message au format des commits relus à l'étape 0, écrit par Write dans le scratchpad, puis :
- fichiers entièrement à cette session et déjà suivis, `PASSATION.md` compris : `git commit -F <message> -- <chemins>` (prend le contenu du disque, laisse le reste de l'index) ;
- nouveau script, ou fichier dont le mode change : dans la MÊME commande, `git diff --cached --quiet` (index non vide : s'arrêter, ce n'est pas à cette session), puis `git add --chmod=+x -- <fichier>`, `git commit -F <message>` sans chemin, et `git ls-files -s <fichier>` doit afficher 100755 ;
- lignes seules d'un fichier partagé (étape 1.3) : dans la MÊME commande, `git diff --cached --quiet` (index non vide : s'arrêter, ce n'est pas à cette session), puis `git apply --cached <correctif>`, `git add -- <chemins seuls>` et `git commit -F <message>`.
Puis `git show --stat HEAD` : s'il ne porte pas exactement les fichiers attendus, s'arrêter et le montrer à l'utilisateur.
Pousser seulement si le projet le prescrit pour une passation ; sinon, le proposer à l'utilisateur.
Jamais `git add -A` ni `.`, ni `stash`, `restore`, `reset`, `checkout --`.
