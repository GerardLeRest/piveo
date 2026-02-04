from pathlib import Path
import json
 
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

def load_config(config_name: str = "config.json") -> dict:
    """
    Charge le fichier de configuration JSON du projet.
    """
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / config_name
    if not config_path.exists():
        raise FileNotFoundError(f"Fichier de configuration introuvable : {config_path}")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)