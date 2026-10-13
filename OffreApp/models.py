
from django.db import models, transaction
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
        validators=[MinValueValidator(0.01)]
    )

    delai_jours = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
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

    def clean(self):
        super().clean()

        # Règle 1 : l'entreprise doit être un transporteur
        if self.transporteur_id:
            if self.transporteur.type_entreprise != 'transporteur':
                raise ValidationError({
                    'transporteur':
                    "L'entreprise doit être un transporteur."
                })

        # Règle 2 : le véhicule doit appartenir au transporteur
        if self.vehicule_id and self.transporteur_id:
            if self.vehicule.entreprise_id != self.transporteur_id:
                raise ValidationError({
                    'vehicule':
                    "Ce véhicule n'appartient pas au transporteur."
                })

        if self.expedition_id:

            # Le propriétaire de l'expédition doit être un chargeur
            if self.expedition.entreprise.type_entreprise != 'chargeur':
                raise ValidationError({
                    'expedition':
                    "L'expédition doit appartenir à un chargeur."
                })

            # Règle 3 : une nouvelle offre exige une expédition publiée
            if (
                self._state.adding
                and self.expedition.statut != 'publiee'
            ):
                raise ValidationError({
                    'expedition':
                    "L'expédition doit être publiée."
                })

            # Règle 4 : une seule offre proposée par transporteur
            offres_actives = Offre.objects.filter(
                expedition_id=self.expedition_id,
                transporteur_id=self.transporteur_id,
                statut='proposee'
            )

            if self.pk:
                offres_actives = offres_actives.exclude(pk=self.pk)

            if self.statut == 'proposee' and offres_actives.exists():
                raise ValidationError({
                    'transporteur':
                    "Ce transporteur possède déjà une offre proposée "
                    "pour cette expédition."
                })

        # Règle 6 : le véhicule doit être disponible
        if self.vehicule_id and self.statut == 'proposee':
            if not self.vehicule.disponible:
                raise ValidationError({
                    'vehicule':
                    "Ce véhicule n'est pas disponible."
                })

        # Règle 7 : compatibilité du type de véhicule et du poids
        if self.vehicule_id and self.expedition_id:
            poids = self.expedition.poids_kg
            type_vehicule = self.vehicule.type_vehicule

            capacites_max = {
                'camionnette': 1500,
                'camion_porteur': 19000,
                'semi_remorque': 26000,
                'fourgon': 3500,
            }

            capacite_max = capacites_max.get(type_vehicule)

            if capacite_max is None:
                raise ValidationError({
                    'vehicule':
                    "Type de véhicule non reconnu."
                })

            if poids > capacite_max or poids > self.vehicule.capacite_kg:
                raise ValidationError({
                    'vehicule':
                    "Le véhicule n'est pas adapté au poids "
                    "de cette expédition."
                })

    def save(self, *args, **kwargs):
        with transaction.atomic():

            # Vérifier les données avant l'enregistrement
            self.full_clean()

            # Enregistrer l'offre
            super().save(*args, **kwargs)

            # Règle 5 : cascade à l'acceptation
            if self.statut == 'acceptee':

                Expedition.objects.filter(
                    pk=self.expedition_id
                ).update(statut='attribuee')

                Offre.objects.filter(
                    expedition_id=self.expedition_id,
                    statut='proposee'
                ).exclude(
                    pk=self.pk
                ).update(statut='refusee')

    def __str__(self):
        return f"Offre {self.pk} - {self.prix} DT"
