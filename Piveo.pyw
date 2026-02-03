#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, json, locale, gettext
from pathlib import Path
from app.GestionLangue import GestionLangue

# Gestion de la langue de cette cesssion
BASE_DIR = Path(__file__).resolve().parent
LOCALE_DIR = BASE_DIR / "ressources" / "locales"

configDir = Path.home() / ".config" / "piveo"
configDir.mkdir(parents=True, exist_ok=True)
fichierLangue = configDir / "configurationLangue.json"

gestionLangue = GestionLangue(fichierLangue)
langue = gestionLangue.lire()

locale.setlocale(locale.LC_ALL, "")

translation = gettext.translation(
    domain="messages",
    localedir=str(LOCALE_DIR),
    languages=[langue],
    fallback=True
)
translation.install()

# Lancement de la fenetre organisme
from PySide6.QtWidgets import QApplication
from app.ChoixOrganisme import ChoixOrganisme

if __name__ == "__main__":
    app = QApplication(sys.argv)
    fenetre = ChoixOrganisme()
    fenetre.show()
    sys.exit(app.exec())
