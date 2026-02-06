#!/usr/bin/env python3

import sys
import locale
import gettext
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.chargement import init_user_data
from app.GestionLangue import GestionLangue

# répertoires
BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "ressources" / "locales"
# copie de ressources vers ~/.local/piveo
# (uniquement si le dossier n'existe pas)
init_user_data()
# fichier config pour les json
config_dir = Path.home() / ".local" / "piveo" / "config"
config_dir.mkdir(parents=True, exist_ok=True)
# fichier de configuration de la langue
fichier_langue = config_dir / "configurationLangue.json"
# lecture de la langue choisie
gestion_langue = GestionLangue(fichier_langue)
langue = gestion_langue.lire()
# configuration locale système
locale.setlocale(locale.LC_ALL, "")
# initialisation de gettext AVANT toute interface
translation = gettext.translation(
    domain="messages",
    localedir=str(LOCALE_DIR),
    languages=[langue],
    fallback=True
)
translation.install()
# import de l'interface APRÈS gettext
from app.ChoixOrganisme import ChoixOrganisme

# point d'entrée de l'application
def main():
    app = QApplication(sys.argv)
    fenetre = ChoixOrganisme()
    fenetre.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
