# Procédure de déploiement — SAE203 Gestion Trafic Aérien
# VM Debian/Ubuntu — Nginx + Gunicorn + MariaDB

## Prérequis déjà en place
- VM Debian avec MariaDB opérationnelle (base `trafic_aerien` existante)
- Code disponible sur GitHub

---

## 1. Créer un utilisateur dédié (bonne pratique)

```bash
sudo adduser django
sudo usermod -aG sudo django
su - django
```

---

## 2. Installer les paquets système

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git
```

---

## 3. Cloner le projet

```bash
cd /home/django
git clone https://github.com/Patpat200/Gestion-Trafic-Aerien-Django
cd Gestion-Trafic-Aerien-Django
```

---

## 4. Environnement virtuel + dépendances

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 5. Collecter les fichiers statiques

Django doit copier tous les fichiers CSS/JS dans `staticfiles/` pour que Nginx puisse les servir directement.

```bash
python manage.py collectstatic --noinput
```

---

## 6. Tester Gunicorn seul (optionnel, vérification)

```bash
gunicorn --bind 0.0.0.0:8000 SAE203.wsgi:application
# Ctrl+C pour arrêter
```

---

## 7. Configurer le service systemd (Gunicorn)

Copier le fichier `doc/gunicorn_trafic.service` vers systemd :

```bash
sudo cp doc/gunicorn_trafic.service /etc/systemd/system/gunicorn_trafic.service
sudo systemctl daemon-reload
sudo systemctl enable gunicorn_trafic
sudo systemctl start gunicorn_trafic
# Vérifier que ça tourne :
sudo systemctl status gunicorn_trafic
```

---

## 8. Configurer Nginx

```bash
sudo cp doc/nginx_trafic_aerien.conf /etc/nginx/sites-available/trafic_aerien
sudo ln -s /etc/nginx/sites-available/trafic_aerien /etc/nginx/sites-enabled/
# Supprimer le site par défaut si présent :
sudo rm -f /etc/nginx/sites-enabled/default
# Tester la config Nginx :
sudo nginx -t
# Activer :
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 9. Vérification finale

Ouvrir un navigateur sur n'importe quelle machine du même réseau :

```
http://192.168.1.80/
```

Le site doit s'afficher avec le tableau de bord.

---

## Commandes utiles (maintenance)

| Action | Commande |
|---|---|
| Voir les logs Gunicorn | `sudo journalctl -u gunicorn_trafic -f` |
| Redémarrer Gunicorn | `sudo systemctl restart gunicorn_trafic` |
| Voir les logs Nginx | `sudo tail -f /var/log/nginx/error.log` |
| Redémarrer Nginx | `sudo systemctl restart nginx` |
| Mettre à jour le code | `git pull && sudo systemctl restart gunicorn_trafic` |

---

## Notes

- Le chemin `/home/django/Gestion-Trafic-Aerien-Django/` doit correspondre à votre répertoire réel.
- Si l'IP de la VM change, mettre à jour `ALLOWED_HOSTS` dans `SAE203/settings.py` ET `server_name` dans `nginx_trafic_aerien.conf`.
- Pour la soutenance, `DEBUG = False` est recommandé en prod mais `DEBUG = True` reste acceptable pour un projet étudiant.