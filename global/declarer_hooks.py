"""Déclare les hooks garde-diff dans le settings.json de l'agent.

Appelé par installer.ps1 (Windows) et installer.sh (macOS, Linux), qui lui passent
la commande Python du système : python sous Windows, python3 ailleurs.

    <python> declarer_hooks.py <dossier .claude> <python> [--simulation]

Une déclaration déjà présente pour le même script est mise à jour, jamais dupliquée.
Les autres réglages du fichier sont gardés tels quels. L'ancien fichier est sauvegardé
à côté (settings.json.avant-vibe-coding) avant toute écriture.
"""
import json
import shutil
import sys
from pathlib import Path

HOOKS = (  # événement, script, délai en secondes
    ("PreToolUse", "garde-diff-avant.py", 15),
    ("PostToolUse", "garde-diff-apres.py", 30),
)
FILTRE = "Write|Edit|MultiEdit"


def commande(python, dossier, script):
    chemin = (dossier / "hooks" / script).as_posix()
    return f'{python} -I -S "{chemin}"'


def declarer(reglages, python, dossier):
    """Ajoute ou met à jour chaque hook. Rend la liste des changements faits."""
    changements = []
    tous = reglages.setdefault("hooks", {})
    for evenement, script, delai in HOOKS:
        voulu = {"type": "command", "command": commande(python, dossier, script), "timeout": delai}
        groupes = tous.setdefault(evenement, [])
        existant = next((h for g in groupes for h in g.get("hooks", [])
                         if script in str(h.get("command", ""))), None)
        if existant is None:
            groupes.append({"matcher": FILTRE, "hooks": [voulu]})
            changements.append(f"{evenement} : {script} déclaré")
        elif existant != voulu:
            existant.clear()
            existant.update(voulu)
            changements.append(f"{evenement} : {script} mis à jour")
    return changements


def main(argv):
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] != "--simulation"):
        print(__doc__)
        return 2
    dossier, python = Path(argv[0]).expanduser(), argv[1]
    simulation = len(argv) == 3
    fichier = dossier / "settings.json"
    reglages = json.loads(fichier.read_text(encoding="utf-8-sig")) if fichier.is_file() else {}
    changements = declarer(reglages, python, dossier)
    prefixe = "[simulation] " if simulation else ""
    if not changements:
        print(f"{prefixe}Hooks déjà déclarés dans {fichier}")
        return 0
    for c in changements:
        print(f"{prefixe}{c} ({python})")
    if simulation:
        return 0
    if fichier.is_file():
        shutil.copyfile(fichier, fichier.with_name("settings.json.avant-vibe-coding"))
    dossier.mkdir(parents=True, exist_ok=True)
    fichier.write_text(json.dumps(reglages, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Hooks déclarés dans {fichier}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
