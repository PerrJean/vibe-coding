"""Pose « Modèle vibe-coding <version> » en tête de chaque fichier suivi de modele/.

    python outils/estampiller_modele.py

La version est le premier titre « ## X.Y » de CHANGELOG.md. À relancer à chaque
nouvelle version : une ligne déjà posée est mise à jour, jamais dupliquée.
Place de la ligne : sous le titre d'un .md (après une ligne vide), en commentaire
« # » ailleurs, sous le shebang s'il y en a un. Les fichiers d'un projet qui
portent cette ligne sont ceux que la skill verification-prealable compare au modèle.
"""
import re
import subprocess
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
LIGNE = re.compile(r"^(# )?Modèle vibe-coding \S+$", re.IGNORECASE)


def version():
    texte = (RACINE / "CHANGELOG.md").read_text(encoding="utf-8")
    trouve = re.search(r"^## (\d+(?:\.\d+)*)", texte, re.MULTILINE)
    if not trouve:
        raise SystemExit("REFUS : aucun titre « ## X.Y » dans CHANGELOG.md")
    return trouve.group(1)


def estampiller(lignes, est_md, tampon):
    """Rend les lignes avec le tampon à sa place, posé ou mis à jour."""
    for i, ligne in enumerate(lignes[:5]):
        if LIGNE.match(ligne):
            lignes[i] = tampon if est_md else f"# {tampon}"
            return lignes
    if est_md:
        if lignes and lignes[0].startswith("# "):
            return lignes[:1] + ["", tampon] + lignes[1:]
        return [tampon, ""] + lignes
    debut = 1 if lignes and lignes[0].startswith("#!") else 0
    return lignes[:debut] + [f"# {tampon}"] + lignes[debut:]


def main():
    tampon = f"Modèle vibe-coding {version()}"
    suivis = subprocess.run(["git", "-C", str(RACINE), "ls-files", "-z", "modele/"],
                            capture_output=True, check=True).stdout.decode("utf-8")
    changes = 0
    for chemin in (c for c in suivis.split("\0") if c):
        fichier = RACINE / chemin
        texte = fichier.read_text(encoding="utf-8")
        avant = texte.split("\n")
        apres = estampiller(list(avant), chemin.endswith(".md"), tampon)
        if apres != avant:
            fichier.write_text("\n".join(apres), encoding="utf-8", newline="\n")
            print(f"estampillé : {chemin}")
            changes += 1
    print(f"{tampon} : {changes} fichier(s) modifié(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
