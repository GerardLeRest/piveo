import os, sys

def get_repertoire_racine() -> str:
    """
    Retourne le répertoire racine de l'application.

    - Linux AppImage : dossier contenant l'AppImage
    - Windows exe    : dossier contenant le .exe
    - Python (dev)   : dossier du fichier courant
    """
    # Linux AppImage
    appimage = os.environ.get("APPIMAGE")
    if appimage:
        return os.path.dirname(os.path.abspath(appimage))

    # Windows exe (PyInstaller, cx_Freeze, etc.)
    if getattr(sys, "frozen", False):
        return os.path.dirname(os.path.abspath(sys.executable))

    # Python (dev)
    return os.path.dirname(os.path.abspath(__file__))
