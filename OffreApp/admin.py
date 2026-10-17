from django.contrib import admin

from .models import Offre


@admin.register(Offre)
class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = ('statut',)
    search_fields = (
        'expedition__reference',
        'transporteur__raison_sociale',
        'vehicule__immatriculation',
    )
    list_editable = ('prix', 'delai_jours', 'statut')
    list_per_page = 10

    fieldsets = (
        ('Relations', {
            'fields': ('expedition', 'transporteur', 'vehicule'),
        }),
        ('Proposition', {
            'fields': ('prix', 'delai_jours', 'statut'),
        }),
    )