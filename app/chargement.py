import shutil
from pathlib import Path

APP_NAME = "piveo"
USER_BASE = Path.home() / ".local" / APP_NAME

def init_donnees_utiliisateurs() -> None:
    """
    Initialise les données utilisateur uniquement si ~/.local/piveo n'existe pas.
    Si le dossier existe déjà, on ne touche à rien.
    """
    resources_base = Path(__file__).resolve().parent.parent / "ressources"

    # Si le dossier utilisateur existe déjà : on ne fait rien
    if USER_BASE.exists():
        return

    # Sinon, installation complète des ressources
    shutil.copytree(resources_base, USER_BASE)