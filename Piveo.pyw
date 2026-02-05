#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, locale, gettext, os
from pathlib import Path
from PySide6.QtWidgets import QApplication
from app.GestionLangue import GestionLangue
from app.paths import init_user_data

# Langue
BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "ressources" / "locales"
# construction du dossier ~/.local/piveo
config_dir = Path.home() / ".config" / "piveo"
config_dir.mkdir(parents=True, exist_ok=True)
# gestion de la langue
fichier_langue = config_dir / "configurationLangue.json"
gestion_langue = GestionLangue(fichier_langue)
langue = gestion_langue.lire()
locale.setlocale(locale.LC_ALL, "")
#traductions:
translation = gettext.translation(
    domain="messages",
    localedir=str(LOCALE_DIR),
    languages=[langue],
    fallback=True
)
translation.install()

# Main
def main():
    init_user_data() # copie des ressources du programme vers ~/.local/Piveo
    from app.ChoixOrganisme import ChoixOrganisme # erreur de _
    # création de la fenêtre
    app = QApplication(sys.argv)
    fenetre = ChoixOrganisme()
    fenetre.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
