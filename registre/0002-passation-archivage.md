# 0002 — Skill passation : étape « Archivage »

| nature | etape | statut | cout_estime | cout_reel | modele |
|---|---|---|---|---|---|
| `chantier` | `global` | `en cours` | 80 | | `claude-opus-5-5` |

## Demande

Une dernière étape, après la transmission, dit si la discussion peut être archivée. Elle
vérifie trois choses : le worktree est propre (`git status` vide, aucun commit absent de la
branche principale) ; l'envoi est fait comme le prévoit la section « Envoi » du CLAUDE.md du
projet, et sans cette section tout envoi demande une validation ; la passation est transmise
(discussion maître, registre ou PASSATION.md). Les trois remplies : une proposition d'archivage,
une fois, en une ligne. Sinon : une ligne sur ce qui manque. La discussion maître fait la même
vérification pour chacune de ses sous-discussions.

## Reste

- Faire marcher la skill modifiée dans deux projets avant de la dire terminée.

## Tranché

- 2026-11-09, l'auteur du dépôt : l'étape reste générique et courte ; `global/CLAUDE.md` reçoit
  la ligne « En fin de discussion, lancer passation, qui dit si la discussion peut être
  archivée. » ; ni fusion ni push sans sa validation.
