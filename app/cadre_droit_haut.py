#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
rechercher une ou plusieurs personnes dans 
l'établissement
"""


from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QHBoxLayout, QPushButton, QApplication, QSpacerItem, QSizePolicy, QFrame
from PySide6.QtGui import QPixmap
from builtins import _
import os, sys

REPERTOIRE_RACINE=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class CadreDroiteHaut(QWidget):
    """ Créer la partie droite haute de l'interface """
        
    def __init__(self, config, fenetre = None):
        """Constructeur de la frame de droite et de ses éléments"""
        super().__init__(fenetre)  # ← Important 
        self.config = config # configuration de l'interface - json
        # layout de la classe
        layout_droit_haut = QVBoxLayout()        
        # zone de saisie - GrdGidLayout - partie haue
        # prenom
        layout_grille = QGridLayout()
        self.label_prenom = QLabel(_("Prénom"))
        layout_grille.addWidget(self.label_prenom,0,0)
        self.prenom_entree = QLineEdit()  
        self.prenom_entree.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        self.prenom_entree.setPlaceholderText(_("Indiquez votre prénom"))
        layout_grille.addWidget(self.prenom_entree,0, 1)
        # nom
        self.label_nom = QLabel(_("Nom"))
        layout_grille.addWidget(self.label_nom,1,0)
        self.nom_entree = QLineEdit()  
        self.nom_entree.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        self.nom_entree.setPlaceholderText(_("Indiquez votre nom"))
        layout_grille.addWidget(self.nom_entree,1, 1)
        layout_droit_haut.addLayout(layout_grille)
        layout_droit_haut.addSpacing(5)
        # Zone boutons - QHBoxLayout
        valider_style = """
            QPushButton {
                background-color: #76aeba;
                border: 1px solid #558b9e;
                border-radius: 6px;
                padding: 6px 14px;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #66a0b0;
            }
            QPushButton:pressed {
                background-color: #5c8c9c;
            }
        """

        suite_bouton_style = """
            QPushButton {
                background-color: #a6d0c0;
                border: 1px solid #7fb09b;
                border-radius: 6px;
                padding: 6px 14px;
                color: black;
            }
            QPushButton:hover {
                background-color: #95c0b0;
            }
            QPushButton:pressed {
                background-color: #84b0a0;
            }
        """

        efface_bouton_style =   """
            QPushButton {
                background-color: #9aaab8;
                border: 1px solid #7a8a98;
                border-radius: 6px;
                padding: 6px 14px;
                color: black;
            }
            QPushButton:hover {
                background-color: #8b9ba9;
            }
            QPushButton:pressed {
                background-color: #7c8c99;
            }
        """

        # boutons
        layout_boutons = QHBoxLayout()
        # bouton valider
        self.bout_val = QPushButton (_("Valider"), self)
        self.bout_val.setStyleSheet(valider_style)
        layout_boutons.addWidget(self.bout_val)
        # bouton effacer
        self.bout_eff = QPushButton (_("Effacer"), self)
        self.bout_eff.setStyleSheet(efface_bouton_style)
        layout_boutons.addWidget(self.bout_eff)
        # bouton Suite
        self.bout_suite = QPushButton (_("Suite"), self)
        self.bout_suite.setStyleSheet(suite_bouton_style)
        layout_boutons.addWidget(self.bout_suite)
        # espacement au dessus des boutons
        espaceur = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_droit_haut.addItem(espaceur)
        layout_droit_haut.addLayout(layout_boutons)

        # désativer les boutons
        self.bout_val.setEnabled(False)
        self.bout_eff.setEnabled(False)
        self.bout_suite.setEnabled(False)

        # partie du bas - 2 images (réusssite à gauhe et score à droite)
        layout_images = QHBoxLayout()
        # image de validation check ou cross)
        self.label_image_gauche = QLabel()
        self.image = QPixmap(os.path.join(REPERTOIRE_RACINE, "ressources","fichiers", "icones", "transparent.png"))
        self.label_image_gauche.setPixmap(self.image) 
        layout_images.addWidget(self.label_image_gauche)
        # espace entre l'image et le compteur de bonnes réponses
        layout_images.addStretch()  # ← ajoute un espace flexible
        # affichage des bonnes réponses
        self.nbre_rep = QLabel(_("0/0")) 
        self.nbre_rep.setStyleSheet("color: grey;font-size: 30px;")
        self.nbre_rep_exactes=0 
        layout_images.addWidget(self.nbre_rep)
        layout_droit_haut.addLayout(layout_images)
        layout_droit_haut.addSpacing(10)
        
        # Ligne horizontale continue
        ligne = QFrame()
        ligne.setFrameShape(QFrame.HLine)
        ligne.setFrameShadow(QFrame.Plain)
        ligne.setLineWidth(1)
        ligne.setStyleSheet("color: black;")
        layout_droit_haut.addWidget(ligne)
        self.setLayout(layout_droit_haut)
        self.show()
        
                
    def config_rechercher(self) -> None:
        """configurer - mode Rechercher"""
        # changer couleur label
        self.label_prenom.setStyleSheet("color: black;")
        self.label_nom.setStyleSheet("color: black;")
        # Désactiver l'affichage des bonnes réponses
        self.Des_Affich_Rep()
        # activer/désactiver boutons 
        self.bout_val.setEnabled(True)
        self.bout_eff.setEnabled(True)
        self.bout_suite.setEnabled(False)
    
    def Des_Affich_Rep(self) -> None:
        """ désactiver l'affichage des bonnes réponses"""
        self.nbre_rep.setStyleSheet("color: grey;font-size: 30px") #nbre bonnes reponses en gris
        self.nbre_rep_exactes=0  # nbre de réponses exactes
        # maj nbrebonnes réponses
        self.nbre_rep.setText(f"{self.nbre_rep_exactes}/0")   
    
    def des_cadre_Dr_Ha(self) -> None:
        """désactiver des boutons et les entry de la frameDB"""     
        self.prenom_entree.setEnabled(False)
        self.nom_entree.setEnabled(False)
        self.bout_val.setEnabled(False)
        self.bout_eff.setEnabled(False)
        self.bout_suite.setEnabled(False)
        self.nbre_rep.setStyleSheet("color: grey;font-size: 30px")
        
    def effacer_reponses(self) -> None:
        """effacer réponses"""
        # effacer champs des noms et prénom
        self.prenom_entree.setEnabled(True)
        self.prenom_entree.clear()
        self.nom_entree.setEnabled(True)
        self.nom_entree.clear()
        # effacer icone
        self.image = QPixmap(os.path.join(REPERTOIRE_RACINE, "fichiers", "icones", "transparent.png"))
        self.label_image_gauche.setPixmap(self.image) 
        # désactiver - Nbres bonne réponse  
        self.nbre_rep.setEnabled(False) 
        
    def config_test_ecrit(self) -> None:
        """ configurer - Test écrit """
        # changer couleur label
        self.label_prenom.setStyleSheet("color: black;")
        self.label_nom.setStyleSheet("color: black;")
        self.nom_entree.setStyleSheet("color: black") 
        self.nbre_rep.setStyleSheet("color: back; font-size:30px;") 
        # effacer réponses
        self.effacer_reponses()        
        # activer boutons 
        self.bout_val.setEnabled(True)
        self.bout_eff.setEnabled(True)
        self.bout_suite.setEnabled(True)   
        
# ----------------------------------------------------
if __name__ == "__main__":
    import gettext
    gettext.install("piveo")
    app = QApplication(sys.argv)
    fenetre = CadreDroiteHaut(None)
    fenetre.prenom_entree.setEnabled(True)
    fenetre.nom_entree.setEnabled(True)
    fenetre.bout_val.setEnabled(True)
    fenetre.bout_eff.setEnabled(False)
    fenetre.bout_suite.setEnabled(False)    
    app.exec()