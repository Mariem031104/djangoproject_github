from django.contrib import admin

from .models import Expedition


class ExpeditionAdmin(admin.ModelAdmin):
    list_display = ('reference', 'ville_depart', 'ville_arrivee', 'poids_kg',
                    'statut', 'date_souhaitee', 'entreprise')
    list_filter = ('statut',)
    readonly_fields = ('reference', 'created_at', 'updated_at')
    ordering = ('-date_souhaitee',)
    list_per_page = 5
    search_fields = ('reference', 'ville_depart', 'ville_arrivee', 'statut')
    list_editable = ('statut', 'date_souhaitee')

    fieldsets = (
        ('Informations', {
            'fields': ('reference', 'entreprise', 'ville_depart', 'ville_arrivee',
                       'date_souhaitee', 'poids_kg', 'statut',
                       'created_at', 'updated_at'),
        }),
    )


admin.site.register(Expedition, ExpeditionAdmin)