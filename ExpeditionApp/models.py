from decimal import Decimal

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, RegexValidator
from django.utils import timezone

from EntrepriseApp.models import Entreprise


class Expedition(models.Model):

    # Format : EXP-AA-NNNNN (ex. EXP-26-00001)
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

    date_souhaitee = models.DateField()

    ville_depart = models.CharField(max_length=100)

    ville_arrivee = models.CharField(max_length=100)

    # Un poids nul (ou négatif) est refusé
    poids_kg = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(
                Decimal('0.01'),
                "Le poids doit être supérieur à 0 kg."
            )
        ]
    )

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
            ('annulee', 'Annulée'),
        ],
        default='publiee'
    )

    # Relation "publie (chargeur)" : Entreprise 1 --- * Expedition
    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='expeditions'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        # Règle métier : l'entreprise doit être un chargeur
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

    @classmethod
    def _generate_reference(cls):
        # Compteur remis à zéro chaque année
        annee = timezone.now().strftime('%y')
        prefixe = f"EXP-{annee}-"

        derniere = (
            cls.objects
            .filter(reference__startswith=prefixe)
            .order_by('-reference')
            .first()
        )

        if derniere:
            compteur = int(derniere.reference[-5:]) + 1
        else:
            compteur = 1

        if compteur > 99999:
            raise ValidationError(
                "Le nombre maximum d'expéditions pour cette année est atteint."
            )

        return f"{prefixe}{compteur:05d}"

    def save(self, *args, **kwargs):
        if not self.reference:
            self.reference = self._generate_reference()

        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.reference