import csv, io
from django.shortcuts import render, redirect, get_object_or_404
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol
from .forms import AeroportForm, PisteForm, CompagnieForm, TypeAvionForm, AvionForm, VolForm
from datetime import timedelta
from django.contrib import messages

def index(request):
    return render(request, 'TraficAerien/index.html')





# ───── AÉROPORTS ─────
def aeroport_liste(request):
    aeroports = Aeroport.objects.all()
    return render(request, 'TraficAerien/aeroport_liste.html', {'aeroports': aeroports})

def aeroport_creer(request):
    if request.method == 'POST':
        form = AeroportForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('aeroport_liste')
    else:
        form = AeroportForm()
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Ajouter un aéroport'
    })

def aeroport_modifier(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    if request.method == 'POST':
        form = AeroportForm(request.POST, instance=aeroport)
        if form.is_valid():
            form.save()
            return redirect('aeroport_liste')
    else:
        form = AeroportForm(instance=aeroport)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier un aéroport'
    })

def aeroport_supprimer(request, pk):
    aeroport = get_object_or_404(Aeroport, pk=pk)
    if request.method == 'POST':
        aeroport.delete()
        return redirect('aeroport_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': aeroport, 'titre': 'Supprimer un aéroport'
    })






# ───── PISTES ─────
def piste_liste(request):
    pistes = Piste.objects.all()
    return render(request, 'TraficAerien/piste_liste.html', {'pistes': pistes})

def piste_creer(request):
    if request.method == 'POST':
        form = PisteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('piste_liste')
    else:
        form = PisteForm()
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Ajouter une piste'
    })

def piste_modifier(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    if request.method == 'POST':
        form = PisteForm(request.POST, instance=piste)
        if form.is_valid():
            form.save()
            return redirect('piste_liste')
    else:
        form = PisteForm(instance=piste)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier une piste'
    })

def piste_supprimer(request, pk):
    piste = get_object_or_404(Piste, pk=pk)
    if request.method == 'POST':
        piste.delete()
        return redirect('piste_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': piste, 'titre': 'Supprimer une piste'
    })





# ───── AVIONS ─────
def avion_liste(request):
    avions = Avion.objects.all()
    return render(request, 'TraficAerien/avion_liste.html', {'avions': avions})

def avion_creer(request):
    if request.method == 'POST':
        form = AvionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('avion_liste')
    else:
        form = AvionForm()
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Ajouter un avion'
    })

def avion_modifier(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        form = AvionForm(request.POST, instance=avion)
        if form.is_valid():
            form.save()
            return redirect('avion_liste')
    else:
        form = AvionForm(instance=avion)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier un avion'
    })

def avion_supprimer(request, pk):
    avion = get_object_or_404(Avion, pk=pk)
    if request.method == 'POST':
        avion.delete()
        return redirect('avion_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': avion, 'titre': 'Supprimer un avion'
    })




# ───── VOLS ─────
def vol_liste(request):
    vols = Vol.objects.all()
    return render(request, 'TraficAerien/vol_liste.html', {'vols': vols})


