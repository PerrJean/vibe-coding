"""garde-diff-avant : hook PreToolUse (Write|Edit|MultiEdit) de Claude Code.

Copie le fichier sur le point d'être modifié dans ~/.cache/garde-diff/,
pour que garde-diff-apres le compare à la nouvelle version.
Ne bloque jamais : sort toujours en 0, sans rien afficher.
"""
import datetime
import fnmatch
import json
import os
import shutil
import sys
import time

CACHE = os.path.join(os.path.expanduser("~"), ".cache", "garde-diff")
JOURS_CONSERVATION = 7  # copies gardées après une alerte, ou orphelines (outil refusé ou en échec)
SENSIBLES = (".env*", "*.pem", "*.key", "settings.local.json")  # jamais copiés


def journaliser(chemin, erreur):
    try:
        os.makedirs(CACHE, exist_ok=True)
        with open(os.path.join(CACHE, "erreurs.log"), "a", encoding="utf-8", newline="\r\n") as f:
            f.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} avant {chemin} : {erreur}\n")
    except Exception:
        pass


def main(etat):
    entree = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    chemin = str((entree.get("tool_input") or {}).get("file_path") or "")
    appel = str(entree.get("tool_use_id") or "")
    etat["chemin"] = chemin
    if not chemin:
        return

    nom = os.path.basename(chemin)
    if any(fnmatch.fnmatch(nom, motif) for motif in SENSIBLES):  # insensible à la casse sous Windows
        return

    if not os.path.isfile(chemin):
        return
    if not appel:
        raise RuntimeError("tool_use_id absent de l'entrée du hook")

    os.makedirs(CACHE, exist_ok=True)
    limite = time.time() - JOURS_CONSERVATION * 86400
    with os.scandir(CACHE) as entrees:
        for e in entrees:
            if e.name.endswith(".orig") and e.is_file() and e.stat().st_mtime < limite:
                try:
                    os.remove(e.path)
                except OSError:
                    pass

    # copyfile ne recopie pas les dates : la copie est datée de maintenant.
    shutil.copyfile(chemin, os.path.join(CACHE, f"{appel}_{nom}.orig"))


if __name__ == "__main__":
    etat = {"chemin": ""}
    try:
        main(etat)
    except Exception as erreur:
        journaliser(etat["chemin"], erreur)
    sys.exit(0)
