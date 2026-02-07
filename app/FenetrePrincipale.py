#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
# Apprendre ou retrouver le nom/prénom des élèves
# du lycée
"""

import random, copy
from pathlib import Path
from app.FrameGauche import *
from app.FrameDroiteHaute import *
from app.FrameDroiteBasse import *
from builtins import _
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QMenu, QMessageBox
)
from PySide6.QtGui import QPixmap, QAction, QActionGroup
from app.utils import get_repertoire_racine
from app.utils_i18n import ui_value
from pathlib import Path
from builtins import _
from app.GestionLangue import GestionLangue


REPERTOIRE_RACINE = Path(__file__).resolve().parent.parent
FICHIER_LANGUE: Path = Path.home() / ".local" / "piveo" / "config" / "configurationLangue.json"


class Fenetre(QMainWindow):
    """ Créer l'interface graphique et lier les diffentes classes entre elles"""
    
    def __init__(self, config, conn):
        super().__init__()

        self.config = config
        self.conn = conn
        # paramétrage fenêtre
        self.setWindowTitle(_("Piveo - ") + ui_value(self.config["Organisme"]))
        self.setMaximumSize(self.width(), self.height())
        # Instance UNIQUE de ModifierBDD
        self.modifierBDD = ModifierBDD(self.conn)
        # Frames (on passe conn ou modifierBDD)
        self.FrameDrBa = FrameDroiteBasse(config, self.modifierBDD, self)
        self.FrameDrHa = FrameDroiteHaute(self.config, self)
        self.FrameG = FrameGauche(
            self.FrameDrBa.listePersonnes,
            self.modifierBDD,
            self,
            self.config
        )
        # Layout
        widget_central = QWidget()
        layoutPrincipal = QGridLayout(widget_central)
        layoutPrincipal.addWidget(self.FrameG, 0, 0, 2, 1)
        layoutPrincipal.addWidget(self.FrameDrHa, 0, 1)
        layoutPrincipal.addWidget(self.FrameDrBa, 1, 1)
        self.setCentralWidget(widget_central)
        # Connexions
        self.FrameDrBa.boutonVal.clicked.connect(self.configurer)
        self.FrameDrHa.boutVal.clicked.connect(self.verifierRechercher)
        self.FrameDrHa.boutEff.clicked.connect(self.effacer)
        self.FrameDrHa.boutSuite.clicked.connect(self.AllerALaSuite)
        self.FrameDrHa.prenomEntry.returnPressed.connect(self.validerRepNom)
        self.FrameDrHa.nomEntry.returnPressed.connect(self.verifierRechercher)
        self.show() # lancer la fenêtre
        self.menus()
            
    def menus(self) -> None:
        # barre de menus
        menuBar = self.menuBar()
        # menu principal
        menuPrincipal = QMenu(_("Menu"), self)
        # choix de la langue - sous menu de menuPrincipal
        menuLangues = QMenu(_("Langues"), self)
        groupe_langue = QActionGroup(self)
        groupe_langue.setExclusive(True)
        # action des langues
        self.gestionLangue = GestionLangue(FICHIER_LANGUE) # objet lecture/ecriture
        self.actionBrezhoneg = QAction("Brezhoneg", self, checkable=True)
        self.actionBrezhoneg.triggered.connect(lambda: self.changerLangue("br"))
        self.actionEnglish = QAction("English", self, checkable=True)
        self.actionEnglish.triggered.connect(lambda: self.changerLangue("en"))
        self.actionEspagnol = QAction("Español", self, checkable=True)
        self.actionEspagnol.triggered.connect(lambda: self.changerLangue("es"))
        self.actionFrancais = QAction("Français", self, checkable=True)
        self.actionFrancais.triggered.connect(lambda: self.changerLangue("fr"))
        # lier acions au menu et ay groupe langue
        for action in (self.actionBrezhoneg, self.actionEnglish, self.actionEspagnol,
                       self.actionFrancais):
            groupe_langue.addAction(action)
            menuLangues.addAction(action)
        # # récuperation du code de la langue
        langueSelectionnee = self.gestionLangue.lire() 
        self.recuperation_code_langue(langueSelectionnee)
        # action Licence GPL-V3
        actionLicence = QAction(_("Licence GPL-v3"), self)
        actionLicence.triggered.connect(self.afficherLicence)
        # action "quitter"
        actionQuitter = QAction(_("Quitter"), self)
        actionQuitter.triggered.connect(self.close)
        # "sousMenuLangues" -> menu menuPrincipal
        menuPrincipal.addMenu(menuLangues)
        menuPrincipal.addAction(actionLicence)
        menuPrincipal.addAction(actionQuitter)
        # lier le menu menuPrinipal au menuBar
        menuBar.addMenu(menuPrincipal)
        
    def recuperation_code_langue(self, langue)->None:
        "Récupérer le code de la langue"
        if langue == "br":
            self.actionBrezhoneg.setChecked(True)
        elif langue == "en":
            self.actionEnglish.setChecked(True)
        elif langue == "es":
            self.actionEspagnol.setChecked(True)
        else:
            self.actionFrancais.setChecked(True)    
    
    def changerLangue(self, codeLangue) -> None:
        self.gestionLangue.ecrire(codeLangue)
        self.afficherMessage()

    def afficherMessage(self):
        QMessageBox.warning(
            self,
            _("Attention"),
            _("Les changements se feront au prochain démarrage.")
        )
                
    def configurer(self) -> None:
        """ configurer l'application"""
        self.FrameDrHa.effacerReponses()
        if self.FrameDrBa.boutonRadioHaut4.isChecked(): # mode "Rechercher"
            self.FrameDrHa.configRechercher()
            # activer/désactiver zones de saisie 
            self.actDesZonesSaisies()          
        else:
            self.configAutresModes()           
        
    def actDesZonesSaisies(self) -> None:
        """Activer ou désactiver les zones de saisie selon le mode"""
        
        if self.FrameDrBa.boutonRadioBas2.isChecked():  # prénom seul
            self.FrameDrHa.nomEntry.setEnabled(False)
            self.FrameDrHa.nomEntry.setPlaceholderText("")
            self.FrameDrHa.prenomEntry.setEnabled(True)
            self.FrameDrHa.prenomEntry.setFocus()
            
        elif self.FrameDrBa.boutonRadioBas3.isChecked():  # nom seul
            self.FrameDrHa.prenomEntry.setEnabled(False)
            self.FrameDrHa.prenomEntry.setPlaceholderText("")
            self.FrameDrHa.nomEntry.setEnabled(True)
            self.FrameDrHa.nomEntry.setFocus()
           
        else:  # nom + prénom
            self.FrameDrHa.prenomEntry.setEnabled(True)
            self.FrameDrHa.nomEntry.setEnabled(True)
            self.FrameDrHa.prenomEntry.setPlaceholderText(_("Indiquez votre prénom"))
            self.FrameDrHa.nomEntry.setPlaceholderText(_("Indiquez votre nom"))
            self.FrameDrHa.prenomEntry.setFocus()
            
    def configAutresModes(self) -> None:
        self.FrameDrBa.choisirSpecialite()
        self.FrameG.listePersonnes = copy.deepcopy(self.FrameDrBa.listePersonnes)

        # Filtrage par option choisie
        if self.FrameDrBa.specialiteSelectionnee != "TOUS":
            self.enleverPersonnes()
        self.FrameG.nbrePers = len(self.FrameG.listePersonnes)
        self.FrameG.rang = 0
        self.FrameG.numOrdrePers.setText(f"{self.FrameG.rang // 2 + 1}/{self.FrameG.nbrePers}")
        self.FrameDrHa.DesAffichRep()
        if self.FrameDrBa.checkBox.isChecked():
            random.shuffle(self.FrameG.listePersonnes)
        if self.FrameDrBa.boutonRadioBas2.isChecked():  # Prénom seul
            self.effacerNomsOuPrenoms(self.FrameG.listePersonnes, 1)
        if self.FrameDrBa.boutonRadioBas3.isChecked():  # Nom seul
            self.effacerNomsOuPrenoms(self.FrameG.listePersonnes, 0)
        if self.FrameDrBa.boutonRadioHaut2.isChecked():  # Test oral
            self.ajouterBlancsListes(self.FrameG.listePersonnes)
        if self.FrameDrBa.boutonRadioHaut3.isChecked():  # Test écrit
            self.ajouterBlancsListes(self.FrameG.listePersonnes)
            self.FrameDrHa.configTestEcrit()
            self.configTestEcrit()
        else:
            self.configApprentissageTestOral()
        if self.FrameG.listePersonnes and all(len(personne) >= 4 for personne in self.FrameG.listePersonnes):
            self.FrameG.maj()
        else:
            print("Données incomplètes ou non chargées, affichage annulé.")

    def configTestEcrit(self) -> None:
        """Configurer le mode Test Écrit"""
        # Désactiver les boutons (Frame gauche)
        for bouton in self.FrameG.boutons:
            bouton.setEnabled(False)
        # Activer ou désactiver les zones de saisie en fonction du mode
        self.actDesZonesSaisies()

    def configApprentissageTestOral(self) -> None:
        """configurer dans les modes Apprentissage et Test Oral """
        #activer ou désactiver les boutons de la frame de gauche
        self.actDesBoutFrameG()
        self.FrameDrHa.effacerReponses() # effacer réponses
        self.FrameDrHa.desFrameDrHa() #désactiver les boutons et zones de saisie de la frame DH
        
    def actDesBoutFrameG(self) -> None:
        """ activer ou désactiver les boutons de la frame de gauche"""
        # activer les boutons frame gauche si la liste des élèves n'est pas vide
        if len(self.FrameG.listePersonnes)>1:
            for i in range(len(icones)):
                self.FrameG.boutons[i].setEnabled(True) 
        else:
            for i in range(len(icones)):
                self.FrameG.boutons[i].setEnabled(False)
        
    def effacer(self) -> None:
        """Effacer après appui sur le bouton "effacer" de la frame haute droite"""
        expression=self.FrameG.rang % 2 == 0 and self.FrameDrBa.boutonRadioHaut3.isChecked() # rang paire et test écrit
        if expression or self.FrameDrBa.boutonRadioHaut4: #  mode "Rechercher"
            self.FrameDrHa.effacerReponses()
            self.actDesZonesSaisies()

    def enleverPersonnes(self) -> None:
        """enlever les personnes ne faisant pas la spécialité sélectionnée"""
        self.FrameG.listePersonnes = [
            personne for personne in self.FrameG.listePersonnes
            if self.FrameDrBa.specialiteSelectionnee in personne[3]
        ]
    
    def effacerNomsOuPrenoms(self,liste: list ,rang: int):
        """effacer les noms ou les prénoms"""
        for i in range(len(liste)):
                liste[i][rang]=" "
                   
    def ajouterBlancsListes(self,liste:list) -> None:
        """ajouter des blancs ou des ??? dans la liste"""
        i=0        
        while i<(len(liste)):
            tab=list(liste[i])# copie de liste[i]
            if self.FrameDrBa.boutonRadioBas1.isChecked(): #nom et prénom
                tab[0]="???"
                tab[1]="???"
            elif self.FrameDrBa.boutonRadioBas2.isChecked(): # prénom seul
                tab[0]="???"
                tab[1]=""
            else:               # nom seul
                tab[0]=""
                tab[1]="???"
            liste.insert(i,tab)
            i=i+2
            
    def verifierRechercher(self) -> None:
        """lancer la vérification de la réponse"""
        if self.FrameDrBa.boutonRadioHaut3.isChecked(): # mode - Test écrit
            self.verifier()
        elif self.FrameDrBa.boutonRadioHaut4.isChecked(): # mode "Rechercher"
            self.rechercher()
        
    def verifier(self) -> None:
        """Vérifier la réponse dans le mode Test Écrit"""

        if self.FrameG.rang % 2 != 0:
            return  # ne rien faire si ce n’est pas un rang pair

        # Récupération des réponses utilisateur
        nom = self.FrameDrHa.nomEntry.text()
        prenom = self.FrameDrHa.prenomEntry.text()

        # Réponses attendues
        nomAttendu = self.FrameG.listePersonnes[self.FrameG.rang + 1][1]
        prenomAttendu = self.FrameG.listePersonnes[self.FrameG.rang + 1][0]

        mode = self.FrameDrBa.groupeBas.checkedButton().text() 
        match = True

        if self.FrameDrBa.boutonRadioBas1.isChecked() or self.FrameDrBa.boutonRadioBas3.isChecked():  # le nom doit être vérifié
            match &= nom.lower() == nomAttendu.lower()
        if self.FrameDrBa.boutonRadioBas1.isChecked() or self.FrameDrBa.boutonRadioBas2.isChecked():  # le prénom doit être vérifié
            self.FrameDrHa.nomEntry.setEnabled(False) # désactivation du nom
            match &= prenom.lower() == prenomAttendu.lower()

        # Affichage des icones
        # icone = ":/check.png" if match else ":/cross.png" # voir fichier icons_rc et icons_qrc
        cheminIcone = REPERTOIRE_RACINE / "ressources" / "fichiers" / "icones"
        icone = cheminIcone / ("check.png" if match else "cross.png")
        image = QPixmap(str(icone))
        self.FrameDrHa.labelImageGauche.setPixmap(image)
   
        if match:
            self.FrameDrHa.nbreRepExactes += 1

        # Mise à jour du score I / J
        score = f"{self.FrameDrHa.nbreRepExactes}/{self.FrameG.rang // 2 + 1}"
        self.FrameDrHa.nbreRep.setText(score)

        # Avancer dans la liste
        self.FrameG.rang += 1
        if self.FrameG.rang > len(self.FrameG.listePersonnes) - 2:
            self.FrameDrHa.desFrameDrHa()
        else:
            self.FrameG.majNomPrenom()
            self.FrameG.majClasseOptions()
            self.FrameDrHa.boutVal.setEnabled(False)
            self.FrameDrHa.boutEff.setEnabled(False)
            self.FrameDrHa.nomEntry.setEnabled(False)
            self.FrameDrHa.prenomEntry.setEnabled(False)

    def AllerALaSuite(self,event) -> None:
        """voir la réponse et passer à la personne suivant"""
        if self.FrameDrBa.boutonRadioHaut3.isChecked(): #Test écrit
            self.FrameDrHa.effacerReponses()
            if (self.FrameG.rang >= len(self.FrameG.listePersonnes)-1):
                pass
            else:
                self.FrameG.rang=self.FrameG.rang+1
            # avancer
            if (self.FrameG.rang<len(self.FrameG.listePersonnes)):
                #réactivation des boutons
                self.FrameDrHa.boutVal.setEnabled(True)
                self.FrameDrHa.boutEff.setEnabled(True)
                # maj bonnes réponses
                self.FrameDrHa.nbreRep.setText(str(self.FrameDrHa.nbreRepExactes)+"/"+str(self.FrameG.rang//2+1))
                # N° de l'élève en cours
                self.FrameG.numOrdrePers.setText(str(self.FrameG.rang//2+1)+"/"+str(self.FrameG.nbrePers))
                # maj des noms te des prénoms
                self.FrameG.majNomPrenom()
                self.FrameG.majClasseOptions()
                # activation/désactivation des zones de saisie
                if (self.FrameG.listePersonnes[self.FrameG.rang][1]=="???") or (self.FrameG.listePersonnes[self.FrameG.rang][0]=="???"):
                    self.actDesZonesSaisies() #activer/désactiver zones de saisie
                else:
                    self.FrameDrHa.prenomEntry.setEnabled(False)
                    self.FrameDrHa.nomEntry.setEnabled(False)
                    self.FrameDrHa.boutVal.setEnabled(False)
                    self.FrameDrHa.boutEff.setEnabled(False)
                # maj des photos
                self.FrameG.majPhoto()
                if (self.FrameG.rang==len(self.FrameG.listePersonnes)-1):
                    self.FrameDrHa.desFrameDrHa()
        else:
            pass
    
    def rechercher(self):
        """Rechercher un ou plusieurs personnes dans tout l'organisme selon le nom, prénom ou les deux"""

        self.FrameG.listePersonnes = []
        self.FrameG.rang = 0

        # Lecture des champs et mise en forme
        nom = self.FrameDrHa.nomEntry.text().lower().strip()
        prenom = self.FrameDrHa.prenomEntry.text().lower().strip()
        mode = self.FrameDrBa.groupeBas.checkedButton().text()

        # Boucle sur tous les élèves de l'établissement
        for eleve in self.modifierBDD.listesPersonnes:
            prenom_eleve = eleve[0].lower().strip()
            nom_eleve = eleve[1].lower().strip()
            # conditions               
            if mode == _("Prenom"):
                condition = (prenom == prenom_eleve)
            elif mode == _("Nom"):
                condition = (nom == nom_eleve)
            else:
                condition = (prenom == prenom_eleve and nom == nom_eleve)

            if condition:
                self.FrameG.listePersonnes.append(eleve)
        # Après avoir collecté tous les résultats, mise à jour
        self.FrameG.nbrePers = len(self.FrameG.listePersonnes)
        if self.FrameG.nbrePers > 0:
            self.FrameG.rang = 0
            self.FrameG.numOrdrePers.setText(f"1/{self.FrameG.nbrePers}")
            self.FrameG.majNomPrenom()
            self.FrameG.majClasseOptions()
            self.FrameG.majPhoto()
            # activation/désactivation boutons sous image - rechercher
            if self.FrameG.nbrePers<=1:
                for bouton in self.FrameG.boutons:
                    bouton.setEnabled(False)
            else:
                for bouton in self.FrameG.boutons:
                    bouton.setEnabled(True)
        else:
            self.FrameG.numOrdrePers.setText(_("0/0"))
            QMessageBox.information(self, _("Aucun résultat"), _("Aucune personne trouvée."))

    def validerRepNom(self):
        """Valider l'entrée prénom selon le mode sélectionné, ou passer au champ nom"""

        modeRecherche = self.FrameDrBa.groupeBas.checkedButton().text()
        modeGeneral = self.FrameDrBa.groupeHaut.checkedButton().text()

        if self.FrameDrBa.boutonRadioBas2.isChecked():  # Prenom
            if self.FrameDrBa.boutonRadioHaut3.isChecked():  # Test écrit
                self.verifier()
            else:
                self.rechercher()
        else:
            # Passer au champ Nom
            self.focusNextChild()
                        
    def afficherLicence(self):
        texte = _(
            "Ce logiciel est distribué sous licence GNU GPL version 3.\n\n"
            "Vous pouvez le redistribuer et/ou le modifier selon les termes de cette licence.\n\n"
            "Plus d'informations : https://www.gnu.org/licenses/gpl-3.0.html\n\n"
            "© 2026 Gérard Le Rest - ge.lerest@gmail.com"
        )
        QMessageBox.information(self, _("GPL-v3"), texte)
