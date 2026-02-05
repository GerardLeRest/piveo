#!/usr/bin/python2
# -*- coding: utf-8 -*

"""
# selection du mode de fonctionnement
# (apprentissage, test mental, test ecrit, Rechercher)
# choix de la classe et de l'option
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox, QButtonGroup
from app.ModifierBDD import ModifierBDD
from PySide6.QtWidgets import QApplication
from app.utils_i18n import ui_value
from builtins import _
import sys

class FrameDroiteBasse (QWidget):
    """ Créer la partie droite basse de l'interface """
    def __init__(self, config, modifierBDD, fenetre = None ):
        """Constructeur de la frame de droite et de ses éléments"""
        # constructeur de la classe parente
        super().__init__(fenetre)
        self.config = config # configuration de l'interface - json
        self.modif = modifierBDD
        self.listePersonnes = []  # liste des élèves de la classe sélectionnée
        self.listeSpecialites = []  # liste des options des élèves de la classese

        self.specialiteSelectionnee = ""  # option sélectionnée

        layoutBasDroit = QVBoxLayout()
        layoutBasDroit.setSpacing(10)
        layoutBoutonsRadiosHaut = QHBoxLayout()
        # boutons radio des modes
        self.boutonRadioHaut1 = QRadioButton(_("Apprentissage"))
        self.boutonRadioHaut2 = QRadioButton(_("Test mental"))
        self.boutonRadioHaut3 = QRadioButton(_("Test ecrit"))
        self.boutonRadioHaut4 = QRadioButton(_("Rechercher"))
        # regroupement
        self.groupeHaut = QButtonGroup()
        self.groupeHaut.addButton(self.boutonRadioHaut1)
        self.groupeHaut.addButton(self.boutonRadioHaut2)
        self.groupeHaut.addButton(self.boutonRadioHaut3)
        self.groupeHaut.addButton(self.boutonRadioHaut4)
        # insetion dans le layout
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut1)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut2)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut3)
        layoutBoutonsRadiosHaut.addWidget(self.boutonRadioHaut4)
         #bouton radi 1 est sélectionné
        self.boutonRadioHaut1.setChecked(True)
        #rattachement au layout principal de la classe
        layoutBasDroit.addLayout(layoutBoutonsRadiosHaut)
        
        # Combobox - QGridLayout
        layoutGrille = QGridLayout()
        layoutGrille.setSpacing(10)
         # labels)
        layoutGrille.addWidget(QLabel(_(ui_value(self.config["Structure"]))), 0, 0)
        layoutGrille.addWidget(QLabel(_(ui_value(self.config["Specialite"]))), 0, 1)
        ## ComboBox
        self.comboBoxGauche = QComboBox()
        self.comboBoxDroite = QComboBox()
        layoutGrille.addWidget(self.comboBoxGauche,1,0)
        layoutGrille.addWidget(self.comboBoxDroite,1,1)
        layoutBasDroit.addLayout(layoutGrille)
        # création de la liste des classes
        classesRangees = sorted(self.listeDesStructures())  # crée une nouvelle liste triée
        classes_ui = [ui_value(c) for c in classesRangees]
        self.comboBoxGauche.addItems(classes_ui)
        self.comboBoxGauche.currentTextChanged.connect(self.choisirStructureSpecialites)
        # checkbutton Aléatoite
        layoutCheckBox = QHBoxLayout()
        self.checkBox = QCheckBox(_("Aléatoire"))
        layoutCheckBox.addWidget(self.checkBox)
        layoutBasDroit.addLayout(layoutCheckBox)
        # boutons radios avec/sans nom prénoms
        layoutBoutonsRadiosBas = QHBoxLayout()
        self.groupeBas = QButtonGroup()
        self.boutonRadioBas1 = QRadioButton(_("Prenom+Nom"))
        self.boutonRadioBas2 = QRadioButton(_("Prenom"))
        self.boutonRadioBas3 = QRadioButton(_("Nom"))
        # regroupement
        self.groupeBas.addButton(self.boutonRadioBas1)
        self.groupeBas.addButton(self.boutonRadioBas2)
        self.groupeBas.addButton(self.boutonRadioBas3)
        # attachement au layout horizontal
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas1)
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas2)
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas3)
         #bouton radi 1 est sélectionné
        self.boutonRadioBas1.setChecked(True)
        layoutBasDroit.addLayout(layoutBoutonsRadiosBas)
        
        # Bouton pour valider le choix
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
        # Créer le bouton "Valider"
        self.boutonVal = QPushButton(_("Valider"))
        self.boutonVal.setFixedWidth(120)
        self.boutonVal.setStyleSheet(validerStyle)
        self.boutonVal.clicked.connect(self.configRechercher)

        # Centrer le bouton
        layoutBouton = QHBoxLayout()
        layoutBouton.addStretch()
        layoutBouton.addWidget(self.boutonVal)
        layoutBouton.addStretch()

        # Ajouter au layout principal du bas
        layoutBasDroit.addSpacing(10)  # petit espace avant le bouton
        layoutBasDroit.addLayout(layoutBouton)
        # créer la liste des options
        self.creerComboSpecialites()

    # ancrer le layout principal à la fenêtre
        self.setLayout(layoutBasDroit)

        self.show()
        
    def listeDesStructures(self) -> list:
        """Renvoie la liste des structures de l'organisme"""
        structures = self.modif.listerStructures()
        if self.config["Organisme"] == "Ecole":
            phrase = _("- choisir une %(structure)s -") % {
                "structure": self.config["Structure"]
                }
        else:
            phrase = _("- choisir un %(structure)s -") % {
                "structure": self.config["Structure"]
                }
        return [phrase] + structures

    def configRechercher(self) -> None:
        """activer/désactiver les listes les comboBox, des radiobuttons
           et des labels"""
        if self.boutonRadioHaut4.isChecked():
            # désactiver les radiobuttons
            # self.boutonRadioHaut1.setEnabled(False)
            # self.boutonRadioHaut2.setEnabled(False)
            # self.boutonRadioHaut3.setEnabled(False)
            # self.boutonRadioHaut4.setEnabled(False)
            # désactiver les listes des comboBox
            self.comboBoxGauche.setEnabled(False)
            self.comboBoxDroite.setEnabled(False)
        else:
            # activer les listes des comboBox
            self.comboBoxGauche.setEnabled(True)
            self.comboBoxDroite.setEnabled(True)
            # activer les radiobuttons
            self.boutonRadioHaut1.setEnabled(True)
            self.boutonRadioHaut2.setEnabled(True)
            self.boutonRadioHaut3.setEnabled(True)
            self.boutonRadioHaut4.setEnabled(True)

    def definirOrdreDefilement(self) -> None :
        """Définir l'ordre de défilement"""
        self.ordreAleatoire = self.checkBox.isChecked() 

    def choisirStructureSpecialites(self) -> None:
        """Choisir la structure et mettre à jour les personnes et les spécialités"""
        structureChoisie = self.comboBoxGauche.currentText()
        self.listePersonnes = self.modif.personnesStructure(structureChoisie)

        # Crée les options présentes uniquement dans cette classe
        self.listeSpecialites = self.creerSpecialites()

        # Met à jour la combobox des options (ligne à garder si elle suit)
        self.creerComboSpecialites()

    def creerSpecialites(self) -> list:
        """Créer la liste des spécialités présentes uniquement dans la classe sélectionnée"""
        listeSpecialites = []
        for eleve in self.listePersonnes:
            options = eleve[3]  # Index 2 = liste des options (ex: ['ALL2', 'CAM'])
            for option in options:
                if option not in listeSpecialites:
                    listeSpecialites.append(option)
        listeSpecialites = sorted(listeSpecialites)
        listeSpecialites.insert(0, "TOUS")
        self.listeSpecialites = listeSpecialites
        return listeSpecialites
    
    def creerComboSpecialites(self) -> None:
        """Créer la liste déroulante des spécialités sans déclencher d'événement parasite"""
        #self.comboBoxDroite.blockSignals(True)  # Empêche les signaux lors de la modification
        self.comboBoxDroite.clear()
        self.comboBoxDroite.addItems(self.listeSpecialites)
        self.comboBoxDroite.setCurrentIndex(0)  # Facultatif : force "TOUS" si besoin
        #self.comboBoxDroite.blockSignals(False)
        self.comboBoxDroite.currentTextChanged.connect(self.choisirSpecialite)

    def choisirSpecialite(self) -> None:
        """Sélectionner une option"""
        self.specialiteSelectionnee = self.comboBoxDroite.currentText()

# ----------------------------------------------------

if __name__ == '__main__':
    import gettext
    gettext.install("piveo")
    app = QApplication(sys.argv)
    config = {
    "Organisme": "Entreprise",
    "Structure": "Département",
    "Personne": "Salarié",
    "Specialite": "Fonctions",
    "BaseDonnees": "salaries.db",
    "CheminPhotos": "photos/salaries/"
    }
    fenetre = FrameDroiteBasse(config=config)
    fenetre.show()
    app.exec()