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


def load_config(config_name: str = "config.json") -> dict:
    """ Charge la configuration utilisateur. """
    config_path = USER_BASE / "config" / config_name
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_paths(config: dict) -> dict:
    """retourne un dictionnaire de chemins"""
    return {
        "base": USER_BASE,
        "config": USER_BASE / "config",
        "BaseDonnees": USER_BASE / "BaseDonnees",   # ← CLÉ MANQUANTE
        "fichiers": USER_BASE / "fichiers",
        "photos": USER_BASE / "fichiers" / "photos" / config["CheminPhotos"],
        "database": USER_BASE / "BaseDonnees" / config["BaseDonnees"],
    }

def ensure_paths(paths: Dict[str, Path]) -> None:
    """ Crée les dossiers nécessaires à l'exécution si absents. """
    for key in ("config", "BaseDonnees", "fichiers", "photos"):
        paths[key].mkdir(parents=True, exist_ok=True)
