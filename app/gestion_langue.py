from pathlib import Path
import json


class GestionLangue:
    """Gestion de la langue de l'application (lecture / écriture)."""

    def __init__(self, fichier_config: Path):
        self.fichier_config = fichier_config

    def lire(self) -> str:
        if not self.fichier_config.exists():
            self.ecrire("fr")
            return "fr"

        with open(self.fichier_config, "r", encoding="utf-8") as f:
            config_json = json.load(f)
            return config_json. get("langueSelectionnee", "fr") # plus sur
            # ou return config_json["langueSelectionnee"]
        
    def ecrire(self, code_langue: str) -> None:
        with open(self.fichier_config, "w", encoding="utf-8") as f:
            json.dump(
                {"langueSelectionnee": code_langue},
                f,
                indent=4,
                ensure_ascii=False
            )