#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
# Apprendre ou retrouver le nom/prénom des élèves
# du lycée
"""

import random, copy, gettext
from pathlib import Path
from app.cadre_gauche import *
from app.cadre_droit_haut import *
from app.cadre_droit_bas import *
from PySide6.QtWidgets import (
    QMainWindow, QWidget,
    QMenu, QMessageBox
)
from PySide6.QtGui import QPixmap, QAction, QActionGroup
from app.textes_interface import libelle
from pathlib import Path
from builtins import _
from app.gestion_langue import GestionLangue
from builtins import _

REPERTOIRE_RACINE = Path(__file__).resolve().parent.parent
FICHIER_LANGUE: Path = Path.home() / ".local" / "piveo" / "configurations_json" / "configurationLangue.json"

class Fenetre(QMainWindow):
    """ Créer l'interface graphique et lier les diffentes classes entre elles"""
    
    def __init__(self, configuration_json, connexion_json):
        super().__init__()

        self.configuration_json = configuration_json
        self.connexion_json = connexion_json
        # paramétrage fenêtre
        self.setWindowTitle(_("Piveo - ") + libelle(self.configuration_json["Organisme"]))
        self.setMaximumSize(self.width(), self.height())
        # Instance UNIQUE de ModifierBDD
        self.gestionnaire_bdd = GestionnaireBdd(self.connexion_json)
        # Frames (on passe conn ou modifierBDD)
        self.cadre_dr_bas = CadreDroitBas(configuration_json, self.gestionnaire_bdd, self)
        self.cadre_dr_haut = CadreDroiteHaut(self.configuration_json, self)
        self.cadre_ga = CadreGauche(
            self.cadre_dr_bas.liste_personnes,
            self.gestionnaire_bdd,
            self.configuration_json,
            self
        )
        # Layout
        widget_central = QWidget()
        layout_principal = QGridLayout(widget_central)
        layout_principal.addWidget(self.cadre_ga, 0, 0, 2, 1)
        layout_principal.addWidget(self.cadre_dr_haut, 0, 1)
        layout_principal.addWidget(self.cadre_dr_bas, 1, 1)
        self.setCentralWidget(widget_central)
        # Connexions
        self.cadre_dr_bas.bouton_valider.clicked.connect(self.configurer)
        self.cadre_dr_haut.bout_valider.clicked.connect(self.verifier_rechercher)
        self.cadre_dr_haut.bout_effacer.clicked.connect(self.effacer)
        self.cadre_dr_haut.bout_suite.clicked.connect(self.aller_a_la_suite)
        self.cadre_dr_haut.prenom_entree.returnPressed.connect(self.valider_rep_nom)
        self.cadre_dr_haut.nom_entree.returnPressed.connect(self.verifier_rechercher)
        self.show() # lancer la fenêtre
        self.menus()
            
    def menus(self) -> None:
        # barre de menus
        menu_bar = self.menuBar()
        # menu principal
        menu_principal = QMenu(_("Menu"), self)
        # choix de la langue - sous menu de menuPrincipal
        menu_langues = QMenu(_("Langues"), self)
        groupe_langue = QActionGroup(self)
        groupe_langue.setExclusive(True)
        # action des langues
        self.gestion_langue = GestionLangue(FICHIER_LANGUE) # objet lecture/ecriture
        self.action_brezhoneg = QAction("Brezhoneg", self, checkable=True)
        self.action_brezhoneg.triggered.connect(lambda: self.changer_langue("br"))
        self.action_english = QAction("English", self, checkable=True)
        self.action_english.triggered.connect(lambda: self.changer_langue("en"))
        self.action_espagnol = QAction("Español", self, checkable=True)
        self.action_espagnol.triggered.connect(lambda: self.changer_langue("es"))
        self.action_francais = QAction("Français", self, checkable=True)
        self.action_francais.triggered.connect(lambda: self.changer_langue("fr"))
        # lier acions au menu et ay groupe langue
        for action in (self.action_brezhoneg, self.action_english, self.action_espagnol,
                       self.action_francais):
            groupe_langue.addAction(action)
            menu_langues.addAction(action)
        # # récuperation du code de la langue
        langue_selectionnee = self.gestion_langue.lire() 
        self.recuperation_code_langue(langue_selectionnee)
        # action Licence GPL-V3
        action_licence = QAction(_("Licence GPL-v3"), self)
        action_licence.triggered.connect(self.afficher_licence)
        # action "quitter"
        action_quitter = QAction(_("Quitter"), self)
        action_quitter.triggered.connect(self.close)
        # "sousMenuLangues" -> menu menuPrincipal
        menu_principal.addMenu(menu_langues)
        menu_principal.addAction(action_licence)
        menu_principal.addAction(action_quitter)
        # lier le menu menuPrinipal au menuBar
        menu_bar.addMenu(menu_principal)
        
    def recuperation_code_langue(self, langue)->None:
        "Récupérer le code de la langue"
        if langue == "br":
            self.action_brezhoneg.setChecked(True)
        elif langue == "en":
            self.action_english.setChecked(True)
        elif langue == "es":
            self.action_espagnol.setChecked(True)
        else:
            self.action_francais.setChecked(True)    
    
    def changer_langue(self, codeLangue) -> None:
        """enregistrer la nouvelle langue"""
        self.gestion_langue.ecrire(codeLangue)
        self.afficher_message()

    def afficher_message(self):
        """message d'averissement pour le chgt de la langue"""
        QMessageBox.warning(
            self,
            _("Attention"),
            _("Les changements se feront au prochain démarrage.")
        )
                
    def configurer(self) -> None:
        """ configurer l'application"""
        self.cadre_dr_haut.effacer_reponses()
        if self.cadre_dr_bas.bouton_rechercher.isChecked(): # mode "Rechercher"
            self.cadre_dr_haut.config_rechercher()
            # activer/désactiver zones de saisie 
            self.act_des_zones_saisies()          
        else:
            self.config_autres_modes()           
        
    def act_des_zones_saisies(self) -> None:
        """Activer ou désactiver les zones de saisie selon le mode"""
        
        if self.cadre_dr_bas.bouton_radio_bas2.isChecked():  # prénom seul
            self.cadre_dr_haut.nom_entree.setEnabled(False)
            self.cadre_dr_haut.nom_entree.setPlaceholderText("")
            self.cadre_dr_haut.prenom_entree.setEnabled(True)
            self.cadre_dr_haut.prenom_entree.setFocus()
            
        elif self.cadre_dr_bas.boutonRadioBas3.isChecked():  # nom seul
            self.cadre_dr_haut.prenom_entree.setEnabled(False)
            self.cadre_dr_haut.prenom_entree.setPlaceholderText("")
            self.cadre_dr_haut.nom_entree.setEnabled(True)
            self.cadre_dr_haut.nom_entree.setFocus()
           
        else:  # nom + prénom
            self.cadre_dr_haut.prenom_entree.setEnabled(True)
            self.cadre_dr_haut.nom_entree.setEnabled(True)
            self.cadre_dr_haut.prenom_entree.setPlaceholderText(_("Indiquez votre prénom"))
            self.cadre_dr_haut.nom_entree.setPlaceholderText(_("Indiquez votre nom"))
            self.cadre_dr_haut.prenom_entree.setFocus()
            
    def config_autres_modes(self) -> None:
        self.cadre_dr_bas.choisir_specialite()
        self.cadre_ga.liste_personnes = copy.deepcopy(self.cadre_dr_bas.liste_personnes)

        # Filtrage par option choisie
        if self.cadre_dr_bas.specialite_selectionnee != "TOUS":
            self.enlever_Personnes()
        self.cadre_ga.nbre_pers = len(self.cadre_ga.liste_personnes)
        self.cadre_ga.rang = 0
        self.cadre_ga.num_Ordre_Pers.setText(f"{self.cadre_ga.rang // 2 + 1}/{self.cadre_ga.nbre_pers}")
        self.cadre_dr_haut.Des_Affich_Rep()
        if self.cadre_dr_bas.checkBox.isChecked():
            random.shuffle(self.cadre_ga.liste_personnes)
        if self.cadre_dr_bas.bouton_radio_bas2.isChecked():  # Prénom seul
            self.effacer_noms_ou_prenoms(self.cadre_ga.liste_personnes, 1)
        if self.cadre_dr_bas.boutonRadioBas3.isChecked():  # Nom seul
            self.effacer_noms_ou_prenoms(self.cadre_ga.liste_personnes, 0)
        if self.cadre_dr_bas.bouton_mental.isChecked():  # Test oral
            self.ajouter_blancs_listes(self.cadre_ga.liste_personnes)
        if self.cadre_dr_bas.bouton_ecrit.isChecked():  # Test écrit
            self.ajouter_blancs_listes(self.cadre_ga.liste_personnes)
            self.cadre_dr_haut.config_test_ecrit()
            self.config_test_ecrit()
        else:
            self.config_apprentissage_test_oral()
        if self.cadre_ga.liste_personnes and all(len(personne) >= 4 for personne in self.cadre_ga.liste_personnes):
            self.cadre_ga.maj()
        else:
            print("Données incomplètes ou non chargées, affichage annulé.")

    def config_test_ecrit(self) -> None:
        """Configurer le mode Test Écrit"""
        # Désactiver les boutons (Frame gauche)
        for bouton in self.cadre_ga.boutons:
            bouton.setEnabled(False)
        # Activer ou désactiver les zones de saisie en fonction du mode
        self.act_des_zones_saisies()

    def config_apprentissage_test_oral(self) -> None:
        """configurer dans les modes Apprentissage et Test Oral """
        #activer ou désactiver les boutons de la frame de gauche
        self.act_des_bout_cadre_G()
        self.cadre_dr_haut.effacer_reponses() # effacer réponses
        self.cadre_dr_haut.des_cadre_Dr_Ha() #désactiver les boutons et zones de saisie de la frame DH
        
    def act_des_bout_cadre_G(self) -> None:
        """ activer ou désactiver les boutons de la frame de gauche"""
        # activer les boutons frame gauche si la liste des élèves n'est pas vide
        if len(self.cadre_ga.liste_personnes)>1:
            for i in range(len(icones)):
                self.cadre_ga.boutons[i].setEnabled(True) 
        else:
            for i in range(len(icones)):
                self.cadre_ga.boutons[i].setEnabled(False)
        
    def effacer(self) -> None:
        """Effacer après appui sur le bouton "effacer" de la frame haute droite"""
        expression=self.cadre_ga.rang % 2 == 0 and self.cadre_dr_bas.bouton_ecrit.isChecked() # rang paire et test écrit
        if expression or self.cadre_dr_bas.bouton_rechercher: #  mode "Rechercher"
            self.cadre_dr_haut.effacer_reponses()
            self.act_des_zones_saisies()

    def enlever_Personnes(self) -> None:
        """enlever les personnes ne faisant pas la spécialité sélectionnée"""
        self.cadre_ga.liste_personnes = [
            personne for personne in self.cadre_ga.liste_personnes
            if self.cadre_dr_bas.specialite_selectionnee in personne[3]
        ]
    
    def effacer_noms_ou_prenoms(self,liste: list ,rang: int):
        """effacer les noms ou les prénoms"""
        for i in range(len(liste)):
                liste[i][rang]=" "
                   
    def ajouter_blancs_listes(self,liste:list) -> None:
        """ajouter des blancs ou des ??? dans la liste"""
        i=0        
        while i<(len(liste)):
            tab=list(liste[i])# copie de liste[i]
            if self.cadre_dr_bas.bouton_radio_bas1.isChecked(): #nom et prénom
                tab[0]="???"
                tab[1]="???"
            elif self.cadre_dr_bas.bouton_radio_bas2.isChecked(): # prénom seul
                tab[0]="???"
                tab[1]=""
            else:               # nom seul
                tab[0]=""
                tab[1]="???"
            liste.insert(i,tab)
            i=i+2
            
    def verifier_rechercher(self) -> None:
        """lancer la vérification de la réponse"""
        if self.cadre_dr_bas.bouton_ecrit.isChecked(): # mode - Test écrit
            self.verifier()
        elif self.cadre_dr_bas.bouton_rechercher.isChecked(): # mode "Rechercher"
            self.rechercher()
        
    def verifier(self) -> None:
        """Vérifier la réponse dans le mode Test Écrit"""

        if self.cadre_ga.rang % 2 != 0:
            return  # ne rien faire si ce n’est pas un rang pair

        # Récupération des réponses utilisateur
        nom = self.cadre_dr_haut.nom_entree.text()
        prenom = self.cadre_dr_haut.prenom_entree.text()

        # Réponses attendues
        nom_attendu = self.cadre_ga.liste_personnes[self.cadre_ga.rang + 1][1]
        prenom_attendu = self.cadre_ga.liste_personnes[self.cadre_ga.rang + 1][0]

        mode = self.cadre_dr_bas.groupe_bas.checkedButton().text() 
        match = True

        if self.cadre_dr_bas.bouton_radio_bas1.isChecked() or self.cadre_dr_bas.boutonRadioBas3.isChecked():  # le nom doit être vérifié
            match &= nom.lower() == nom_attendu.lower()
        if self.cadre_dr_bas.bouton_radio_bas1.isChecked() or self.cadre_dr_bas.bouton_radio_bas2.isChecked():  # le prénom doit être vérifié
            self.cadre_dr_haut.nom_entree.setEnabled(False) # désactivation du nom
            match &= prenom.lower() == prenom_attendu.lower()

        # Affichage des icones
        # icone = ":/check.png" if match else ":/cross.png" # voir fichier icons_rc et icons_qrc
        chemin_icone = REPERTOIRE_RACINE / "ressources" / "fichiers" / "icones"
        icone = chemin_icone / ("check.png" if match else "cross.png")
        image = QPixmap(str(icone))
        self.cadre_dr_haut.label_image_gauche.setPixmap(image)
   
        if match:
            self.cadre_dr_haut.nbre_rep_exactes += 1

        # Mise à jour du score I / J
        score = f"{self.cadre_dr_haut.nbre_rep_exactes}/{self.cadre_ga.rang // 2 + 1}"
        self.cadre_dr_haut.nbre_rep.setText(score)

        # Avancer dans la liste
        self.cadre_ga.rang += 1
        if self.cadre_ga.rang > len(self.cadre_ga.liste_personnes) - 2:
            self.cadre_dr_haut.des_cadre_Dr_Ha()
        else:
            self.cadre_ga.maj_nom_prenom()
            self.cadre_ga.maj_classe_options()
            self.cadre_dr_haut.bout_valider.setEnabled(False)
            self.cadre_dr_haut.bout_effacer.setEnabled(False)
            self.cadre_dr_haut.nom_entree.setEnabled(False)
            self.cadre_dr_haut.prenom_entree.setEnabled(False)

    def aller_a_la_suite(self,event) -> None:
        """voir la réponse et passer à la personne suivant"""
        if self.cadre_dr_bas.bouton_ecrit.isChecked(): #Test écrit
            self.cadre_dr_haut.effacer_reponses()
            if (self.cadre_ga.rang >= len(self.cadre_ga.liste_personnes)-1):
                pass
            else:
                self.cadre_ga.rang=self.cadre_ga.rang+1
            # avancer
            if (self.cadre_ga.rang<len(self.cadre_ga.liste_personnes)):
                #réactivation des boutons
                self.cadre_dr_haut.bout_valider.setEnabled(True)
                self.cadre_dr_haut.bout_effacer.setEnabled(True)
                # maj bonnes réponses
                self.cadre_dr_haut.nbre_rep.setText(str(self.cadre_dr_haut.nbre_rep_exactes)+"/"+str(self.cadre_ga.rang//2+1))
                # N° de l'élève en cours
                self.cadre_ga.num_Ordre_Pers.setText(str(self.cadre_ga.rang//2+1)+"/"+str(self.cadre_ga.nbre_pers))
                # maj des noms te des prénoms
                self.cadre_ga.maj_nom_prenom()
                self.cadre_ga.maj_classe_options()
                # activation/désactivation des zones de saisie
                if (self.cadre_ga.liste_personnes[self.cadre_ga.rang][1]=="???") or (self.cadre_ga.liste_personnes[self.cadre_ga.rang][0]=="???"):
                    self.act_des_zones_saisies() #activer/désactiver zones de saisie
                else:
                    self.cadre_dr_haut.prenom_entree.setEnabled(False)
                    self.cadre_dr_haut.nom_entree.setEnabled(False)
                    self.cadre_dr_haut.bout_valider.setEnabled(False)
                    self.cadre_dr_haut.bout_effacer.setEnabled(False)
                # maj des photos
                self.cadre_ga.maj_Photo()
                if (self.cadre_ga.rang==len(self.cadre_ga.liste_personnes)-1):
                    self.cadre_dr_haut.des_cadre_Dr_Ha()
        else:
            pass
    
    def rechercher(self):
        """Rechercher un ou plusieurs personnes dans tout l'organisme selon le nom, prénom ou les deux"""

        self.cadre_ga.liste_personnes = []
        self.cadre_ga.rang = 0

        # Lecture des champs et mise en forme
        nom = self.cadre_dr_haut.nom_entree.text().lower().strip()
        prenom = self.cadre_dr_haut.prenom_entree.text().lower().strip()
        mode = self.cadre_dr_bas.groupe_bas.checkedButton().text()

        # Boucle sur tous les élèves de l'établissement
        for eleve in self.gestionnaire_bdd.liste_personnes:
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
                self.cadre_ga.liste_personnes.append(eleve)
        # Après avoir collecté tous les résultats, mise à jour
        self.cadre_ga.nbre_pers = len(self.cadre_ga.liste_personnes)
        if self.cadre_ga.nbre_pers > 0:
            self.cadre_ga.rang = 0
            self.cadre_ga.num_Ordre_Pers.setText(f"1/{self.cadre_ga.nbre_pers}")
            self.cadre_ga.maj_nom_prenom()
            self.cadre_ga.maj_classe_options()
            self.cadre_ga.maj_Photo()
            # activation/désactivation boutons sous image - rechercher
            if self.cadre_ga.nbre_pers<=1:
                for bouton in self.cadre_ga.boutons:
                    bouton.setEnabled(False)
            else:
                for bouton in self.cadre_ga.boutons:
                    bouton.setEnabled(True)
        else:
            self.cadre_ga.num_Ordre_Pers.setText(_("0/0"))
            QMessageBox.information(self, _("Aucun résultat"), _("Aucune personne trouvée."))

    def valider_rep_nom(self):
        """Valider l'entrée prénom selon le mode sélectionné, ou passer au champ nom"""

        modeRecherche = self.cadre_dr_bas.groupe_bas.checkedButton().text()
        modeGeneral = self.cadre_dr_bas.groupe_haut.checkedButton().text()

        if self.cadre_dr_bas.bouton_radio_bas2.isChecked():  # Prenom
            if self.cadre_dr_bas.bouton_ecrit.isChecked():  # Test écrit
                self.verifier()
            else:
                self.rechercher()
        else:
            # Passer au champ Nom
            self.focusNextChild()
                        
    def afficher_licence(self):
        texte = _(
            "Ce logiciel est distribué sous licence GNU GPL version 3.\n\n"
            "Vous pouvez le redistribuer et/ou le modifier selon les termes de cette licence.\n\n"
            "Plus d'informations : https://www.gnu.org/licenses/gpl-3.0.html\n\n"
            "© 2026 Gérard Le Rest - ge.lerest@gmail.com"
        )
        QMessageBox.information(self, _("GPL-v3"), texte)