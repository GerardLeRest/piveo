#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Manipulation de la base de données SQLite.

Ce module :
- ne connaît PAS les chemins
- ne connaît PAS les fichiers JSON
- reçoit uniquement une connexion SQLite
"""

import sqlite3


class GestionnaireBdd:
    """Classe de manipulation des données de la base"""

    def __init__(self, conn: sqlite3.Connection):
        """
        Initialise la classe avec une connexion SQLite déjà ouverte.
        """
        self.conn = conn
        self.curs = self.conn.cursor()
        # Activer les clés étrangères (important avec SQLite)
        self.curs.execute("PRAGMA foreign_keys = ON;")
        # Liste interne des personnes chargées
        self.liste_personnes = []
        # Chargement initial des données
        self.charger_personnes()

    def charger_personnes(self):
        """
        Charge toutes les personnes depuis la base de données
        et les stocke dans .
        """
        self.liste_personnes.clear()
        self.curs.execute("""
            SELECT 
                p.prenom,
                p.nom,
                p.structure,
                GROUP_CONCAT(s.specialite, ', '),
                p.photo
            FROM personnes p
            LEFT JOIN personnes_specialites ps ON ps.id_personne = p.id
            LEFT JOIN specialites s ON s.id = ps.id_specialite
            GROUP BY p.id
        """)
        for prenom, nom, structure, specialites_str, photo in self.curs.fetchall():
            # Conversion des spécialités en liste
            liste_specialites = (
                specialites_str.split(', ')
                if specialites_str else []
            )
            personne = [
                prenom,
                nom,
                structure,
                liste_specialites,
                photo
            ]
            self.liste_personnes.append(personne)

    def lister_structures(self):
        """
        Retourne la liste des structures présentes dans la base,
        sans doublon et triée alphabétiquement.
        """
        return sorted(
            set(personne[2] for personne in self.liste_personnes)
        )

    def personnes_structure(self, structure_nom: str):
        """
        Retourne la liste des personnes appartenant à une structure donnée.
        """
        return [
            personne
            for personne in self.liste_personnes
            if personne[2] == structure_nom
        ]

    def fermer_connexion(self):
        """
        Ferme proprement la connexion à la base de données.
        """
        self.conn.close()

