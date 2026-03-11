#!/usr/bin/python2
# -*- coding: utf-8 -*

"""
afficher la photo de l'élève sélecctionné
et ses informations
"""

import sys, gettext
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel,
							  QApplication, QHBoxLayout, QPushButton, QSpacerItem, QSizePolicy)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import QSize, Qt
from app.gestionnaire_bdd import  GestionnaireBdd
from pathlib import Path
from app.textes_interface import libelle
# ⚠️ IMPORTANT
# ligne ci-dessous -> fonctionnement NORMAL
from builtins import _
# Deux lignes ci-dessous décommmentée -> test if __name__ == "__name__":
# import gettext
# _ = gettext.gettext


icones=["Gnome-go-first.png","Gnome-go-previous.png","Gnome-go-next.png","Gnome-go-last.png", ]

dossier_personnel = Path.home()
dossier_racine = Path(__file__).resolve().parent.parent
fichier_langue = dossier_personnel / ".local" / "piveo" /"configurationLangue.json"

class CadreGauche (QWidget):
    """ Créer la partie gauche de l'interface """
        
    def __init__(self, liste_personnes, recuperer_BDD,configuration_json, parent=None):
        """Constructeur de la frame de gauche et de ses éléments"""
        super().__init__(parent) # constructeur de la classe parente
        self.configuration_json = configuration_json # configuration de l'interface - json
        layout_gauche = QVBoxLayout()  
        # poisition de LayoutGauche dans la fenetre principale de la fenêtreself.LayoutPrincipal(row=0,column=0,rowspan=3,padx=10,pady=2)
        self.modif_bdd = recuperer_BDD
        self.liste_personnes=liste_personnes #liste des personnes
        self.rang=0     #rang de l'élève dans la classe
        self.nbre_pers=0 # nbre élèves
        self.resize(150, 100) # définir une taille fixe pour la fenêtre
        self.repertoire_racine = "" # repertoire du projet
        # Partie haute du layout
        # QGridLayout
        # prenom
        layout_grille = QGridLayout()
        self.prenom = QLabel("-")
        self.prenom.setText(_("Prénom"))
        self.prenom.setStyleSheet("color: #446069; font-weight: bold; font-size: 16px")
        layout_grille.addWidget(self.prenom, 0, 1)
        layout_grille.addWidget(QLabel(_("Prénom :")), 0, 0, alignment=Qt.AlignRight)
        # nom
        self.nom = QLabel()
        self.nom.setText(_("Nom"))
        self.nom.setStyleSheet("color: #446069; font-weight: bold; font-size: 16px")
        layout_grille.addWidget(self.nom, 1, 1)
        layout_grille.addWidget(QLabel(_("Nom :")), 1, 0, alignment=Qt.AlignRight)
        # attachement à layoutGauche
        layout_gauche.addLayout(layout_grille)
        # Layout principal vertical
        layout_milieu = QVBoxLayout()
        # Création du QLabel de l'image
        self.label_image = QLabel()
        self.label_image.setFixedSize(128, 128)
        self.label_image.setStyleSheet("border: 1px solid #666; background-color: #f0f0f0;")
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # Chargement de l'image par défaut
        chemin_defaut = dossier_racine / "ressources" / "fichiers" / "images" / "inconnu.jpg"
        pixmapDefaut = QPixmap(chemin_defaut).scaled(
            128, 128,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.label_image.setPixmap(pixmapDefaut)
        # Puis ajout dans layout vertical principal
        layout_boutons = QHBoxLayout()

        # boutons de défilement
        fonctions = [self.acceder_premier, self.acceder_precedent, self.acceder_suivant, self.acceder_dernier]
        icones = ["Gnome-go-first.png", "Gnome-go-previous.png", "Gnome-go-next.png", "Gnome-go-last.png"]
        self.boutons = []
        for i, icone in enumerate(icones):
            bouton = QPushButton()
            bouton.setIcon(QIcon(str(dossier_racine / "ressources"  / "fichiers" / "icones" / icone)))
            bouton.setIconSize(QSize(24, 24))
            bouton.clicked.connect(fonctions[i])
            layout_boutons.addWidget(bouton)
            self.boutons.append(bouton)
        layout_boutons.setSpacing(6)  # espace horizontal entre flèches

        # Bloc vertical (photo + boutons), avec marges
        bloc_photo = QVBoxLayout()
        bloc_photo.setContentsMargins(10, 10, 10, 10)  # marges autour du bloc
        bloc_photo.setSpacing(10)  # espace entre photo et boutons
        bloc_photo.addWidget(self.label_image, alignment=Qt.AlignCenter)
        bloc_photo.addLayout(layout_boutons)
        # Encapsule le tout dans un widget
        photo_milieu = QWidget()
        photo_milieu.setLayout(bloc_photo)
        # Ajoute à layoutMilieu
        layout_milieu.addWidget(photo_milieu)
        # Ajoute à layoutGauche (comme avant)
        layout_gauche.addLayout(layout_milieu)
		# layout bas
        # affichage des élèves restants
        layout_bas = QVBoxLayout()
        self.num_Ordre_Pers=QLabel() # rang de la Personne
        self.num_Ordre_Pers.setText(_("rang / effectif "))
        layout_bas.addWidget(self.num_Ordre_Pers, alignment=Qt.AlignCenter)
        # affichage de la structure 
        self.structure=QLabel() # label de la structure
        self.structure.setText(_(libelle(configuration_json["Structure"])))
        self.structure.setStyleSheet("color: #76aeba; font-weight: bold; font-size: 11pt;")
        layout_bas.addWidget(self.structure, alignment=Qt.AlignCenter)
        # affichage des options
        self.specialites = QLabel() # permet de changer le texte du label
        self.specialites.setText(_(libelle(configuration_json["Specialite"])))
        self.specialites.setStyleSheet("font-size: 10pt;")
        layout_bas.addWidget(self.specialites, alignment=Qt.AlignCenter)
        # attachement au layout gauche
        layout_gauche.addLayout(layout_bas)

        # Espace vertical fixe de 10 pixels
        spacer = QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
        layout_gauche.addItem(spacer)
        # attachement à la fenêtre principale
        self.setLayout(layout_gauche)

        self.show()

    def acceder_premier(self) -> None:
        """accéder au Premier élève de la liste"""
        self.rang=0
        self.maj()
        
    def acceder_precedent(self) -> None:
        """accéder à l'élève précédent"""
        if (self.rang>0):
            self.rang=self.rang-1
        self.maj()
                
    def acceder_suivant(self) -> None:
        """accéder à l'élève suivant"""
        if (self.rang<len(self.liste_personnes)-1):
            self.rang=self.rang+1
        self.maj()
                
    def acceder_dernier(self):
        """accéder au dernier élève"""
        self.rang=len(self.liste_personnes)-1
        self.maj()
        
    def maj(self) -> None:
        """Mettre à jour l'affichage de l'élève courant si la liste est valide"""
        if not self.liste_personnes or self.rang >= len(self.liste_personnes):
            return  # on ne fait rien si la liste est vide ou le rang est hors limites
        self.maj_nom_prenom()
        self.maj_classe_options()
        self.maj_Photo()
        self.maj_num_Ordre_Pers()

    def effacer_affichage(self) -> None:
        """Effacer les informations affichées en cas de données manquantes"""
        self.prenom.setText("-")
        self.nom.setText("-")
        self.structure.setText("-")
        self.specialites.setText("-")
        self.num_Ordre_Pers.setText("-")
        image_par_defaut = dossier_racine / "fichiers" / "images" / "inconnu.jpg"
        self.label_image.setPixmap(QPixmap(image_par_defaut))   
            
    def maj_Photo(self) -> None:
        """Mise à jour de la photo"""
        nom_image = self.liste_personnes[self.rang][4]
        chemin_image = (
            dossier_racine
            / "ressources"
            / "fichiers"
            / "photos"
            / self.configuration_json["CheminPhotos"]
            / nom_image
        )
        # si l'image existe
        if chemin_image.exists():
            pixmap = QPixmap(str(chemin_image))
        else:
            chemin_defaut = dossier_racine / "fichiers" / "images" / "inconnu.jpg"
            pixmap = QPixmap(str(chemin_defaut))
        self.label_image.setPixmap(pixmap)


    def maj_nom_prenom(self):
        self.prenom.setText(self.liste_personnes[self.rang][0])
        self.nom.setText(self.liste_personnes[self.rang][1])
            
    
    def maj_classe_options(self):
        # Structure (classe / département / parti)
        structure_interne = self.liste_personnes[self.rang][2]
        self.structure.setText(libelle(structure_interne))

        # Options (liste)
        options = self.liste_personnes[self.rang][3]
        options_ui = [libelle(opt) for opt in options] # affichage ui
        texteOptions = " - ".join(options_ui)
        self.specialites.setText(texteOptions)


    def maj_num_Ordre_Pers(self) -> None:
        """mettre à jour le numéro d'ordre de l'élève"""
        if self.nbre_pers==len(self.liste_personnes): # apprentissage
            self.num_Ordre_Pers.setText(str(self.rang+1)+"/"+str(self.nbre_pers))
        else: # test mental
            self.num_Ordre_Pers.setText(str(self.rang//2+1)+"/"+str(self.nbre_pers))  
                
# ----------------------------------------------------
        
if __name__ == '__main__':

    app = QApplication(sys.argv)

    dossier_racine = Path(__file__).resolve().parent.parent

    liste_personnes = [
        ['Sarah', 'Fernandez', '1S1', ['CAM', 'THE'], 'Fernandez_Sarah.jpg'],
        ['Clement', 'Henry', '1S1', ['CAM'], 'Henry_Clement.jpg'],
        ['Emma', 'Petit', 'PSTI2D1', ['ESP'], 'Petit_Emma.jpg']
    ]
    config = {
        "Organisme": "Ecole",
        "Structure": "Classe",
        "Personne": "Élève",
        "Specialite": "Options",
        "BaseDonnees": "eleves.db",
        "CheminPhotos": "eleves/"
    }
    gestionnaire_bdd = GestionnaireBdd

    fenetre = CadreGauche(liste_personnes, gestionnaire_bdd, config)
    fenetre.nbre_pers = len(liste_personnes)
    fenetre.show()
    sys.exit(app.exec_())
