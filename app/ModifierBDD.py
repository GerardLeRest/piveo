#!/usr/bin/python3
# -*- coding: utf-8 -*

"""
Manipulation de la Base de Données
"""

import sqlite3, os
from app.utils import get_repertoire_racine
from pathlib import Path


class ModifierBDD:
    """Manipulation de la BDD"""
    def __init__(self, config, cheminFichier):
        self.config = config
        self.cheminFichier = cheminFichier
        # chemin de la base de donnée
        BASE_DIR = Path(__file__).resolve().parent.parent
        DB_PATH = BASE_DIR / "ressources" / "BaseDonnees" / cheminFichier
        # connexion à la BDD
        self.conn = sqlite3.connect(DB_PATH)
        self.curs = self.conn.cursor()
        self.curs.execute("PRAGMA foreign_keys=on;")
        self.listesPersonnes = []
        self.chargerPersonnes()

    def chargerPersonnes(self):
        """Charge toutes les personnes depuis la BDD"""
        self.listesPersonnes.clear()
        self.curs.execute('''
            SELECT 
                p.prenom, 
                p.nom, 
                p.structure, 
                GROUP_CONCAT(s.specialite, ', '), -- Exemple : "ALL2, TH"

                p.photo
            FROM personnes p
            LEFT JOIN personnes_specialites ps ON ps.id_personne = p.id
            LEFT JOIN specialites s ON s.id = ps.id_specialite
            GROUP BY p.id
        ''')
        # sepcialitesStr correspond à GROUP_CONCAT(s.specialite, ', ')
        for prenom, nom, structure, specialitesStr, photo in self.curs.fetchall():
            # listeSpécialites = ["CAM","THE"] par exemple
            listeSpecialites = specialitesStr.split(', ') if specialitesStr else []
            personne = [prenom, nom, structure, listeSpecialites, photo]
            self.listesPersonnes.append(personne)

    def listerStructures(self):
        """retourne toutes les structures présentes dans la liste des personnes,
        une seule fois chacune, triées alphabétiquement."""
        return sorted(set(personne[2] for personne in self.listesPersonnes))

    def personnesStructure(self, structureNom):
        """Retourne les personnes d’une structure spécifique"""
        listeFiltree = [
            personne for personne in self.listesPersonnes # parcourir une liste
            if personne[2] == structureNom # retourner dans la liste, personnes si on a la condition
        ]
        return listeFiltree
        # OU
        # return [
        #             personne for personne in self.listesPersonnes
        #             if personne[2] == structureNom
        #         ]
    
    def fermerConnexion(self):
        self.conn.close()


# ------------------------------------------------------------------------------
if __name__ == "__main__":
    config = {
        "Organisme": "Entreprise",
        "Structure": "Département",
        "Personne": "Salarié",
        "Specialite": "Fonctions",
        "BaseDonnees": "salaries.db",
        "CheminPhotos": "photos/salaries/"
    }
    modifier_bdd = ModifierBDD(config, config["BaseDonnees"])
    print(modifier_bdd.listerStructures())
