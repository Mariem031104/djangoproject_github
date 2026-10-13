from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur, Entreprise


class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ('type_entreprise',)


admin.site.register(Utilisateur, UserAdmin)
admin.site.register(Entreprise, EntrepriseAdmin)