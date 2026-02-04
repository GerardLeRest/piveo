#!/usr/bin/python2
# -*- coding: utf-8 -*

"""     
    Fenêtre d'accueil - choix de l'organisme:
    Ecole, Entreprise, Parlement
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton,
    QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from builtins import _
from app.FenetrePrincipale import Fenetre
from app.utils import get_repertoire_racine
from pathlib import Path
import json, sqlite3
from app.paths import load_config, resolve_paths, ensure_paths


class ChoixOrganisme(QWidget):
    """Choisir l'organisme - Parlement - École - Entreprise"""

    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self) -> None:
        """création de l'interface"""
        self.resize(250, 400)
        self.setWindowTitle(_("Piveo"))
        self.setStyleSheet("background-color: white;")  # fond blanc propre
        layout = QVBoxLayout() # layout général
        layout.setContentsMargins(20, 20, 20, 20)  # marges internes propres

        # Titre centré
        label = QLabel(_("mode de fonctionnement"))
        label.setStyleSheet("""
            color: #2F4F4F;
            font-weight: bold;
            font-size: 20px;
        """)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        layout.addSpacing(10)

        # Boutons radios
        self.radioEcole = QRadioButton(_("Ecole"))
        self.radioEntreprise = QRadioButton(_("Entreprise"))
        self.radioParlement = QRadioButton(_("Parlement"))
        self.radioEcole.setChecked(True) # radio s&électionné par défaut

        for radio in [self.radioEcole, self.radioEntreprise, self.radioParlement]:
            radio.setStyleSheet("font-size: 18px; margin: 2px 0;")
            layout.addWidget(radio)

        layout.addSpacing(15)

        # Bouton OK centré et stylisé
        bouton = QPushButton(_("OK"))
        bouton.setFixedWidth(80)
        bouton.setStyleSheet("""
            QPushButton {
                background-color: #4682B4;
                color: white;
                border-radius: 8px;
                padding: 5px 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5A9BD5;
            }
        """)
        layout.addWidget(bouton, alignment=Qt.AlignCenter)
        bouton.clicked.connect(self.lancerPiveo)

        layout.addSpacing(15)

        # Logo centré
        labelLogo = QLabel()
        self.repertoireRacine = Path(get_repertoire_racine())
        chemin_icone = self.repertoireRacine / "fichiers" / "logos" / "logoPiveo.png"
        pixmap = QPixmap(str(chemin_icone))
        if not pixmap.isNull():
            pixmap = pixmap.scaledToWidth(100, Qt.SmoothTransformation)
            labelLogo.setPixmap(pixmap)
        labelLogo.setAlignment(Qt.AlignCenter)
        layout.addWidget(labelLogo)

        self.setLayout(layout)

    def lancerPiveo(self):
        "lancement de la classe Piveo"
        if self.radioEcole.isChecked():
            fichier = "ConfigEcole.json"
        elif self.radioEntreprise.isChecked():
            fichier = "ConfigEntreprise.json"
        elif self.radioParlement.isChecked():
            fichier = "ConfigParlement.json"
        else:
            fichier = None
        try:
            chemin = self.repertoireRacine.parent / "ressources" /"config" / fichier
            with open(chemin, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement du fichier : {e}")
            return
        # connexion de la base de données
        paths = resolve_paths(config)
        ensure_paths(paths) # construction des dossiers manquant
        print("BASE UTILISÉE :", paths["database"])  # ← LIGNE DE DEBUG
        # connexion à la base de données
        conn = sqlite3.connect(paths["database"])
        # lancement de la fenetre
        self.Piveo = Fenetre(config, conn)
        self.Piveo.show()
        self.close()