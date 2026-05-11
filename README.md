# Gestion-Trafic-A-rien-Django
SAE2.03

# Guide de Configuration Django : Du Projet Vierge à la Première Page

Ce document détaille les étapes pour installer Django, configurer un environnement de travail propre et ajouter une nouvelle page à votre application.

## 1. Prérequis et Environnement Virtuel

Il est essentiel d'utiliser un environnement virtuel (`venv`) pour isoler les dépendances de votre projet.

1. **Créer l'environnement virtuel :**
   ```bash
   python -m venv venv
   ```
2. **Activer l'environnement :**
   * **Windows :** `./venv/Scripts/activate`
   * **Mac/Linux :** `source venv/bin/activate`

## 2. Installation de Django

Une fois l'environnement activé, installez Django via `pip` :
```bash
pip install django
```

## 3. Création du Projet et de l'Application

1. **Créer le projet (ex: `firstproject`) :**
   ```bash
   django-admin startproject firstproject .
   ```
2. **Créer l'application (ex: `myfirstapp`) :**
   ```bash
   python manage.py startapp myfirstapp
   ```
3. **Déclarer l'application :**
   Ajoutez `'myfirstapp.apps.MyfirstappConfig'` à la liste `INSTALLED_APPS` dans `firstproject/settings.py`.

## 4. Configuration des URLs Globales

Dans le fichier `firstproject/urls.py`, incluez les URLs de votre application pour qu'elles soient reconnues par le projet :

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('myfirstapp/', include('myfirstapp.urls')), # Redirige vers les URLs de l'app
]
```

## 5. Ajouter une Nouvelle Page (ex: "formulaire")

Pour ajouter une page, suivez toujours ces trois étapes :

### Étape A : Créer la Vue
Dans `myfirstapp/views.py`, définissez la fonction qui traitera la requête :
```python
from django.shortcuts import render

def formulaire(request):
    return render(request, 'myfirstapp/formulaire.html')
```

### Étape B : Configurer l'URL de l'Application
Créez ou modifiez `myfirstapp/urls.py`. **Important :** Donnez toujours un `name` à vos routes pour éviter les erreurs `NoReverseMatch` :
```python
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('formulaire/', views.formulaire, name='formulaire'), # Le nom 'formulaire' est utilisé pour les liens
]
```

### Étape C : Créer le Template
Créez le fichier HTML dans le dossier suivant : `myfirstapp/templates/myfirstapp/formulaire.html`.
```html
<!DOCTYPE html>
<html>
<body>
    <h1>Nouvelle Page</h1>
    <form action="" method="post">
        {% csrf_token %} <input type="text" name="nom">
        <button type="submit">Envoyer</button>
    </form>
    <a href="{% url 'index' %}">Retour à l'accueil</a>
</body>
</html>
```

## 6. Lancement du Serveur

Pour tester votre configuration :
```bash
python manage.py runserver
```
Accédez ensuite à votre nouvelle page via : `http://127.0.0.1:8000/myfirstapp/formulaire/`
