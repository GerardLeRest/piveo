from pathlib import Path
import sys

def base_dir() -> Path:
    """
    Dossier racine des ressources :
    - en --onefile : dossier temporaire _MEIPASS (où PyInstaller décompresse)
    - en --onedir : dossier contenant l'exe
    - en dev      : dossier racine du projet (comme avant)
    """
    if getattr(sys, "frozen", False): # Windows
        # --onefile : ressources dans _MEIPASS
        if hasattr(sys, "_MEIPASS"):
            return Path(sys._MEIPASS)  # type: ignore[attr-defined]
        # --onedir : ressources à côté de l'exe
        return Path(sys.executable).resolve().parent

    # dev : autre
    return Path(__file__).resolve().parent.parent

def resource_path(relative: str) -> Path:
    return base_dir() / relative
