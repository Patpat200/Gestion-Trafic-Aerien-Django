from django import forms
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol

class AeroportForm(forms.ModelForm):
    class Meta:
        model = Aeroport
        fields = ['nom', 'pays']

class PisteForm(forms.ModelForm):
    class Meta:
        model = Piste
        fields = ['numero', 'aeroport', 'longueur']

class CompagnieForm(forms.ModelForm):
    class Meta:
        model = Compagnie
        fields = ['nom', 'description', 'pays_rattachement']

class TypeAvionForm(forms.ModelForm):
    class Meta:
        model = TypeAvion
        fields = ['marque', 'modele', 'description', 'image', 'longueur_piste_necessaire']

class AvionForm(forms.ModelForm):
    class Meta:
        model = Avion
        fields = ['nom', 'compagnie', 'modele']

class VolForm(forms.ModelForm):
    class Meta:
        model = Vol
        fields = [
            'avion', 'pilote',
            'aeroport_depart', 'date_heure_depart',
            'aeroport_arrivee', 'date_heure_arrivee'
        ]
        widgets = {
            'date_heure_depart': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'date_heure_arrivee': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }