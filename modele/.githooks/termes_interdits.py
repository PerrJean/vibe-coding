# Modèle vibe-coding 4.1
"""Refuse les termes interdits, lus dans une liste hors du dépôt.

    <python> .githooks/termes_interdits.py <liste> --index [--auteur]
    <python> .githooks/termes_interdits.py <liste> --disque

La liste est hors du dépôt : la publier publierait ce qu'elle protège. Un terme
par ligne (nom d'employeur, de client, de projet interne...), # pour un
commentaire, comparé sans casse et en mot entier. Liste absente ou vide : refus,
le contrôle ne se tait jamais. Les messages nomment les fichiers, jamais les termes.

--index : le contenu indexé, celui qui entre dans le dépôt (pre-commit).
--disque : les fichiers suivis, tels qu'ils sont sur le disque.
--auteur : refuse aussi un auteur de commit dont le nom ou l'adresse contient un terme.
Les chemins sont lus dans git, jamais reçus en argument. Un échec de git refuse :
aucun fichier n'est sauté en silence.
"""
import re
import subprocess
import sys
from pathlib import Path


def git(*args):
    fini = subprocess.run(["git", *args], capture_output=True)
    if fini.returncode != 0:
        raise RuntimeError(f"git {args[0]} en échec (code {fini.returncode})")
    return fini.stdout


def lire_liste(chemin):
    if not chemin.is_file():
        return []
    lignes = (l.strip() for l in chemin.read_text(encoding="utf-8-sig").splitlines())
    return [l for l in lignes if l and not l.startswith("#")]


def motif(termes):
    alternance = "|".join(re.escape(t) for t in termes)
    return re.compile(rf"(?<!\w)(?:{alternance})(?!\w)", re.IGNORECASE)


def contenus(mode):
    """(chemin, texte) de chaque fichier à contrôler."""
    if mode == "--index":
        sortie = git("diff", "--cached", "--name-only", "-z", "--no-renames", "--diff-filter=ACMR")
    else:
        sortie = git("ls-files", "-z")
    for brut in (c for c in sortie.split(b"\0") if c):
        chemin = brut.decode("utf-8", "replace")
        if mode == "--index":
            octets = git("show", f":{chemin}")
        elif Path(chemin).is_file():
            octets = Path(chemin).read_bytes()
        else:
            continue  # suivi mais supprimé du disque
        yield chemin, octets.decode("utf-8", "ignore")


def main(argv):
    if len(argv) < 2 or argv[1] not in ("--index", "--disque") or argv[2:] not in ([], ["--auteur"]):
        print(__doc__)
        return 2
    liste = Path(argv[0]).expanduser()
    termes = lire_liste(liste)
    if not termes:
        print(f"REFUS : liste des termes interdits absente ou vide : {liste}")
        print("        Crée-la (un terme par ligne), ou vide LISTE_INTERDITS dans ./verifier pour désactiver ce contrôle.")
        return 1
    m = motif(termes)
    fautes = []
    try:
        for chemin, texte in contenus(argv[1]):
            if m.search(texte):
                fautes.append(chemin)
        if "--auteur" in argv and m.search(git("var", "GIT_AUTHOR_IDENT").decode("utf-8", "replace")):
            fautes.append("auteur du commit (git config user.name / user.email)")
    except (OSError, RuntimeError) as e:
        print(f"REFUS : lecture impossible, rien n'a été vérifié : {e}")
        return 1
    for chemin in fautes:
        print(f"REFUS : terme interdit dans {chemin}")
    if fautes:
        print(f"        Termes : voir {liste}, jamais affichés ici.")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
