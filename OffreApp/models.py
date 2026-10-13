from decimal import Decimal

from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from ExpeditionApp.models import Expedition
from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule


# Règle 7 : poids maximum (en kg) transportable selon le type de véhicule
POIDS_MAX_PAR_TYPE = {
    'camionnette': 1500,
    'fourgon': 3500,
    'camion_porteur': 19000,
    'semi_remorque': 26000,
}


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
                Decimal('0.01'),
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

    date_proposition = models.DateField(auto_now_add=True)

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

    # ------------------------------------------------------------------
    # Règles métier
    # ------------------------------------------------------------------
    def clean(self):
        super().clean()

        # Règle 1 : seule une entreprise transporteur peut créer une offre
        if self.transporteur_id:
            if self.transporteur.type_entreprise != 'transporteur':
                raise ValidationError({
                    'transporteur': "L'entreprise doit être un transporteur."
                })

        # Règle 2 : le véhicule appartient au transporteur de l'offre
        if self.vehicule_id and self.transporteur_id:
            if self.vehicule.entreprise_id != self.transporteur_id:
                raise ValidationError({
                    'vehicule': "Ce véhicule n'appartient pas au transporteur."
                })

        if self.expedition_id:

            # Règle 3 : nouvelle offre => expédition publiée
            if self._state.adding and self.expedition.statut != 'publiee':
                raise ValidationError({
                    'expedition': (
                        "Une offre ne peut être créée que sur "
                        "une expédition publiée."
                    )
                })

            # Règle 4 : une seule offre "proposee" par transporteur
            # et par expédition
            if self.statut == 'proposee' and self.transporteur_id:
                doublons = Offre.objects.filter(
                    expedition_id=self.expedition_id,
                    transporteur_id=self.transporteur_id,
                    statut='proposee',
                )
                if self.pk:
                    doublons = doublons.exclude(pk=self.pk)

                if doublons.exists():
                    raise ValidationError({
                        'transporteur': (
                            "Ce transporteur a déjà une offre proposée "
                            "pour cette expédition."
                        )
                    })

            # Accepter une offre n'a de sens que sur une expédition publiée
            if self.statut == 'acceptee':
                deja_acceptee = (
                    self.pk
                    and Offre.objects.filter(
                        pk=self.pk, statut='acceptee'
                    ).exists()
                )
                if not deja_acceptee and self.expedition.statut != 'publiee':
                    raise ValidationError({
                        'statut': (
                            "Seule une offre sur une expédition publiée "
                            "peut être acceptée."
                        )
                    })

        if self.vehicule_id:

            # Règle 6 : véhicule indisponible => pas de nouvelle offre
            if self._state.adding and not self.vehicule.disponible:
                raise ValidationError({
                    'vehicule': "Ce véhicule n'est pas disponible."
                })

            # Règle 7 : compatibilité type de véhicule / poids
            if self.expedition_id:
                poids_max = POIDS_MAX_PAR_TYPE.get(self.vehicule.type_vehicule)

                if poids_max is None:
                    raise ValidationError({
                        'vehicule': "Type de véhicule non reconnu."
                    })

                poids = self.expedition.poids_kg
                if (
                    poids > poids_max
                    or poids > self.vehicule.capacite_kg
                ):
                    raise ValidationError({
                        'vehicule': (
                            "Le véhicule n'est pas adapté au poids "
                            "de cette expédition."
                        )
                    })

    def save(self, *args, **kwargs):
        with transaction.atomic():
            self.full_clean()
            super().save(*args, **kwargs)

            # Règle 5 : cascade à l'acceptation
            if self.statut == 'acceptee':
                Expedition.objects.filter(
                    pk=self.expedition_id
                ).update(statut='attribuee')

                Offre.objects.filter(
                    expedition_id=self.expedition_id,
                    statut='proposee',
                ).exclude(pk=self.pk).update(statut='refusee')

    def __str__(self):
        return f"Offre {self.pk} - {self.prix} DT"