"""Garde de publication du dépôt public : rien de personnel n'y entre.

    python .githooks/garde_publication.py --index    le contenu indexé (pre-commit)
    python .githooks/garde_publication.py --disque   les fichiers suivis, sur le disque
    python .githooks/garde_publication.py --message <fichier>   le message (commit-msg)
    python .githooks/garde_publication.py --plage <début>..<fin>   chaque commit (pre-push)

Refuse un fichier qui contient :
  - un secret (clé d'API, jeton, clé privée) ;
  - un chemin personnel (dossier d'utilisateur Windows, macOS ou Linux) ;
  - une adresse e-mail ;
  - un nom propre : le nom de l'auteur ailleurs que dans LICENSE, ou un terme
    des listes privées.
Refuse aussi tout hook de .githooks/ ou modele/.githooks/ (fichier sans
extension) qui n'est pas en 100755 dans l'index : il ne s'exécuterait pas
après un clone sous Linux ou macOS.

Avec --message, les mêmes règles s'appliquent au message de commit, sauf pour
deux adresses permises : l'adresse masquée GitHub et l'adresse noreply
d'Anthropic des lignes Co-Authored-By. L'auteur et le validateur du commit
(git var GIT_AUTHOR_IDENT, GIT_COMMITTER_IDENT) doivent porter une adresse
masquée GitHub.

Avec --plage, chaque commit de <début>..<fin> est contrôlé comme s'il était
créé : tout son arbre (règles de contenu et mode des hooks), son message et les
adresses de son auteur et de son validateur. La sortie nomme les commits en
faute. <fin> seul, ou un <début> fait de zéros (branche nouvelle) ou absent du
dépôt local, contrôle tout l'historique de <fin>. Une <fin> faite de zéros
(suppression de branche) n'a rien à contrôler.

Les listes privées vivent hors du dépôt : la publier publierait ce qu'elle
protège. Leurs chemins se déclarent dans la configuration LOCALE de git, une
ligne par liste :

    git config --add vibe.listes <chemin de la liste>

Un terme par ligne, # pour un commentaire, comparé sans casse et en mot entier.
Aucune liste déclarée, ou une liste absente ou vide : refus, le contrôle ne se
tait jamais. Les messages nomment le fichier et la règle, jamais le terme.
Les fichiers contrôlés sont lus dans git, jamais reçus en argument ; seuls le
fichier du message (hook commit-msg) et la plage (hook pre-push) arrivent en
argument, passés par git.
Un échec de git refuse.
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
NOREPLY_GITHUB = re.compile(r"(?:\d+\+)?[A-Za-z0-9-]+@users\.noreply\.github\.com")
ADRESSES_PERMISES = re.compile(
    rf"(?<![\w.%+-])(?:{NOREPLY_GITHUB.pattern}|noreply@anthropic\.com)(?![\w-]|\.\w)")
CISEAUX = "# ------------------------ >8 ------------------------"
ZEROS = re.compile(r"0+")
IDENTITES = (("author", "GIT_AUTHOR_IDENT", "l'identité d'auteur"),
             ("committer", "GIT_COMMITTER_IDENT", "l'identité de validateur"))


def git(*args, entree=None):
    fini = subprocess.run(["git", *args], input=entree, capture_output=True)
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


def fautes_fichiers(mode, regles, auteur):
    fautes = [(chemin, "hook hors du mode 100755 (git add --chmod=+x)") for chemin in hooks_hors_mode()]
    for chemin, texte in contenus(mode):
        for regle, motif in regles:
            if motif.search(chemin) or motif.search(texte):
                fautes.append((chemin, regle))
        if chemin != LICENCE and (auteur.search(chemin) or auteur.search(texte)):
            fautes.append((chemin, "nom de l'auteur hors de LICENSE"))
    return fautes


def fautes_texte_message(texte, regles, auteur):
    texte = ADRESSES_PERMISES.sub("", texte)
    fautes = [("le message", regle) for regle, motif in regles if motif.search(texte)]
    if auteur.search(texte):
        fautes.append(("le message", "nom de l'auteur hors de LICENSE"))
    return fautes


def faute_adresse(identite, qui):
    """Une faute si l'identité (« Nom <adresse> date ») n'a pas d'adresse masquée GitHub."""
    adresse = re.search(r"<([^>]*)>", identite or "")
    if not adresse or not NOREPLY_GITHUB.fullmatch(adresse.group(1)):
        return [(qui, "adresse non masquée (noreply GitHub obligatoire)")]
    return []


def fautes_message(fichier, regles, auteur):
    """Le message (jusqu'à la ligne de ciseaux de git commit -v), puis les deux identités."""
    texte = Path(fichier).read_text(encoding="utf-8", errors="ignore").split(CISEAUX)[0]
    fautes = fautes_texte_message(texte, regles, auteur)
    for _, variable, qui in IDENTITES:
        fautes += faute_adresse(git("var", variable).decode("utf-8", "replace"), qui)
    return fautes


def commits_de(plage):
    """Les commits de <début>..<fin>, du plus ancien au plus récent.

    <fin> seul, ou un <début> fait de zéros ou absent du dépôt : tout l'historique
    de <fin>. Une <fin> faite de zéros (suppression de branche) : aucun commit.
    """
    if "..." in plage:
        raise RuntimeError("plage à trois points : écrire <début>..<fin>")
    debut, separateur, fin = plage.rpartition("..")
    if ZEROS.fullmatch(fin):
        return []
    connu = subprocess.run(["git", "cat-file", "-e", f"{debut}^{{commit}}"],
                           capture_output=True).returncode == 0
    revision = f"{debut}..{fin}" if separateur and debut and not ZEROS.fullmatch(debut) and connu else fin
    return git("rev-list", "--reverse", revision, "--").decode("ascii").split()


