from django.db import models
from .models import Entreprise  # À ne pas ajouter si Entreprise est définie dans ce même fichier
from django.core.validators import MinValueValidator

class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=11, unique=True)
    capacite_kg = models.IntegerField(validators=[MinValueValidator(100,"capacite doit etre sup a 100 kg")])
    disponibilite = models.BooleanField(default=True)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    proprietaire = models.ForeignKey(
        'Entreprise',
        on_delete=models.CASCADE,
        related_name='vehicules'
    )

    def __str__(self):
        return self.immatriculation