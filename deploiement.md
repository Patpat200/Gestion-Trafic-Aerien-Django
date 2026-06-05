# Procédure de déploiement — SAE203 Gestion Trafic Aérien
# 2 VMs Debian Server en mode Pont (DHCP)

---

## Architecture

```
[ PC Hôte / Réseau de la salle ]
        |
        |-- [ VM Django ]  Debian Server — Nginx + Gunicorn + Django
        |-- [ VM BDD ]     Debian Server — MariaDB
```

Les deux VMs sont en **mode pont** sur le réseau de la salle.  
Les IPs sont attribuées par DHCP — pour connaître l'IP d'une VM :
```bash
ip a
```

---

## VM BDD — Installation MariaDB

### 1. Installer MariaDB

```bash
sudo apt update
sudo apt install -y mariadb-server
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

### 2. Créer la base et l'utilisateur

```bash
sudo mariadb
```

```sql
CREATE DATABASE trafic_aerien CHARACTER SET utf8mb4;
CREATE USER 'django_user'@'%' IDENTIFIED BY 'toto';
GRANT ALL PRIVILEGES ON trafic_aerien.* TO 'django_user'@'%';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Autoriser les connexions distantes

Éditer `/etc/mysql/mariadb.conf.d/50-server.cnf` :

```bash
sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
```

Trouver la ligne `bind-address` et mettre :
```
bind-address = 0.0.0.0
```

Redémarrer MariaDB :
```bash
sudo systemctl restart mariadb
```

### 4. Charger le schéma et les données

Depuis la VM BDD (après avoir cloné le repo ou copié les fichiers) :
```bash
sudo mariadb trafic_aerien < db/schema.sql
sudo mariadb trafic_aerien < db/donnees.sql
```

---

## VM Django — Installation Nginx + Gunicorn + Django

### 1. Installer les paquets système

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx git
```

### 2. Cloner le projet

```bash
cd ~
git clone https://github.com/Patpat200/Gestion-Trafic-Aerien-Django
cd Gestion-Trafic-Aerien-Django
```

### 3. Environnement virtuel et dépendances

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configurer settings.py

```bash
nano SAE203/settings.py
```

Modifier les lignes suivantes :

```python
# Mettre l'IP de la VM Django (résultat de "ip a")
ALLOWED_HOSTS = ['<IP_VM_DJANGO>', 'localhost', '127.0.0.1']

# Mettre l'IP de la VM BDD (résultat de "ip a" sur la VM BDD)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'trafic_aerien',
        'USER': 'django_user',
        'PASSWORD': 'toto',
        'HOST': '<IP_VM_BDD>',
        'PORT': '3306',
    }
}
```

### 5. Collecter les fichiers statiques

```bash
python3 manage.py collectstatic --noinput
```

### 6. Appliquer les migrations Django (tables internes uniquement)

```bash
python3 manage.py migrate
```

### 7. Configurer Nginx

```bash
sudo nano /etc/nginx/sites-available/trafic_aerien
```

Coller la configuration suivante (remplacer `<IP_VM_DJANGO>` par la vraie IP) :

```nginx
server {
    listen 80;
    server_name <IP_VM_DJANGO> localhost;

    location /static/ {
        alias /home/<USER>/Gestion-Trafic-Aerien-Django/staticfiles/;
    }

    location /media/ {
        alias /home/<USER>/Gestion-Trafic-Aerien-Django/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Activer le site et redémarrer Nginx :

```bash
sudo ln -s /etc/nginx/sites-available/trafic_aerien /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
sudo systemctl enable nginx
```

### 8. Lancer Gunicorn

Toujours avec le venv activé :

```bash
source venv/bin/activate
pkill -f gunicorn 2>/dev/null
python3 -m gunicorn --bind 127.0.0.1:8000 SAE203.wsgi:application --daemon
```

### 9. Vérification

Depuis n'importe quel PC du réseau, ouvrir un navigateur sur :
```
http://<IP_VM_DJANGO>/
```

---

## Mise à jour du code (après un git push)

```bash
cd ~/Gestion-Trafic-Aerien-Django
git stash
git pull origin main
git stash pop
# Résoudre les conflits dans settings.py si nécessaire (ALLOWED_HOSTS, HOST BDD)
source venv/bin/activate
python3 manage.py collectstatic --noinput
pkill -f gunicorn
python3 -m gunicorn --bind 127.0.0.1:8000 SAE203.wsgi:application --daemon
```

---

## Commandes utiles

| Action | Commande |
|---|---|
| Trouver l'IP de la VM | `ip a` |
| Voir les erreurs Gunicorn | Lancer sans `--daemon` |
| Voir les erreurs Nginx | `sudo tail -20 /var/log/nginx/error.log` |
| Redémarrer Nginx | `sudo systemctl restart nginx` |
| Tester Gunicorn seul | `curl http://127.0.0.1:8000` |
| Vérifier port 8000 | `sudo ss -tlnp \| grep 8000` |
| Tuer Gunicorn | `pkill -f gunicorn` |
| Libérer le port 8000 | `sudo fuser -k 8000/tcp` |

---

## Notes importantes

- `settings.py` **ne doit pas être commité** avec les vraies IPs — les modifier directement sur la VM après chaque `git pull`
- Les IPs changent à chaque redémarrage en DHCP — toujours vérifier avec `ip a` avant de démarrer
- Le venv doit toujours être activé (`source venv/bin/activate`) avant de lancer Gunicorn
- Si port 8000 déjà occupé : `sudo fuser -k 8000/tcp` puis relancer Gunicorn
