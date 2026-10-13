from django.contrib import admin

from .models import Offre


class OffreAdmin(admin.ModelAdmin):
    list_display = ('id', 'expedition', 'transporteur', 'vehicule', 'prix', 'delai_jours', 'statut')
    list_filter = ('statut',)


admin.site.register(Offre, OffreAdmin)