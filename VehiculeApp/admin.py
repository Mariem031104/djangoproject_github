# VehiculeApp/admin.py
from django.contrib import admin
from .models import Vehicule


@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('immatriculation', 'type_vehicule', 'capacite_kg', 'disponible', 'entreprise')
    list_filter = ('type_vehicule', 'disponible')
    search_fields = ('immatriculation',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10

    fieldsets = (
        ('Identification', {'fields': ('immatriculation', 'type_vehicule', 'entreprise')}),
        ('Capacité et disponibilité', {'fields': ('capacite_kg', 'disponible')}),
        ('Informations système', {'fields': ('created_at', 'updated_at')}),
    )