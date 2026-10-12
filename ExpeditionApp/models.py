from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

from EntrepriseApp.models import Entreprise


class Expedition(models.Model):

    # =========================
    # RÉFÉRENCE
    # Format : EXP-AA-NNNNN
    # Exemple : EXP-26-00001
    # =========================

    reference = models.CharField(
        max_length=12,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^EXP-\d{2}-\d{5}$',
                message="La référence doit respecter le format EXP-AA-NNNNN."
            )
        ]
    )

    # =========================
    # INFORMATIONS EXPÉDITION
    # =========================

    date_souhaitee = models.DateField()

    ville_depart = models.CharField(
        max_length=100
    )

    ville_arrivee = models.CharField(
        max_length=100
    )

    poids_kg = models.IntegerField(
        validators=[
            MinValueValidator(
                1,
                "Le poids doit être supérieur à 0 kg."
            )
        ]
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    # =========================
    # STATUT
    # =========================

    statut = models.CharField(
        max_length=30,
        choices=[
            ('publiee', 'Publiée'),
            ('en_cours', 'En cours'),
            ('attribuee', 'Attribuée'),
            ('livree', 'Livrée'),
            ('annulee', 'Annulée'),
        ],
        default='publiee'
    )

    # =========================
    # ENTREPRISE
    # Une expédition doit être
    # créée par un CHARGEUR
    # =========================

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions'
    )

    # =========================
    # DATES
    # =========================

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================
    # VALIDATION MÉTIER
    # =========================

    def clean(self):
        super().clean()

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

    # =========================
    # GÉNÉRATION DE LA RÉFÉRENCE
    # Format : EXP-AA-NNNNN
    # Compteur remis à zéro chaque année
    # =========================

    @classmethod
    def _generate_reference(cls):
        annee = timezone.now().strftime('%y')

        prefixe = f"EXP-{annee}-"

        derniere_expedition = (
            cls.objects
            .filter(reference__startswith=prefixe)
            .order_by('-reference')
            .first()
        )

        if derniere_expedition:
            dernier_numero = int(
                derniere_expedition.reference[-5:]
            )
            compteur = dernier_numero + 1
        else:
            compteur = 1

        if compteur > 99999:
            raise ValidationError(
                "Le nombre maximum d'expéditions pour cette année est atteint."
            )

        return f"{prefixe}{compteur:05d}"

    # =========================
    # SAUVEGARDE
    # =========================

    def save(self, *args, **kwargs):

        if not self.reference:
            self.reference = self._generate_reference()

        self.full_clean()

        super().save(*args, **kwargs)

    # =========================
    # AFFICHAGE
    # =========================

    def __str__(self):
        return self.reference