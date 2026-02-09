from pathlib import Path
import sys

def base_dir() -> Path:
    """
    Retourne le dossier de la release :
    - dossier contenant Piveo.pyw en dev
    - dossier contenant Piveo.exe en prod
    """
    if getattr(sys, "frozen", False): # windows
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent

def resource_path(relative: str) -> Path:
    """
    Retourne le chemin absolu d'une ressource
    située dans le dossier de la release.
    """
    return base_dir() / relative