def lire_objets(shas):
    """{sha: octets} des objets, lus en un seul appel à git cat-file --batch."""
    shas = list(dict.fromkeys(shas))
    sortie = git("cat-file", "--batch", entree="".join(f"{s}\n" for s in shas).encode("ascii"))
    objets, i = {}, 0
    for sha in shas:
        fin_entete = sortie.index(b"\n", i)
        entete = sortie[i:fin_entete].split()
        if len(entete) != 3:
            raise RuntimeError("objet introuvable dans le dépôt")
        debut = fin_entete + 1
        objets[sha] = sortie[debut:debut + int(entete[2])]
        i = debut + int(entete[2]) + 1
    return objets


def arbre(commit):
    """(mode, sha, chemin) de chaque fichier de l'arbre du commit (sous-modules exclus)."""
    entrees = []
    for brut in (e for e in git("ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0") if e):
        meta, chemin = brut.decode("utf-8", "replace").split("\t", 1)
        mode, genre, sha = meta.split()
        if genre == "blob":
            entrees.append((mode, sha, chemin))
    return entrees


def fautes_arbre(entrees, objets, regles, auteur, vus):
    """Les règles de contenu sur chaque fichier de l'arbre ; vus garde le verdict de chaque blob."""
    fautes = []
    for mode, sha, chemin in entrees:
        nom = chemin.rsplit("/", 1)[-1]
        if chemin.startswith(tuple(f"{d}/" for d in DOSSIERS_HOOKS)) and mode != "100755" and "." not in nom:
            fautes.append((chemin, "hook hors du mode 100755 (git add --chmod=+x)"))
        if sha not in vus:
            texte = objets[sha].decode("utf-8", "ignore")
            vus[sha] = ([r for r, motif in regles if motif.search(texte)], bool(auteur.search(texte)))
        touchees, nomme = vus[sha]
        touchees = dict.fromkeys(touchees + [r for r, motif in regles if motif.search(chemin)])
        fautes += [(chemin, regle) for regle in touchees]
        if chemin != LICENCE and (nomme or auteur.search(chemin)):
            fautes.append((chemin, "nom de l'auteur hors de LICENSE"))
    return fautes


def fautes_objet_commit(octets, regles, auteur):
    """Le message et les deux identités d'un objet commit."""
    entete, _, message = octets.decode("utf-8", "replace").partition("\n\n")
    champs = {}
    for ligne in entete.split("\n"):
        cle, _, valeur = ligne.partition(" ")
        champs.setdefault(cle, valeur)
    fautes = fautes_texte_message(message, regles, auteur)
    for cle, _, qui in IDENTITES:
        fautes += faute_adresse(champs.get(cle), qui)
    return fautes


def fautes_plage(commits, regles, auteur):
    """(commit court, endroit, règle) pour chaque faute des commits."""
    arbres = {c: arbre(c) for c in commits}
    objets = lire_objets(commits + [sha for a in arbres.values() for _, sha, _ in a])
    vus, fautes = {}, []
    for c in commits:
        for endroit, regle in (fautes_arbre(arbres[c], objets, regles, auteur, vus)
                               + fautes_objet_commit(objets[c], regles, auteur)):
            fautes.append((c[:10], endroit, regle))
    return fautes


def main(argv):
    if argv not in (["--index"], ["--disque"]) and not (
            len(argv) == 2 and argv[0] in ("--message", "--plage")):
        print(__doc__)
        return 2
    try:
        if argv[0] == "--plage":
            commits = commits_de(argv[1])
            if not commits:
                print("-> garde de publication : aucun commit à contrôler")
                return 0
        prives = mot_entier(termes_prives())
        licence = Path(git("rev-parse", "--show-toplevel").decode("utf-8").strip()) / LICENCE
        auteur = mot_entier(nom_auteur(licence.read_text(encoding="utf-8")))
        regles = (("secret", SECRETS), ("chemin personnel", CHEMINS),
                  ("adresse e-mail", EMAIL), ("terme d'une liste privée", prives))
        if argv[0] == "--plage":
            return rapport_plage(commits, fautes_plage(commits, regles, auteur))
        if argv[0] == "--message":
            fautes = fautes_message(argv[1], regles, auteur)
        else:
            fautes = fautes_fichiers(argv[0], regles, auteur)
    except (OSError, RuntimeError, ValueError) as e:
        print(f"REFUS : rien n'a été vérifié : {e}")
        return 1
    for chemin, regle in fautes:
        print(f"REFUS : {regle} dans {chemin}")
    return 1 if fautes else 0


def rapport_plage(commits, fautes):
    for court, endroit, regle in fautes:
        print(f"REFUS : {regle} dans {endroit}, commit {court}")
    en_faute = list(dict.fromkeys(court for court, _, _ in fautes))
    if en_faute:
        print(f"Commits en faute ({len(en_faute)} sur {len(commits)}) : {' '.join(en_faute)}")
        return 1
    print(f"-> garde de publication : {len(commits)} commit(s) contrôlé(s), aucune faute")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
