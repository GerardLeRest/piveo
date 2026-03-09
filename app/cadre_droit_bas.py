#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
# selection du mode de fonctionnement
# (apprentissage, test mental, test ecrit, Rechercher)
# choix de la classe et de l'option
"""

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QRadioButton, QPushButton, QGridLayout, QLabel, QComboBox, QCheckBox, QButtonGroup
from app.gestionnaire_bdd import GestionnaireBdd
from PySide6.QtWidgets import QApplication
from app.textes_interface import libelle
from builtins import _
import sys

class CadreDroitBas (QWidget):
    """ Créer la partie droite basse de l'interface """
    def __init__(self, configuration_json, gestionnaire_bdd, fenetre = None ):
        """Constructeur de la frame de droite et de ses éléments"""
        # constructeur de la classe parente
        super().__init__(fenetre)
        self.configuration_json = configuration_json # configuration de l'interface - json
        self.modif_BDD = gestionnaire_bdd
        self.liste_personnes = []  # liste des élèves de la classe sélectionnée
        self.liste_specialites = []  # liste des options des élèves de la classese

        self.specialite_selectionnee = ""  # option sélectionnée

        layout_bas_droit = QVBoxLayout()
        layout_bas_droit.setSpacing(10)
        layout_boutons_radios_haut = QHBoxLayout()
        # boutons radio des modes
        self.bouton_apprentissage = QRadioButton(_("Apprentissage"))
        self.bouton_mental = QRadioButton(_("Test mental"))
        self.bouton_ecrit = QRadioButton(_("Test ecrit"))
        self.bouton_rechercher = QRadioButton(_("Rechercher"))
        # toolTips
        self.bouton_apprentissage.setToolTip(_("Faire défiler les élèves"))
        self.bouton_mental.setToolTip(_("Deviner mentalement lorsque les noms sont masqués"))
        self.bouton_ecrit.setToolTip(_("Test écrit avec les deux champs ci-dessus"))
        self.bouton_rechercher.setToolTip(_("Rechercher un ou plusieurs personnes avec les champs ci-dessus"))
        # regroupement
        self.groupe_haut = QButtonGroup()
        self.groupe_haut.addButton(self.bouton_apprentissage)
        self.groupe_haut.addButton(self.bouton_mental)
        self.groupe_haut.addButton(self.bouton_ecrit)
        self.groupe_haut.addButton(self.bouton_rechercher)
        # insetion dans le layout
        layout_boutons_radios_haut.addWidget(self.bouton_apprentissage)
        layout_boutons_radios_haut.addWidget(self.bouton_mental)
        layout_boutons_radios_haut.addWidget(self.bouton_ecrit)
        layout_boutons_radios_haut.addWidget(self.bouton_rechercher)
         #bouton radi 1 est sélectionné
        self.bouton_apprentissage.setChecked(True)
        #rattachement au layout principal de la classe
        layout_bas_droit.addLayout(layout_boutons_radios_haut)
        
        # Combobox - QGridLayout
        layout_Grille = QGridLayout()
        layout_Grille.setSpacing(10)
         # labels)
        layout_Grille.addWidget(QLabel(_(libelle(self.configuration_json["Structure"]))), 0, 0)
        layout_Grille.addWidget(QLabel(_(libelle(self.configuration_json["Specialite"]))), 0, 1)
        ## ComboBox
        self.comboBox_Gauche = QComboBox()
        self.comboBox_droite = QComboBox()
        layout_Grille.addWidget(self.comboBox_Gauche,1,0)
        layout_Grille.addWidget(self.comboBox_droite,1,1)
        layout_bas_droit.addLayout(layout_Grille)
        # création de la liste des classes
        classesRangees = sorted(self.liste_des_structures())  # crée une nouvelle liste triée
        classes_ui = [libelle(c) for c in classesRangees]
        self.comboBox_Gauche.addItems(classes_ui)
        self.comboBox_Gauche.currentTextChanged.connect(self.choisir_structure_specialites)
        # checkbutton Aléatoite
        layoutCheckBox = QHBoxLayout()
        self.checkBox = QCheckBox(_("Aléatoire"))
        layoutCheckBox.addWidget(self.checkBox)
        layout_bas_droit.addLayout(layoutCheckBox)
        # boutons radios avec/sans nom prénoms
        layoutBoutonsRadiosBas = QHBoxLayout()
        self.groupe_bas = QButtonGroup()
        self.bouton_radio_bas1 = QRadioButton(_("Prenom+Nom"))
        self.bouton_radio_bas2 = QRadioButton(_("Prenom"))
        self.boutonRadioBas3 = QRadioButton(_("Nom"))
        # regroupement
        self.groupe_bas.addButton(self.bouton_radio_bas1)
        self.groupe_bas.addButton(self.bouton_radio_bas2)
        self.groupe_bas.addButton(self.boutonRadioBas3)
        # attachement au layout horizontal
        layoutBoutonsRadiosBas.addWidget(self.bouton_radio_bas1)
        layoutBoutonsRadiosBas.addWidget(self.bouton_radio_bas2)
        layoutBoutonsRadiosBas.addWidget(self.boutonRadioBas3)
         #bouton radi 1 est sélectionné
        self.bouton_radio_bas1.setChecked(True)
        layout_bas_droit.addLayout(layoutBoutonsRadiosBas)
        
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
        self.bouton_valider = QPushButton(_("Valider"))
        self.bouton_valider.setFixedWidth(120)
        self.bouton_valider.setStyleSheet(validerStyle)
        self.bouton_valider.clicked.connect(self.config_rechercher)

        # Centrer le bouton
        layout_bouton = QHBoxLayout()
        layout_bouton.addStretch()
        layout_bouton.addWidget(self.bouton_valider)
        layout_bouton.addStretch()

        # Ajouter au layout principal du bas
        layout_bas_droit.addSpacing(10)  # petit espace avant le bouton
        layout_bas_droit.addLayout(layout_bouton)
        # créer la liste des options
        self.creer_combo_specialites()

    # ancrer le layout principal à la fenêtre
        self.setLayout(layout_bas_droit)

        self.show()
        
    def liste_des_structures(self) -> list:
        """Renvoie la liste des structures de l'organisme"""
        structures = self.modif_BDD.lister_structures()
        if self.configuration_json["Organisme"] == "Ecole":
            phrase = _("- choisir une %(structure)s -") % {
                "structure": self.configuration_json["Structure"]
                }
        else:
            phrase = _("- choisir un %(structure)s -") % {
                "structure": self.configuration_json["Structure"]
                }
        return [phrase] + structures

    def config_rechercher(self) -> None:
        """activer/désactiver les listes les comboBox, des radiobuttons
           et des labels"""
        if self.bouton_rechercher.isChecked():
            # désactiver les radiobuttons
            # self.boutonRadioHaut1.setEnabled(False)
            # self.boutonRadioHaut2.setEnabled(False)
            # self.boutonRadioHaut3.setEnabled(False)
            # self.boutonRadioHaut4.setEnabled(False)
            # désactiver les listes des comboBox
            self.comboBox_Gauche.setEnabled(False)
            self.comboBox_droite.setEnabled(False)
        else:
            # activer les listes des comboBox
            self.comboBox_Gauche.setEnabled(True)
            self.comboBox_droite.setEnabled(True)
            # activer les radiobuttons
            self.bouton_apprentissage.setEnabled(True)
            self.bouton_mental.setEnabled(True)
            self.bouton_ecrit.setEnabled(True)
            self.bouton_rechercher.setEnabled(True)

    def definir_ordre_defilement(self) -> None :
        """Définir l'ordre de défilement"""
        self.ordreAleatoire = self.checkBox.isChecked() 

    def choisir_structure_specialites(self) -> None:
        """Choisir la structure et mettre à jour les personnes et les spécialités"""
        structure_choisie = self.comboBox_Gauche.currentText()
        self.liste_personnes = self.modif_BDD.personnes_structure(structure_choisie)

        # Crée les options présentes uniquement dans cette classe
        self.liste_specialites = self.creer_specialites()

        # Met à jour la combobox des options (ligne à garder si elle suit)
        self.creer_combo_specialites()

    def creer_specialites(self) -> list:
        """Créer la liste des spécialités présentes uniquement dans la classe sélectionnée"""
        liste_specialites = []
        for eleve in self.liste_personnes:
            options = eleve[3]  # Index 2 = liste des options (ex: ['ALL2', 'CAM'])
            for option in options:
                if option not in liste_specialites:
                    liste_specialites.append(option)
        liste_specialites = sorted(liste_specialites)
        liste_specialites.insert(0, "TOUS")
        self.liste_specialites = liste_specialites
        return liste_specialites
    
    def creer_combo_specialites(self) -> None:
        """Créer la liste déroulante des spécialités sans déclencher d'événement parasite"""
        #self.comboBoxDroite.blockSignals(True)  # Empêche les signaux lors de la modification
        self.comboBox_droite.clear()
        self.comboBox_droite.addItems(self.liste_specialites)
        self.comboBox_droite.setCurrentIndex(0)  # Facultatif : force "TOUS" si besoin
        #self.comboBoxDroite.blockSignals(False)
        self.comboBox_droite.currentTextChanged.connect(self.choisir_specialite)

    def choisir_specialite(self) -> None:
        """Sélectionner une option"""
        self.specialite_selectionnee = self.comboBox_droite.currentText()

# ----------------------------------------------------

if __name__ == '__main__':
    # import gettext
    # gettext.install("piveo")
    # app = QApplication(sys.argv)
    # config = {
    # "Organisme": "Entreprise",
    # "Structure": "Département",
    # "Personne": "Salarié",
    # "Specialite": "Fonctions",
    # "BaseDonnees": "salaries.db",
    # "CheminPhotos": "photos/salaries/"
    # }
    # fenetre = CadreDroitBas(configuration=config)
    # fenetre.show()
    # app.exec()
    print("Module utilisé dans l'application principale")