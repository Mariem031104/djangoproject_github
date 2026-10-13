from django.contrib import admin

from .models import Offre


class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = ('statut',)
    search_fields = ('transporteur__username', 'transporteur__email', 'vehicule__immatriculation')
    list_editable = ('prix', 'delai_jours', 'statut')


admin.site.register(Offre, OffreAdmin)