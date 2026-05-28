from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Aéroports
    path('aeroports/', views.aeroport_liste, name='aeroport_liste'),
    path('aeroports/ajouter/', views.aeroport_creer, name='aeroport_creer'),
    path('aeroports/modifier/<int:pk>/', views.aeroport_modifier, name='aeroport_modifier'),
    path('aeroports/supprimer/<int:pk>/', views.aeroport_supprimer, name='aeroport_supprimer'),

    # Pistes
    path('pistes/', views.piste_liste, name='piste_liste'),
    path('pistes/ajouter/', views.piste_creer, name='piste_creer'),
    path('pistes/modifier/<int:pk>/', views.piste_modifier, name='piste_modifier'),
    path('pistes/supprimer/<int:pk>/', views.piste_supprimer, name='piste_supprimer'),

    # Avions
    path('avions/', views.avion_liste, name='avion_liste'),
    path('avions/ajouter/', views.avion_creer, name='avion_creer'),
    path('avions/modifier/<int:pk>/', views.avion_modifier, name='avion_modifier'),
    path('avions/supprimer/<int:pk>/', views.avion_supprimer, name='avion_supprimer'),

    # Vols
    path('vols/', views.vol_liste, name='vol_liste'),
    path('vols/ajouter/', views.vol_creer, name='vol_creer'),
    path('vols/modifier/<int:pk>/', views.vol_modifier, name='vol_modifier'),
    path('vols/supprimer/<int:pk>/', views.vol_supprimer, name='vol_supprimer'),
    path('vols/import/', views.import_vols_csv, name='import_vols_csv'),
    path('vols/fiches/', views.fiche_vols, name='fiche_vols'),


    # Compagnies
    path('compagnies/', views.compagnie_liste, name='compagnie_liste'),
    path('compagnies/ajouter/', views.compagnie_creer, name='compagnie_creer'),
    path('compagnies/modifier/<int:pk>/', views.compagnie_modifier, name='compagnie_modifier'),
    path('compagnies/supprimer/<int:pk>/', views.compagnie_supprimer, name='compagnie_supprimer'),

    # Types d'avions
    path('typesavions/', views.typeavion_liste, name='typeavion_liste'),
    path('typesavions/ajouter/', views.typeavion_creer, name='typeavion_creer'),
    path('typesavions/modifier/<int:pk>/', views.typeavion_modifier, name='typeavion_modifier'),
    path('typesavions/supprimer/<int:pk>/', views.typeavion_supprimer, name='typeavion_supprimer'),


]