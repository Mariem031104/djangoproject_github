```python
from django.db import models
from django.core.exceptions import ValidationError

from EntrepriseApp.models import Entreprise


class Expedition(models.Model):

    reference = models.CharField(
        max_length=10,
        unique=True
    )

    date_souhaitee = models.DateField()

    ville_depart = models.CharField(
        max_length=10
    )

    ville_arrivee = models.CharField(
        max_length=10
    )

    poids_kg = models.IntegerField()

    description = models.TextField(
        blank=True,
        null=True
    )

    statut = models.CharField(
        max_length=30,
        choices=[
            ('publiee', 'Publiée'),
            ('en_cours', 'En cours'),
            ('attribuee', 'Attribuée'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée — Défaut Publiée'),
        ],
        default='publiee'
    )

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def clean(self):
        super().clean()

        # Règle métier :
        # une expédition ne peut être créée
        # que par une entreprise de type "chargeur"

        if (
            self.entreprise_id
            and self.entreprise.type_entreprise != 'chargeur'
        ):
            raise ValidationError({
                'entreprise': (
                    "Une expédition ne peut être créée "
                    "que par une entreprise de type chargeur."
                )
            })

    def __str__(self):
        return self.reference


