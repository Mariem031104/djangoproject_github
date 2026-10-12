from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicule(models.Model):

    immatriculation = models.CharField(
        max_length=11,
        unique=True
    )

    capacite_kg = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                "La capacité doit être supérieure à 0 kg."
            )
        ]
    )

    disponibilite = models.BooleanField(
        default=True
    )

    type_vehicule = models.CharField(
        max_length=20,
        choices=[
            ('camionette', 'Camionnette'),
            ('remorque', 'Remorque'),
            ('forgon', 'Fourgon'),
            ('porteur', 'Porteur'),
        ],
        default='camionette'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    proprietaire = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )

    def clean(self):
        if (
            self.proprietaire
            and self.proprietaire.type_entreprise != 'transporteur'
        ):
            raise ValidationError(
                "Le propriétaire du véhicule doit être une entreprise de type transporteur."
            )

    def __str__(self):
        return self.immatriculation