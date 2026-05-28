from django.db import models

class Aeroport(models.Model):
    nom = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom} ({self.pays})"

class Piste(models.Model):
    numero = models.CharField(max_length=10)
    aeroport = models.ForeignKey(Aeroport, on_delete=models.CASCADE, related_name='pistes')
    longueur = models.IntegerField(help_text="Longueur en mètres")

    def __str__(self):
        return f"Piste {self.numero} — {self.aeroport.nom}"

class Compagnie(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    pays_rattachement = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class TypeAvion(models.Model):
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='avions/', blank=True, null=True)
    longueur_piste_necessaire = models.IntegerField(help_text="En mètres")

    def __str__(self):
        return f"{self.marque} {self.modele}"

class Avion(models.Model):
    nom = models.CharField(max_length=100)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE)
    modele = models.ForeignKey(TypeAvion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nom} ({self.compagnie})"

class Vol(models.Model):
    avion = models.ForeignKey(Avion, on_delete=models.CASCADE)
    pilote = models.CharField(max_length=100)
    aeroport_depart = models.ForeignKey(Aeroport, on_delete=models.CASCADE, related_name='vols_depart')
    date_heure_depart = models.DateTimeField()
    aeroport_arrivee = models.ForeignKey(Aeroport, on_delete=models.CASCADE, related_name='vols_arrivee')
    date_heure_arrivee = models.DateTimeField()
    piste_arrivee = models.ForeignKey('Piste', on_delete=models.SET_NULL, null=True, blank=True, related_name='vols')


    def __str__(self):
        return f"Vol {self.id} — {self.aeroport_depart} -> {self.aeroport_arrivee}"

