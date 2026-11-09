---
name: chercher-l-existant
description: Avant de coder un composant, chercher ce qui existe déjà (outils de l'organisation, bibliothèques, projets open source, gabarits officiels) et vérifier ce qu'on retient. À charger quand l'utilisateur demande « cherche l'existant », « est-ce qu'une bibliothèque fait ça ? », ou pendant l'interview d'un nouveau projet.
---
# Chercher l'existant
1. **Le besoin** : reformuler en une phrase le composant cherché, et dire s'il est banal ou propre au métier. Propre au métier : le dire, et s'arrêter là.
2. **Chercher, dans cet ordre** : les outils déjà présents dans l'organisation (le CLAUDE.md du projet les liste), puis la bibliothèque standard du langage, puis les bibliothèques et projets open source, puis les gabarits officiels.
3. **Vérifier chaque candidat**, chiffres à l'appui et chaque chiffre avec sa source : le paquet existe sous ce nom exact, avec son éditeur et sa page officielle, sans confusion avec un nom proche ; dernière version et activité récente ; adoption (téléchargements, projets dépendants) ; failles connues (pip-audit, npm audit, base OSV) ; licence ; nombre de dépendances ajoutées. Un critère introuvable s'écrit « non trouvé », jamais estimé.
4. **Rendre** un tableau : candidats en lignes, critères en colonnes, puis une recommandation : utiliser, utiliser avec réserve, ou coder soi-même et pourquoi.
5. **Ne rien installer** : l'installation se fait dans un chantier, après validation de l'utilisateur, avec la version figée.