def vol_creer(request):
    suggestion = None
    if request.method == 'POST':
        form = VolForm(request.POST)
        if form.is_valid():
            vol = form.save(commit=False)
            type_avion = vol.avion.modele
            aeroport_arr = vol.aeroport_arrivee
            heure_arr = vol.date_heure_arrivee

            # BOUCLE 1 : On cherche les pistes assez longues (façon algorithmique classique)
            toutes_les_pistes = Piste.objects.filter(aeroport=aeroport_arr)
            pistes_compatibles = []
            
            for piste in toutes_les_pistes:
                if piste.longueur >= type_avion.longueur_piste_necessaire:
                    pistes_compatibles.append(piste)

            if len(pistes_compatibles) == 0:
                messages.error(request, f"Aucune piste assez longue à l'aéroport {aeroport_arr}.")
                return render(request, 'TraficAerien/vol_form.html', {'form': form, 'titre': 'Ajouter un vol'})

            # On récupère tous les vols existants sur cet aéroport pour faire nos comparaisons
            vols_existants = Vol.objects.filter(aeroport_arrivee=aeroport_arr)
            piste_libre = None
            
            # BOUCLE 2 : On vérifie si les pistes compatibles sont libres
            for piste in pistes_compatibles:
                occupee = False
                for ancien_vol in vols_existants:
                    if ancien_vol.piste_arrivee == piste:
                        # On calcule l'écart de temps en secondes
                        ecart = (ancien_vol.date_heure_arrivee - heure_arr).total_seconds()
                        if ecart < 600 and ecart > -600:  # 600 secondes = 10 minutes
                            occupee = True
                            break  # On sort de la boucle, cette piste est prise
                
                if occupee == False:
                    piste_libre = piste
                    break  # Super, on a trouvé une piste, on arrête de chercher !

            # BOUCLE 3 : Si tout est occupé, on avance de 10 min en 10 min
            if piste_libre is None:
                heure_test = heure_arr
                for i in range(48):  # On teste pendant 8 heures maximum (48 * 10min)
                    heure_test = heure_test + timedelta(minutes=10)
                    
                    # On refait le même test avec le nouvel horaire
                    for piste in pistes_compatibles:
                        occupee = False
                        for ancien_vol in vols_existants:
                            if ancien_vol.piste_arrivee == piste:
                                ecart = (ancien_vol.date_heure_arrivee - heure_test).total_seconds()
                                if ecart < 600 and ecart > -600: 
                                    occupee = True
                                    break
                        if occupee == False:
                            piste_libre = piste
                            break
                    
                    if piste_libre is not None:
                        break  # On a enfin trouvé un créneau
                
                suggestion = heure_test
                messages.warning(request, f"Attention, piste occupée ! Nouveau créneau proposé : {suggestion}")
                return render(request, 'TraficAerien/vol_form.html', {
                    'form': form, 'titre': 'Ajouter un vol', 'suggestion': suggestion
                })

            # Si on arrive ici, tout est bon, on sauvegarde en base
            vol.piste_arrivee = piste_libre
            vol.save()
            messages.success(request, f"Vol créé avec succès sur la piste {piste_libre.numero}.")
            return redirect('vol_liste')
    else:
        form = VolForm()
    return render(request, 'TraficAerien/vol_form.html', {
        'form': form, 'titre': 'Ajouter un vol'
    })


def vol_modifier(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    if request.method == 'POST':
        form = VolForm(request.POST, instance=vol)
        if form.is_valid():
            form.save()
            return redirect('vol_liste')
    else:
        form = VolForm(instance=vol)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier un vol'
    })

def vol_supprimer(request, pk):
    vol = get_object_or_404(Vol, pk=pk)
    if request.method == 'POST':
        vol.delete()
        return redirect('vol_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': vol, 'titre': 'Supprimer un vol'
    })

def fiche_vols(request):
    aeroports = Aeroport.objects.all()
    
    # On prépare des variables vides par défaut (quand on arrive sur la page)
    vols_trouves = None
    aeroport_sel = None
    date_sel = ""
    sens_sel = ""
    
    # Si on détecte qu'une recherche a été lancée (présence de 'aeroport_id' dans l'URL)
    if 'aeroport_id' in request.GET:
        # On récupère EXACTEMENT les "name" de ton formulaire HTML
        aero_id = request.GET.get('aeroport_id')
        date_sel = request.GET.get('date')
        sens_sel = request.GET.get('sens')
        
        # On s'assure que l'utilisateur a bien rempli l'aéroport et la date
        if aero_id and date_sel:
            # On récupère l'objet Aéroport pour l'afficher dans le titre du HTML
            aeroport_sel = Aeroport.objects.get(pk=aero_id)
            
            # On filtre selon le choix du menu déroulant "Sens"
            if sens_sel == 'depart':
                vols_trouves = Vol.objects.filter(
                    aeroport_depart=aeroport_sel, 
                    date_heure_depart__date=date_sel
                )
            elif sens_sel == 'arrivee':
                vols_trouves = Vol.objects.filter(
                    aeroport_arrivee=aeroport_sel, 
                    date_heure_arrivee__date=date_sel
                )

    # On envoie toutes les informations au template pour qu'il puisse tout afficher
    return render(request, 'TraficAerien/fiche_vols.html', {
        'aeroports': aeroports, 
        'vols': vols_trouves,
        'aeroport_sel': aeroport_sel,
        'date_sel': date_sel,
        'sens': sens_sel
    })





