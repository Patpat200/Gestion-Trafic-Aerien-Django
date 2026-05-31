USE trafic_aerien;

CREATE TABLE aeroport (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    pays VARCHAR(100) NOT NULL
);

CREATE TABLE compagnie (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    description TEXT,
    pays_rattachement VARCHAR(100) NOT NULL
);

CREATE TABLE typeavion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    marque VARCHAR(100) NOT NULL,
    modele VARCHAR(100) NOT NULL,
    description TEXT,
    image VARCHAR(200),
    longueur_piste_necessaire INT NOT NULL
);

CREATE TABLE piste (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero VARCHAR(10) NOT NULL,
    longueur INT NOT NULL,
    aeroport_id INT NOT NULL,
    FOREIGN KEY (aeroport_id) REFERENCES aeroport(id) ON DELETE CASCADE
);

CREATE TABLE avion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    compagnie_id INT NOT NULL,
    modele_id INT NOT NULL,
    FOREIGN KEY (compagnie_id) REFERENCES compagnie(id) ON DELETE CASCADE,
    FOREIGN KEY (modele_id) REFERENCES typeavion(id) ON DELETE CASCADE
);

CREATE TABLE vol (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pilote VARCHAR(100) NOT NULL,
    date_heure_depart DATETIME NOT NULL,
    date_heure_arrivee DATETIME NOT NULL,
    avion_id INT NOT NULL,
    aeroport_depart_id INT NOT NULL,
    aeroport_arrivee_id INT NOT NULL,
    piste_arrivee_id INT,
    FOREIGN KEY (avion_id) REFERENCES avion(id) ON DELETE CASCADE,
    FOREIGN KEY (aeroport_depart_id) REFERENCES aeroport(id) ON DELETE CASCADE,
    FOREIGN KEY (aeroport_arrivee_id) REFERENCES aeroport(id) ON DELETE CASCADE,
    FOREIGN KEY (piste_arrivee_id) REFERENCES piste(id) ON DELETE SET NULL
);