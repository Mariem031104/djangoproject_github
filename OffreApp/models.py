from django.db import models

from ExpeditionApp.models import Expedition
from EntreprisesApp.models import Entreprise
from VehiculesApp.models import Vehicule


class Offre(models.Model):

    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]

    prix = models.DecimalField(max_digits=10, decimal_places=2)

    delai_jours = models.PositiveIntegerField()

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee'
    )

    date_proposition = models.DateField(auto_now_add=True)

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE
    )

    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE
    )

    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE
    )