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

repertoireRacine=os.path.dirname(os.path.abspath(__file__)) # répetoire du fichier pyw

class FrameDroiteHaute(QWidget):
    """ Créer la partie droite haute de l'interface """
        
    def __init__(self, config, fenetre = None):
        """Constructeur de la frame de droite et de ses éléments"""
        super().__init__(fenetre)  # ← Important 
        self.config = config # configuration de l'interface - json
        # layout de la classe
        layoutDroitHaut = QVBoxLayout()        
        # zone de saisie - GrdGidLayout - partie haue
        # prenom
        layoutGrille = QGridLayout()
        self.labelPrenom = QLabel(_("Prénom"))
        layoutGrille.addWidget(self.labelPrenom,0,0)
        self.prenomEntry = QLineEdit()  
        self.prenomEntry.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        self.prenomEntry.setPlaceholderText(_("Indiquez votre prénom"))
        layoutGrille.addWidget(self.prenomEntry,0, 1)
        # nom
        self.labelNom = QLabel(_("Nom"))
        layoutGrille.addWidget(self.labelNom,1,0)
        self.nomEntry = QLineEdit()  
        self.nomEntry.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 6px;
                padding: 4px 8px;
            }
        """)
        self.nomEntry.setPlaceholderText(_("Indiquez votre nom"))
        layoutGrille.addWidget(self.nomEntry,1, 1)
        layoutDroitHaut.addLayout(layoutGrille)
        layoutDroitHaut.addSpacing(5)
        # Zone boutons - QHBoxLayout
        validerStyle = """
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

        suiteBoutonStyle = """
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

        effaceBoutonStyle =   """
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
        layoutBoutons = QHBoxLayout()
        # bouton valider
        self.boutVal = QPushButton (_("Valider"), self)
        self.boutVal.setStyleSheet(validerStyle)
        layoutBoutons.addWidget(self.boutVal)
        # bouton effacer
        self.boutEff = QPushButton (_("Effacer"), self)
        self.boutEff.setStyleSheet(effaceBoutonStyle)
        layoutBoutons.addWidget(self.boutEff)
        # bouton Suite
        self.boutSuite = QPushButton (_("Suite"), self)
        self.boutSuite.setStyleSheet(suiteBoutonStyle)
        layoutBoutons.addWidget(self.boutSuite)
        # espacement au dessus des boutons
        spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layoutDroitHaut.addItem(spacer)
        layoutDroitHaut.addLayout(layoutBoutons)

        # désativer les boutons
        self.boutVal.setEnabled(False)
        self.boutEff.setEnabled(False)
        self.boutSuite.setEnabled(False)

        # partie du bas - 2 images (réusssite à gauhe et score à droite)
        layoutImages = QHBoxLayout()
        # image de validation chexk ou cross)
        self.labelImageGauche = QLabel()
        self.image = QPixmap(os.path.join(repertoireRacine, "fichiers", "icones", "transparent.png"))
        self.labelImageGauche.setPixmap(self.image) 
        layoutImages.addWidget(self.labelImageGauche)
        # espace entre l'image et le compteur de bonnes réponses
        layoutImages.addStretch()  # ← ajoute un espace flexible
        # affichage des bonnes réponses
        self.nbreRep = QLabel(_("0/0")) 
        self.nbreRep.setStyleSheet("color: grey;font-size: 30px;")
        self.nbreRepExactes=0 
        layoutImages.addWidget(self.nbreRep)
        layoutDroitHaut.addLayout(layoutImages)
        layoutDroitHaut.addSpacing(10)
        
        # Ligne horizontale continue
        ligne = QFrame()
        ligne.setFrameShape(QFrame.HLine)
        ligne.setFrameShadow(QFrame.Plain)
        ligne.setLineWidth(1)
        ligne.setStyleSheet("color: black;")
        layoutDroitHaut.addWidget(ligne)
        self.setLayout(layoutDroitHaut)
        self.show()
        
                
    def configRechercher(self) -> None:
        """configurer - mode Rechercher"""
        # changer couleur label
        self.labelPrenom.setStyleSheet("color: black;")
        self.labelNom.setStyleSheet("color: black;")
        # Désactiver l'affichage des bonnes réponses
        self.DesAffichRep()
        # activer/désactiver boutons 
        self.boutVal.setEnabled(True)
        self.boutEff.setEnabled(True)
        self.boutSuite.setEnabled(False)
    
    def DesAffichRep(self) -> None:
        """ désactiver l'affichage des bonnes réponses"""
        self.nbreRep.setStyleSheet("color: grey;font-size: 30px") #nbre bonnes reponses en gris
        self.nbreRepExactes=0  # nbre de réponses exactes
        # maj nbrebonnes réponses
        self.nbreRep.setText(f"{self.nbreRepExactes}/0")   
    
    def desFrameDrHa(self) -> None:
        """désactiver des boutons et les entry de la frameDB"""     
        self.prenomEntry.setEnabled(False)
        self.nomEntry.setEnabled(False)
        self.boutVal.setEnabled(False)
        self.boutEff.setEnabled(False)
        self.boutSuite.setEnabled(False)
        self.nbreRep.setStyleSheet("color: grey;font-size: 30px")
        
    def effacerReponses(self) -> None:
        """effacer réponses"""
        # effacer champs des noms et prénom
        self.prenomEntry.setEnabled(True)
        self.prenomEntry.clear()
        self.nomEntry.setEnabled(True)
        self.nomEntry.clear()
        # effacer icone
        self.image = QPixmap(os.path.join(repertoireRacine, "fichiers", "icones", "transparent.png"))
        self.labelImageGauche.setPixmap(self.image) 
        # désactiver - Nbres bonne réponse  
        self.nbreRep.setEnabled(False) 
        
    def configTestEcrit(self) -> None:
        """ configurer - Test écrit """
        # changer couleur label
        self.labelPrenom.setStyleSheet("color: black;")
        self.labelNom.setStyleSheet("color: black;")
        self.nomEntry.setStyleSheet("color: black") 
        self.nbreRep.setStyleSheet("color: back; font-size:30px;") 
        # effacer réponses
        self.effacerReponses()        
        # activer boutons 
        self.boutVal.setEnabled(True)
        self.boutEff.setEnabled(True)
        self.boutSuite.setEnabled(True)   
        
# ----------------------------------------------------
if __name__ == "__main__":
    import gettext
    gettext.install("piveo")
    app = QApplication(sys.argv)
    fenetre = FrameDroiteHaute(None)
    fenetre.prenomEntry.setEnabled(True)
    fenetre.nomEntry.setEnabled(True)
    fenetre.boutVal.setEnabled(True)
    fenetre.boutEff.setEnabled(False)
    fenetre.boutSuite.setEnabled(False)    
    app.exec()