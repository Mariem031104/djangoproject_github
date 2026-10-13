from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


class Vehicule(models.Model):

    TYPE_CHOICES = [
        ('camionnette', 'Camionnette / utilitaire léger'),
        ('camion_porteur', 'Camion porteur'),
        ('semi_remorque', 'Semi-remorque'),
        ('fourgon', 'Fourgon'),
    ]

    immatriculation = models.CharField(
        max_length=11,
        unique=True
    )

    type_vehicule = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='camionnette'
    )

    # Une capacité nulle (ou négative) est refusée
    capacite_kg = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                "La capacité doit être supérieure à 0 kg."
            )
        ]
    )

    disponible = models.BooleanField(default=True)

    # Relation "possède" : Entreprise 1 --- * Vehicule
    entreprise = models.ForeignKey(
        'EntrepriseApp.Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # Règle métier : l'entreprise doit être un transporteur
        if (
            self.entreprise_id
            and self.entreprise.type_entreprise != 'transporteur'
        ):
            raise ValidationError({
                'entreprise': (
                    "Le propriétaire du véhicule doit être "
                    "une entreprise de type transporteur."
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.immatriculation