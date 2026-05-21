from django.contrib import admin
from .models import Aeroport, Piste, Compagnie, TypeAvion, Avion, Vol

admin.site.register(Aeroport)
admin.site.register(Piste)
admin.site.register(Compagnie)
admin.site.register(TypeAvion)
admin.site.register(Avion)
admin.site.register(Vol)