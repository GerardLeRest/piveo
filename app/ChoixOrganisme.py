#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fenêtre d'accueil – choix de l'organisme :
École, Entreprise, Parlement
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
# from gettext import gettext as _
from pathlib import Path
import json, sqlite3
from app.FenetrePrincipale import Fenetre
from app.utils import get_repertoire_racine

class ChoixOrganisme(QWidget):
    """Fenêtre de choix de l'organisme"""

    

    def __init__(self):
        super().__init__()
        self.repertoire_racine = Path(get_repertoire_racine())
        self.interface()

    def interface(self) -> None:
        """Création de l'interface graphique"""
        self.resize(250, 400)
        self.setWindowTitle(_("Piveo"))
        self.setStyleSheet("background-color: white;")
        # layout verticale
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        # Titre
        label = QLabel(_("Mode de fonctionnement"))
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet(
            "color: #2F4F4F; font-weight: bold; font-size: 20px;"
        )
        layout.addWidget(label)
        layout.addSpacing(10)
        # Boutons radio
        self.radio_ecole = QRadioButton(_("École"))
        self.radio_entreprise = QRadioButton(_("Entreprise"))
        self.radio_parlement = QRadioButton(_("Parlement"))
        self.radio_ecole.setChecked(True)
        for radio in (self.radio_ecole, self.radio_entreprise, self.radio_parlement):
            radio.setStyleSheet("font-size: 18px; margin: 2px 0;")
            layout.addWidget(radio)
        # créer un espace
        layout.addSpacing(15)
        # Bouton OK
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
        bouton.clicked.connect(self.lancer_piveo)
        layout.addWidget(bouton, alignment=Qt.AlignCenter)
        # créer un espace
        layout.addSpacing(15)
        # Logo
        label_logo = QLabel()
        chemin_logo = (
            self.repertoire_racine / "fichiers" / "logos" / "logoPiveo.png"
        )
        pixmap = QPixmap(str(chemin_logo))
        if not pixmap.isNull():
            label_logo.setPixmap(
                pixmap.scaledToWidth(100, Qt.SmoothTransformation)
            )
        label_logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(label_logo)
        # attacher le layout à la fenêtre (self)
        self.setLayout(layout)

    def lancer_piveo(self) -> None:
        """Lancé après le clic utilisateur"""
        # chemin des ~/.loval/piveo
        APP_NAME = "piveo"
        USER_BASE = Path.home() / ".local" / APP_NAME
    
        if self.radio_ecole.isChecked():
            fichier_config = "ConfigEcole.json"
        elif self.radio_entreprise.isChecked():
            fichier_config = "ConfigEntreprise.json"
        else:
            fichier_config = "ConfigParlement.json"
        # charger la configuration choisie
        try:
            chemin_config = USER_BASE / "config" / fichier_config
            with open(chemin_config, "r", encoding="utf-8") as f:
                config = json.load(f)
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration : {e}")
            return
        # Chemin COMPLET vers la base de données
        chemin_bdd = USER_BASE / "BaseDonnees" / config["BaseDonnees"]
        conn = sqlite3.connect(chemin_bdd)
        # Lancement de la fenêtre principale
        self.fenetre_principale = Fenetre(config, conn)
        self.fenetre_principale.show()
        self.close()