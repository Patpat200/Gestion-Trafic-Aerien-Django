# Documentation - Système de Gestion de Trafic Aérien

Bienvenue sur la documentation technique officielle du projet de SAÉ (Situation d'Apprentissage et d'Évaluation) réalisé dans le cadre de la première année du BUT Réseaux et Télécommunications à l'IUT de Colmar.

Ce site centralise l'ensemble des guides de déploiement, l'analyse de l'architecture réseau/système ainsi que les commandes essentielles pour administrer et exploiter l'application.

## Présentation du Projet

L'objectif de cette SAÉ est de concevoir et déployer une application web complète permettant de simuler et de gérer un trafic aérien. L'interface permet de piloter différentes entités métiers : aéroports, pistes, compagnies aériennes, avions et vols, tout en respectant des contraintes strictes d'intégrité de données et de sécurité opérationnelle (validation des longueurs de pistes, espacement temporel anticollision).

### Architecture Technique

Le projet s'appuie sur une infrastructure hybride répartie sur des machines virtuelles Debian :

* **Application :** Développée en Python avec le framework web Django (Architecture MVT).
* **Base de Données :** Serveur relationnel MariaDB / MySQL géré de manière indépendante de l'ORM (tables créées manuellement en SQL pur).
* **Serveur de Production :** Serveur d'application Gunicorn couplé à un serveur web Nginx faisant office de Proxy Inverse.

## Sommaire de la Documentation

Pour naviguer dans la documentation, utilisez le menu latéral ou suivez directement les sections ci-dessous :

* [Guide de Déploiement](DEPLOIMENT.md) : Instructions pas-à-pas pour installer et configurer l'infrastructure de production (Debian, MariaDB, Gunicorn, Nginx).
* [Lancement Local](LOCAL.md) : Procédure pour exécuter et tester l'application en environnement de développement sous Windows ou Linux.
* [Mémento Commandes](MEMENTO.md) : Liste des commandes système, réseau et base de données utiles pour la maintenance et la supervision du serveur.

---

**Équipe projet :** Adil, Lucas, Adel  
**Établissement :** IUT de Colmar – Université de Haute-Alsace (UHA)  
**Formation :** BUT Réseaux et Télécommunications – 1ère année