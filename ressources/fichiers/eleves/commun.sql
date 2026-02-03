PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS personnes_specialites;
DROP TABLE IF EXISTS personnes;
DROP TABLE IF EXISTS specialites;

CREATE TABLE personnes (
  id        INTEGER PRIMARY KEY,
  prenom    TEXT NOT NULL,
  nom       TEXT NOT NULL,
  structure TEXT,
  photo     TEXT
);

CREATE TABLE specialites (
  id         INTEGER PRIMARY KEY,
  specialite TEXT NOT NULL UNIQUE
);

CREATE TABLE personnes_specialites (
  id_personne  INTEGER NOT NULL,
  id_specialite INTEGER NOT NULL,
  PRIMARY KEY (id_personne, id_specialite),
  FOREIGN KEY (id_personne)  REFERENCES personnes(id)  ON DELETE CASCADE,
  FOREIGN KEY (id_specialite) REFERENCES specialites(id) ON DELETE CASCADE
);

CREATE INDEX idx_ps_personne  ON personnes_specialites(id_personne);
CREATE INDEX idx_ps_specialite ON personnes_specialites(id_specialite);

