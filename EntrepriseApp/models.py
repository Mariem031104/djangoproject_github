from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils import timezone


class Utilisateur(AbstractUser):
    # Format : AAuserNN (ex. 26user00)
    user_id = models.CharField(
        max_length=8,
        primary_key=True,
        validators=[
            RegexValidator(
                regex=r'^\d{2}user\d{2}$',
                message="Le format doit être AAuserNN."
            )
        ]
    )

    # Seuls les emails gmail.com sont acceptés
    email = models.EmailField(
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9._%+-]+@gmail\.com$',
                message="Seules les adresses gmail.com sont acceptées."
            )
        ]
    )

    role = models.CharField(
        max_length=20,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur'
    )

    telephone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        # Génération de l'identifiant à la première sauvegarde
        if not self.user_id:
            annee = timezone.now().year % 100
            prefixe = f"{annee:02d}user"

            derniers_ids = Utilisateur.objects.filter(
                user_id__startswith=prefixe
            ).values_list('user_id', flat=True)

            numeros = [
                int(uid[-2:])
                for uid in derniers_ids
                if uid[-2:].isdigit()
            ]

            prochain = max(numeros, default=-1) + 1

            if prochain > 99:
                raise ValidationError(
                    "Le nombre maximal de 100 utilisateurs "
                    "par année est atteint."
                )

            self.user_id = f"{prefixe}{prochain:02d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=100)

    matricule_fiscal = models.CharField(
        max_length=17,
        unique=True,
        validators=[
            RegexValidator(
                regex=(
                    r'^\d{7}[/ -]?[A-Za-z]'
                    r'[/ -]?[ABDNPEabdnpe]'
                    r'[/ -]?[MPCNEmpcne]'
                    r'[/ -]?\d{3}$'
                ),
                message="Le matricule fiscal tunisien est invalide."
            )
        ]
    )

    type_entreprise = models.CharField(
        max_length=100,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur'
    )

    # Minimum 20 caractères
    adresse = models.TextField(
        validators=[
            MinLengthValidator(
                20,
                "L'adresse doit contenir au moins 20 caractères."
            )
        ]
    )

    # Relation "gère" : Utilisateur 1 --- 1 Entreprise
    gerant = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='entreprise'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if self.adresse and len(self.adresse.strip()) < 20:
            raise ValidationError({
                'adresse': "L'adresse doit contenir au moins 20 caractères."
            })

    def __str__(self):
        return self.raison_sociale