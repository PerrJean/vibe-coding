"""garde-diff-apres : hook PostToolUse (Write|Edit|MultiEdit) de Claude Code.

Compare la copie faite par garde-diff-avant au fichier modifié.
Réécriture complète ou conversion des fins de ligne : alerte (code 2), copie gardée.
Sinon : copie supprimée, sortie en 0 sans rien afficher.
"""
import datetime
import json
import os
import subprocess
import sys

SEUIL_REECRITURE = 0.8  # part des lignes du fichier ajoutées ET retirées
LIGNES_MIN = 50  # le fichier doit en compter strictement plus
ECART_FINS_DE_LIGNE = 10  # lignes en plus dans le diff brut par rapport au diff sans CR
CACHE = os.path.join(os.path.expanduser("~"), ".cache", "garde-diff")


def alerter(message):
    sys.stderr.buffer.write(message.encode("utf-8"))
    sys.stderr.buffer.flush()
    sys.exit(2)


def journaliser(chemin, erreur):
    try:
        os.makedirs(CACHE, exist_ok=True)
        with open(os.path.join(CACHE, "erreurs.log"), "a", encoding="utf-8", newline="\r\n") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} apres {chemin} : {erreur}\n")
    except Exception:
        pass


def lancer_numstat(copie, chemin, *options):
    # autocrlf forcé à false pour comparer les octets réels.
    # --no-index renvoie 1 quand les fichiers diffèrent : ce n'est pas une erreur.
    commande = ["git", "-c", "core.autocrlf=false", "-C", CACHE, "diff", "--no-index",
                "--numstat", *options, "--", copie, chemin]
    return subprocess.Popen(commande, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                            stderr=subprocess.DEVNULL)


def lire_numstat(processus):
    sortie, _ = processus.communicate()
    plus = moins = 0
    for ligne in sortie.decode("utf-8", "replace").splitlines():
        champs = ligne.split("\t")
        if len(champs) >= 3 and champs[0].isdigit() and champs[1].isdigit():
            plus += int(champs[0])
            moins += int(champs[1])
    return plus, moins


def main(etat):
    entree = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    chemin = str((entree.get("tool_input") or {}).get("file_path") or "")
    appel = str(entree.get("tool_use_id") or "")
    etat["chemin"] = chemin
    if not chemin or not appel:
        return

    copie = os.path.join(CACHE, f"{appel}_{os.path.basename(chemin)}.orig")
    # Pas de copie : fichier créé par cet appel, ou fichier sensible.
    if not os.path.isfile(copie) or not os.path.isfile(chemin):
        return

    # Les deux diffs tournent en parallèle.
    p_brut = lancer_numstat(copie, chemin)
    p_sans_cr = lancer_numstat(copie, chemin, "--ignore-cr-at-eol")
    brut = lire_numstat(p_brut)
    sans_cr = lire_numstat(p_sans_cr)
    total_brut = brut[0] + brut[1]
    total_sans_cr = sans_cr[0] + sans_cr[1]
    annulation = (f"Version précédente : {copie}. Pour annuler, recopie-la sur {chemin}, "
                  "puis refais la modification de façon ciblée avec Edit.")

    if total_brut - total_sans_cr >= ECART_FINS_DE_LIGNE and total_brut >= 2 * total_sans_cr:
        alerter(f"Fins de ligne converties dans {chemin} : {total_brut} lignes changées, "
                f"{total_sans_cr} seulement en ignorant les CR. {annulation} "
                "Si la conversion des fins de ligne était demandée, ignore cette alerte et dis-le.")

    with open(chemin, "rb") as f:
        lignes = len(f.read().splitlines())  # coupe sur \r\n, \n et \r, comme ReadAllLines
    if (lignes > LIGNES_MIN and brut[0] > SEUIL_REECRITURE * lignes
            and brut[1] > SEUIL_REECRITURE * lignes):
        alerter(f"Réécriture complète de {chemin} : +{brut[0]} / -{brut[1]} lignes sur {lignes}. "
                f"{annulation} Si la réécriture complète était demandée, ignore cette alerte et dis-le.")

    os.remove(copie)


if __name__ == "__main__":
    etat = {"chemin": ""}
    try:
        main(etat)
    except Exception as erreur:
        journaliser(etat["chemin"], erreur)
    sys.exit(0)
