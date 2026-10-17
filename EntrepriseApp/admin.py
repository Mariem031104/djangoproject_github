from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Utilisateur, Entreprise


@admin.register(Utilisateur)
class UtilisateurAdmin(UserAdmin):
    list_display = ('user_id', 'username', 'email', 'role', 'telephone', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('user_id', 'username', 'email', 'telephone')
    ordering = ('user_id',)
    readonly_fields = ('user_id', 'created_at', 'updated_at', 'last_login', 'date_joined')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations TransConnect', {
            'fields': ('user_id', 'role', 'telephone', 'created_at', 'updated_at'),
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations TransConnect', {
            'fields': ('email', 'role', 'telephone'),
        }),
    )


@admin.register(Entreprise)
class EntrepriseAdmin(admin.ModelAdmin):
    list_display = ('raison_sociale', 'matricule_fiscal', 'type_entreprise', 'gerant', 'created_at')
    list_filter = ('type_entreprise',)
    search_fields = ('raison_sociale', 'matricule_fiscal')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 10

    fieldsets = (
        ('Identification', {
            'fields': ('raison_sociale', 'matricule_fiscal', 'type_entreprise'),
        }),
        ('Coordonnées', {
            'fields': ('adresse', 'gerant'),
        }),
        ('Informations système', {
            'fields': ('created_at', 'updated_at'),
        }),
    )