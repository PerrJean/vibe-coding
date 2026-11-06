#!/usr/bin/env bash
# Installe les règles, skills et hooks communs dans ~/.claude (macOS, Linux, WSL).
# Relie ~/.claude à ce dépôt pour qu'un git pull suffise à mettre à jour : un lien symbolique
# par skill, un pour le dossier des hooks (s'il ne porte que des hooks de global/hooks).
# CLAUDE.md est copié, pas relié : sa section Environnement est propre au poste.
# Déplacer le dépôt casse les liens : relancer alors l'installateur.
# Même comportement que installer.ps1 :
#   ./global/installer.sh --simulation   montre ce qui serait fait
#   ./global/installer.sh                installe, après sauvegarde de ce qui est remplacé
#   ./global/installer.sh --remplacer    remplace aussi un CLAUDE.md existant (sauvegardé)
set -eu
source_dir=$(cd "$(dirname "$0")" && pwd)
dest=${CLAUDE_DIR:-$HOME/.claude}
simulation=0; remplacer=0
for a in "$@"; do
  case $a in --simulation) simulation=1 ;; --remplacer) remplacer=1 ;; *) echo "option inconnue : $a"; exit 2 ;; esac
done
sauvegarde="$dest/sauvegardes/vibe-coding-$(date +%Y%m%d-%H%M%S)"
n=2; base=$sauvegarde; while [ -e "$sauvegarde" ]; do sauvegarde="$base-$n"; n=$((n + 1)); done

agir() { # message, puis la commande
  msg=$1; shift
  if [ $simulation = 1 ]; then echo "[simulation] $msg"; else echo "$msg"; "$@"; fi
}
sauvegarder() {
  [ -e "$1" ] || return 0
  rel=${1#"$dest"/}
  agir "Sauvegarde : $rel" sh -c 'mkdir -p "$(dirname "$2")" && cp -R "$1" "$2"' _ "$1" "$sauvegarde/$rel"
}
relie_vers() { [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]; }
lier() { # cible, source, nom
  if relie_vers "$1" "$2"; then echo "Déjà relié : $3"; return 0; fi
  sauvegarder "$1"
  # rm -rf sur un lien sans / final retire le lien seul, jamais ce qu'il vise.
  agir "Lien : $3 -> $2" sh -c 'rm -rf "$1" && mkdir -p "$(dirname "$1")" && ln -s "$2" "$1"' _ "$1" "$2"
}
refus=0

[ $simulation = 1 ] || mkdir -p "$dest"

if [ -e "$dest/CLAUDE.md" ] && [ $remplacer = 0 ]; then
  agir "CLAUDE.md existe déjà : modèle posé à côté, $dest/CLAUDE.vibe-coding.md. Fusionner à la main." \
    cp "$source_dir/CLAUDE.md" "$dest/CLAUDE.vibe-coding.md"
else
  sauvegarder "$dest/CLAUDE.md"
  agir "CLAUDE.md installé. Remplir la section Environnement." cp "$source_dir/CLAUDE.md" "$dest/CLAUDE.md"
fi

if [ -d "$source_dir/skills" ]; then
  for s in "$source_dir"/skills/*/; do
    [ -d "$s" ] || continue
    nom=$(basename "$s")
    lier "$dest/skills/$nom" "${s%/}" "skills/$nom"
  done
fi

if [ -d "$source_dir/hooks" ]; then
  cible="$dest/hooks"; autres=""
  if [ -d "$cible" ] && ! relie_vers "$cible" "$source_dir/hooks"; then
    for f in "$cible"/* "$cible"/.[!.]*; do
      [ -e "$f" ] || continue
      nom=$(basename "$f")
      [ "$nom" = __pycache__ ] || [ -e "$source_dir/hooks/$nom" ] || autres="$autres $nom"
    done
  fi
  if [ -n "$autres" ]; then
    echo "REFUS : $cible contient des fichiers absents de global/hooks :$autres. Les déplacer, puis relancer."
    refus=1
  else
    lier "$cible" "$source_dir/hooks" hooks
  fi
  # Déclaration dans settings.json, avec la commande Python de macOS et Linux : python3.
  if [ $simulation = 1 ]; then
    python3 "$source_dir/declarer_hooks.py" "$dest" python3 --simulation
  else
    python3 "$source_dir/declarer_hooks.py" "$dest" python3
  fi
fi

if [ $simulation = 0 ] && [ -d "$sauvegarde" ]; then echo "Anciennes versions sauvegardées dans $sauvegarde"; fi
exit $refus
