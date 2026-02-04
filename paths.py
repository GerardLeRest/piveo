from pathlib import Path

 
def resolve_paths(config: dict) -> dict:
    """dictionnaire des lens vers le dossier local/piveo"""
    base = Path.home() / ".local" / "piveo"
    return {
        "base": base,
        "config": base / "config",
        "BaseDonnees": base / "data",          # ← correspondance métier → technique
        "fichiers": base / "fichiers",
        "photos": base / "fichiers" / "photos" / config["CheminPhotos"],
        "database": base / "data" / config["BaseDonnees"],
    }

def ensure_paths(paths: dict) -> None:
    """crée les dossiers qui manques"""
    for key in ("config", "BaseDonnees", "fichiers", "photos"):
        paths[key].mkdir(parents=True, exist_ok=True)
