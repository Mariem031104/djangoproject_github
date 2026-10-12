
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule


class Offre(models.Model):

    STATUT_CHOICES = [
        ('proposee', 'Proposée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('retiree', 'Retirée'),
    ]

    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                0.01,
                "Le prix doit être supérieur à 0."
            )
        ]
    )

    delai_jours = models.PositiveIntegerField(
        validators=[
            MinValueValidator(
                1,
                "Le délai doit être supérieur ou égal à 1 jour."
            )
        ]
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='proposee'
    )

    date_proposition = models.DateField(
        auto_now_add=True
    )

    expedition = models.ForeignKey(
        Expedition,
        on_delete=models.CASCADE,
        related_name='offres'
    )

    transporteur = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='offres'
    )

    vehicule = models.ForeignKey(
        Vehicule,
        on_delete=models.CASCADE,
        related_name='offres'
    )

    def clean(self):
        super().clean()

        # Règle 1 : le transporteur doit être de type transporteur
        if (
            self.transporteur_id
            and self.transporteur.type_entreprise != 'transporteur'
        ):
            raise ValidationError({
                'transporteur': (
                    "L'offre doit être associée à une entreprise "
                    "de type transporteur."
                )
            })

        # Règle 2 : le véhicule doit appartenir au transporteur
        if (
            self.vehicule_id
            and self.transporteur_id
            and self.vehicule.entreprise_id != self.transporteur_id
        ):
            raise ValidationError({
                'vehicule': (
                    "Le véhicule doit appartenir au transporteur "
                    "qui propose l'offre."
                )
            })

        # Règle 3 : l'expédition doit appartenir à un chargeur
        if self.expedition_id:
            if (
                self.expedition.entreprise.type_entreprise
                != 'chargeur'
            ):
                raise ValidationError({
                    'expedition': (
                        "L'expédition doit appartenir à une "
                        "entreprise de type chargeur."
                    )
                })

            # Règle 4 : seules les expéditions publiées acceptent
            # de nouvelles offres
            if (
                self._state.adding
                and self.expedition.statut != 'publiee'
            ):
                raise ValidationError({
                    'expedition': (
                        "Une offre ne peut être créée que pour "
                        "une expédition publiée."
                    )
                })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Offre {self.pk} - {self.prix} DT"
