#!/usr/bin/env bash
# Teste modele/verifier dans un projet jetable tiré de modele/, en CI simulée (CI=true).
#   outils/tester_verifier.sh [bash à tester]   (défaut : bash ; sous macOS, /bin/bash est le 3.2)
# Contrôles, pour chaque mode (complet, fusion, rapide, rapide sans fichier indexé) : code 0 ;
# le test ordinaire tourne ; le test nommé dans tests/locaux.txt, qui échouerait, est sauté.
# Code 0 si tout passe, 1 sinon. Compatible avec le bash 3.2 de macOS.
set -u
bash_teste=${1:-bash}
depot=$(cd "$(dirname "$0")/.." && pwd)
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT
projet=$tmp/projet
cp -R "$depot/modele" "$projet"
cd "$projet" || exit 2
# Faux node, en tête du PATH : il note les tests reçus et échoue si on lui passe le test local.
# Ce qui est testé, c'est le tri des tests par ./verifier, pas node.
mkdir -p "$tmp/bin"
printf '#!/bin/sh\necho "$*" >> "%s/node.log"\ncase "$*" in *local.test.mjs*) exit 1 ;; esac\n' "$tmp" > "$tmp/bin/node"
chmod +x "$tmp/bin/node"
export PATH="$tmp/bin:$PATH"
mkdir -p tests
printf "import test from 'node:test';\ntest('ordinaire', () => {});\n" > tests/ordinaire.test.mjs
printf "import test from 'node:test';\ntest('local', () => { throw new Error('lancé en CI'); });\n" > tests/local.test.mjs
printf '# données locales\ntests/local.test.mjs\n' > tests/locaux.txt
git init -q -b main
git add -A
git -c user.name=essai -c user.email=essai -c commit.gpgsign=false commit -qm essai
export CI=true
"$bash_teste" -c 'echo "bash testé : $BASH_VERSION"'

echecs=0
verifie() { # message, puis la commande
  local msg=$1; shift
  if "$@"; then echo "  OK     $msg"; else echo "  ÉCHEC  $msg"; echecs=$((echecs + 1)); fi
}
lancer() { # nom du mode, puis les arguments de ./verifier
  local nom=$1; shift
  "$bash_teste" ./verifier "$@" > "$tmp/$nom.txt" 2>&1
  local code=$?
  verifie "$nom : code 0" test "$code" = 0
  [ "$code" = 0 ] || sed 's/^/         /' "$tmp/$nom.txt"
}
contient() { grep -qF -- "$2" "$tmp/$1.txt"; }

echo "== Complet"
lancer complet
verifie "complet : 1 test lancé" contient complet "1 fichier(s) de test"
verifie "complet : test local sauté" contient complet "sautés en CI (tests/locaux.txt) : 1"

echo "== Fusion"
lancer fusion --fusion
verifie "fusion : 1 test lancé" contient fusion "1 fichier(s) de test"

echo "== Rapide, un test modifié"
echo "// modifié" >> tests/ordinaire.test.mjs
git add tests/ordinaire.test.mjs
lancer rapide --rapide
verifie "rapide : 1 test lancé" contient rapide "1 fichier(s) de test"

echo "== Rapide, rien d'indexé"
git reset -q
lancer rapide-vide --rapide
verifie "rapide-vide : aucun test" contient rapide-vide "aucun test à lancer"

echo "== Tests reçus par node"
verifie "ordinaire.test.mjs reçu 3 fois" test "$(grep -c 'ordinaire.test.mjs' "$tmp/node.log")" = 3
verifie "local.test.mjs jamais reçu" test "$(grep -c 'local.test.mjs' "$tmp/node.log")" = 0

echo "== Résultat : $echecs échec(s)"
[ "$echecs" -eq 0 ]
