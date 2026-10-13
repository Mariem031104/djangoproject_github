from django.contrib import admin

from .models import Expedition


class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids_kg', 'statut', 'entreprise')
    list_filter = ('statut',)
    readonly_fields = ('reference',)


admin.site.register(Expedition, ExpeditionAdmin)