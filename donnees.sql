USE trafic_aerien;

INSERT INTO aeroport (nom, pays) VALUES
('Charles de Gaulle', 'France'),
('Orly', 'France'),
('Lyon Saint-Exupery', 'France'),
('Nice Cote d Azur', 'France'),
('Marseille Provence', 'France');

INSERT INTO compagnie (nom, description, pays_rattachement) VALUES
('Air France', 'Compagnie nationale francaise', 'France'),
('EasyJet', 'Compagnie low-cost europeenne', 'Royaume-Uni'),
('Ryanair', 'Compagnie low-cost irlandaise', 'Irlande'),
('Transavia', 'Filiale low-cost Air France', 'France');

INSERT INTO typeavion (marque, modele, description, longueur_piste_necessaire) VALUES
('Airbus', 'A320', 'Court moyen courrier', 1800),
('Boeing', 'B737', 'Court moyen courrier', 2200),
('Airbus', 'A321', 'Moyen courrier', 2000),
('Boeing', 'B777', 'Long courrier', 3000),
('Airbus', 'A380', 'Tres gros porteur', 3200),
('ATR', '72-600', 'Turbopropulseur regional', 1500);

INSERT INTO piste (numero, longueur, aeroport_id) VALUES
('27L', 4215, 1), ('09R', 2700, 1),
('25', 3320, 2), ('07', 2400, 2),
('35L', 4000, 3), ('17', 2800, 3),
('04R', 3000, 4), ('22', 2100, 4),
('31R', 3500, 5), ('13', 2600, 5);

INSERT INTO avion (nom, compagnie_id, modele_id) VALUES
('F-GKXA', 1, 1), ('F-GKXB', 1, 1), ('F-WXYZ', 1, 4),
('F-HBNA', 1, 3), ('G-EZAA', 2, 1), ('G-EZAB', 2, 1),
('G-EZAC', 2, 2), ('EI-DCL', 3, 2), ('EI-DCM', 3, 2),
('EI-ENL', 3, 1), ('F-GZHG', 4, 1), ('F-GZHH', 4, 1),
('F-HBXA', 1, 5), ('F-ATRC', 1, 6), ('G-EZAD', 2, 3);