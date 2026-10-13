from django.contrib import admin

from .models import Vehicule


class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
    list_filter = ('type_vehicule', 'disponible')


admin.site.register(Vehicule, VehiculeAdmin)