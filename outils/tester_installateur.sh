#!/usr/bin/env bash
# Teste global/installer.sh (macOS, Linux, WSL) dans un HOME jetable, jamais dans le vrai ~/.claude.
#   outils/tester_installateur.sh
# Contrôles : bit exécutable sur le disque ; la simulation n'écrit rien ; skills et hooks sont des
# liens vers le dépôt ; les hooks sont déclarés avec python3 et se lancent ; un deuxième passage
# ne change rien ; le contrôle de dérive (skill verification-prealable) retrouve le dépôt depuis le
# lien de la skill, et chaque fichier de modele/ porte la version du CHANGELOG.
# Code 0 si tout passe, 1 sinon. Compatible avec le bash 3.2 de macOS.
set -u
depot=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
export HOME="$tmp/home"
mkdir -p "$HOME"
claude=$HOME/.claude
echecs=0
verifie() { # message, puis la commande
  local msg=$1; shift
  if "$@"; then echo "  OK     $msg"; else echo "  ÉCHEC  $msg"; echecs=$((echecs + 1)); fi
}
installer() { "$depot/global/installer.sh" "$@" > "$tmp/sortie.txt" 2>&1; }

echo "== Bit exécutable"
executables_sans_x() { # fichiers en 100755 dans l'index, sans bit x sur le disque
  git -C "$depot" ls-files -s | awk '$1 == "100755" { sub(/^[^\t]*\t/, ""); print }' |
    while IFS= read -r f; do [ -x "$depot/$f" ] || echo "$f"; done
}
verifie "installer.sh en 100755" test "$(git -C "$depot" ls-files -s global/installer.sh | cut -c1-6)" = 100755
verifie "fichiers 100755 exécutables sur le disque" test -z "$(executables_sans_x)"

echo "== Simulation"
verifie "code 0" installer --simulation
verifie "rien d'écrit dans HOME" test ! -e "$claude"

echo "== Installation"
verifie "code 0" installer
lien_vers() { [ -L "$1" ] && [ "$(readlink "$1")" = "$2" ]; }
for s in "$depot"/global/skills/*/; do
  nom=$(basename "$s")
  verifie "lien skills/$nom" lien_vers "$claude/skills/$nom" "$depot/global/skills/$nom"
done
verifie "lien hooks" lien_vers "$claude/hooks" "$depot/global/hooks"
verifie "CLAUDE.md copié" test -f "$claude/CLAUDE.md"
verifie "2 hooks déclarés avec python3" test "$(grep -c '"python3 -I -S ' "$claude/settings.json")" = 2
verifie "aucun hook déclaré avec python" test "$(grep -c '"python -I' "$claude/settings.json")" = 0

echo "== Hooks garde-diff, lancés comme l'agent les lance"
cache=$HOME/.cache/garde-diff
echo bonjour > "$tmp/essai.txt"
appel="{\"tool_name\":\"Write\",\"tool_use_id\":\"essai1\",\"tool_input\":{\"file_path\":\"$tmp/essai.txt\"}}"
printf '%s' "$appel" | python3 -I -S "$claude/hooks/garde-diff-avant.py"
verifie "avant : copie posée" test -f "$cache/essai1_essai.txt.orig"
echo bonsoir >> "$tmp/essai.txt"
printf '%s' "$appel" | python3 -I -S "$claude/hooks/garde-diff-apres.py"
verifie "après : copie retirée" test ! -e "$cache/essai1_essai.txt.orig"
verifie "aucune erreur journalisée" test ! -e "$cache/erreurs.log"

echo "== Deuxième passage"
verifie "code 0" installer
verifie "rien de relié, sauvegardé ni installé" test -z "$(grep -E '^(Lien|Sauvegarde|CLAUDE.md installé)' "$tmp/sortie.txt")"
verifie "hooks déjà déclarés" grep -q 'Hooks déjà déclarés' "$tmp/sortie.txt"

echo "== Contrôle de dérive"
lien=$(readlink "$claude/skills/verification-prealable")
verifie "dépôt trois niveaux au-dessus du lien de la skill" test "$(cd "$lien/../../.." && pwd)" = "$depot"
version=$(grep -m1 -E '^## [0-9]' "$depot/CHANGELOG.md" | sed -E 's/^## ([0-9.]+).*/\1/')
sans_tampon=$(git -C "$depot" ls-files modele/ | while IFS= read -r f; do
  head -5 "$depot/$f" | grep -qE "^(# )?Modèle vibe-coding $version\$" || echo "$f"
done)
verifie "fichiers de modele/ estampillés $version" test -z "$sans_tampon"
[ -z "$sans_tampon" ] || printf '         %s\n' $sans_tampon

echo "== Résultat : $echecs échec(s)"
[ "$echecs" -eq 0 ]
