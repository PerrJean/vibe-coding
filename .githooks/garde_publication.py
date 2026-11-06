"""Garde de publication du dépôt public : rien de personnel n'y entre.

    python .githooks/garde_publication.py --index    le contenu indexé (pre-commit)
    python .githooks/garde_publication.py --disque   les fichiers suivis, sur le disque

Refuse un fichier qui contient :
  - un secret (clé d'API, jeton, clé privée) ;
  - un chemin personnel (dossier d'utilisateur Windows, macOS ou Linux) ;
  - une adresse e-mail ;
  - un nom propre : le nom de l'auteur ailleurs que dans LICENSE, ou un terme
    des listes privées.
Refuse aussi tout hook de .githooks/ ou modele/.githooks/ (fichier sans
extension) qui n'est pas en 100755 dans l'index : il ne s'exécuterait pas
après un clone sous Linux ou macOS.

Les listes privées vivent hors du dépôt : la publier publierait ce qu'elle
protège. Leurs chemins se déclarent dans la configuration LOCALE de git, une
ligne par liste :

    git config --add vibe.listes <chemin de la liste>

Un terme par ligne, # pour un commentaire, comparé sans casse et en mot entier.
Aucune liste déclarée, ou une liste absente ou vide : refus, le contrôle ne se
tait jamais. Les messages nomment le fichier et la règle, jamais le terme.
Les chemins sont lus dans git, jamais reçus en argument. Un échec de git refuse.
"""
import re
import subprocess
import sys
from pathlib import Path

# Les motifs sont écrits pour ne pas se reconnaître eux-mêmes : ce fichier est
# publié et passe par la même garde.
SECRETS = re.compile(
    r"sk-ant-[A-Za-z0-9_-]{10,}|AIza[0-9A-Za-z_-]{20,}|gh[pousr]_[A-Za-z0-9]{20,}"
    r"|AKIA[0-9A-Z]{16}|xox[abprs]-[A-Za-z0-9-]{10,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
CHEMINS = re.compile(r"[A-Za-z]:[\\/]+Users[\\/]|/(?:home|Users)/[A-Za-z0-9._-]")
EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}")
LICENCE = "LICENSE"
DOSSIERS_HOOKS = (".githooks", "modele/.githooks")


def git(*args):
    fini = subprocess.run(["git", *args], capture_output=True)
    if fini.returncode != 0:
        raise RuntimeError(f"git {args[0]} en échec (code {fini.returncode})")
    return fini.stdout


def mot_entier(termes):
    alternance = "|".join(re.escape(t) for t in termes)
    return re.compile(rf"(?<!\w)(?:{alternance})(?!\w)", re.IGNORECASE)


def termes_prives():
    """Les termes des listes déclarées dans `git config vibe.listes`."""
    try:
        chemins = git("config", "--get-all", "vibe.listes").decode("utf-8").split("\n")
    except RuntimeError:
        raise RuntimeError("aucune liste privée déclarée (git config --add vibe.listes <chemin>)")
    termes = []
    for brut in (c.strip() for c in chemins if c.strip()):
        chemin = Path(brut).expanduser()
        if not chemin.is_file():
            raise RuntimeError("une liste privée déclarée est absente")
        lignes = (l.strip() for l in chemin.read_text(encoding="utf-8-sig").splitlines())
        lus = [l for l in lignes if l and not l.startswith("#")]
        if not lus:
            raise RuntimeError("une liste privée déclarée est vide")
        termes += lus
    return termes


def nom_auteur(texte_licence):
    """Le nom qui suit « Copyright (c) <année> » dans LICENSE."""
    m = re.search(r"Copyright \(c\) \d{4}\s+(.+)", texte_licence)
    if not m:
        raise RuntimeError("LICENSE ne porte pas de ligne « Copyright (c) <année> <nom> »")
    return [m.group(1).strip()] + [mot for mot in m.group(1).split() if len(mot) > 2]


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


def hooks_hors_mode():
    """Les hooks (fichiers sans extension de DOSSIERS_HOOKS) qui ne sont pas en 100755 dans l'index."""
    sortie = git("ls-files", "-s", "-z", "--", *DOSSIERS_HOOKS)
    for entree in (e.decode("utf-8", "replace") for e in sortie.split(b"\0") if e):
        meta, chemin = entree.split("\t", 1)
        if meta.split()[0] != "100755" and "." not in chemin.rsplit("/", 1)[-1]:
            yield chemin


def main(argv):
    if argv not in (["--index"], ["--disque"]):
        print(__doc__)
        return 2
    fautes = []
    try:
        fautes += [(chemin, "hook hors du mode 100755 (git add --chmod=+x)") for chemin in hooks_hors_mode()]
        prives = mot_entier(termes_prives())
        licence = Path(git("rev-parse", "--show-toplevel").decode("utf-8").strip()) / LICENCE
        auteur = mot_entier(nom_auteur(licence.read_text(encoding="utf-8")))
        for chemin, texte in contenus(argv[0]):
            for regle, motif in (("secret", SECRETS), ("chemin personnel", CHEMINS),
                                 ("adresse e-mail", EMAIL), ("terme d'une liste privée", prives)):
                if motif.search(chemin) or motif.search(texte):
                    fautes.append((chemin, regle))
            if chemin != LICENCE and (auteur.search(chemin) or auteur.search(texte)):
                fautes.append((chemin, "nom de l'auteur hors de LICENSE"))
    except (OSError, RuntimeError) as e:
        print(f"REFUS : rien n'a été vérifié : {e}")
        return 1
    for chemin, regle in fautes:
        print(f"REFUS : {regle} dans {chemin}")
    return 1 if fautes else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