def import_vols_csv(request):
    ok = 0
    erreurs = []
    termine = False

    if request.method == 'POST':
        fichier = request.FILES.get('fichier_csv')
        
        if not fichier:
            messages.error(request, "Pas de fichier reçu")
            return redirect('import_vols_csv')

        donnees = fichier.read().decode('utf-8')
        lecteur = csv.reader(io.StringIO(donnees))
        next(lecteur) # on saute la ligne des titres

        for ligne in lecteur:
            try:
                avion = Avion.objects.get(nom=ligne[0])
                aero_dep = Aeroport.objects.get(nom=ligne[2])
                aero_arr = Aeroport.objects.get(nom=ligne[4])

                Vol.objects.create(
                    avion=avion,
                    pilote=ligne[1],
                    aeroport_depart=aero_dep,
                    date_heure_depart=ligne[3],
                    aeroport_arrivee=aero_arr,
                    date_heure_arrivee=ligne[5]
                )
                ok += 1

            except Exception as e:
                erreurs.append(f"Ligne {ok + len(erreurs) + 2} : {e}")

        termine = True

    return render(request, 'TraficAerien/import_vols.html', {
        'termine': termine,
        'ok': ok,
        'erreurs': erreurs
    })









# ───── COMPAGNIES ─────
def compagnie_liste(request):
    compagnies = Compagnie.objects.all()
    return render(request, 'TraficAerien/compagnie_liste.html', {'compagnies': compagnies})

def compagnie_creer(request):
    if request.method == 'POST':
        form = CompagnieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('compagnie_liste')
    else:
        form = CompagnieForm()
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Ajouter une compagnie'
    })

def compagnie_modifier(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    if request.method == 'POST':
        form = CompagnieForm(request.POST, instance=compagnie)
        if form.is_valid():
            form.save()
            return redirect('compagnie_liste')
    else:
        form = CompagnieForm(instance=compagnie)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier une compagnie'
    })

def compagnie_supprimer(request, pk):
    compagnie = get_object_or_404(Compagnie, pk=pk)
    if request.method == 'POST':
        compagnie.delete()
        return redirect('compagnie_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': compagnie, 'titre': 'Supprimer une compagnie'
    })





# ───── TYPES D'AVIONS ─────
def typeavion_liste(request):
    types = TypeAvion.objects.all()
    return render(request, 'TraficAerien/typeavion_liste.html', {'types': types})

def typeavion_creer(request):
    if request.method == 'POST':
        form = TypeAvionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('typeavion_liste')
    else:
        form = TypeAvionForm()
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Ajouter un type d\'avion'
    })

def typeavion_modifier(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    if request.method == 'POST':
        form = TypeAvionForm(request.POST, request.FILES, instance=type_avion)
        if form.is_valid():
            form.save()
            return redirect('typeavion_liste')
    else:
        form = TypeAvionForm(instance=type_avion)
    return render(request, 'TraficAerien/formulaire.html', {
        'form': form, 'titre': 'Modifier un type d\'avion'
    })

def typeavion_supprimer(request, pk):
    type_avion = get_object_or_404(TypeAvion, pk=pk)
    if request.method == 'POST':
        type_avion.delete()
        return redirect('typeavion_liste')
    return render(request, 'TraficAerien/confirmer_suppression.html', {
        'objet': type_avion, 'titre': 'Supprimer un type d\'avion'
    })
