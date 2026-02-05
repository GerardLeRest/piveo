import json
import shutil
from pathlib import Path
from typing import Dict

APP_NAME = "piveo"
USER_BASE = Path.home() / ".local" / APP_NAME

def init_user_data() -> None:
    """
    Première initialisation de Piveo.
    Copie resources/ vers ~/.local/piveo si nécessaire.
    """
    resources_base = Path(__file__).resolve().parent.parent / "ressources"

    if USER_BASE.exists():
        return
    for item in resources_base.iterdir():
        dest = USER_BASE / item.name
        if item.is_dir():
            shutil.copytree(item, dest) # dossier
        else:
            shutil.copy2(item, dest) # fichier
