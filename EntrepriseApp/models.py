from django.db import models
from django .contrib.auth.models import AbstractUser

class utilisateur(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key = True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=[
                ('chargeur', 'Chargeur'),
                ('transporteur', 'Transporteur'),
            ],
            default='chargeur'
        )
    telephone = models.CharField(max_length=15, null = True ,blank =True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Entreprise(models.Model):

    matricule_fiscale = models.CharField(
        max_length=17,
        unique=True
    )

    type_entreprise = models.CharField(
        max_length=100,
        choices=[
            ('chargeur', 'Chargeur'),
            ('transporteur', 'Transporteur'),
        ],
        default='chargeur'
    )

    adresse = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    gerant = models.OneToOneField(utilisateur,on_delete=models.CASCADE ,related_name='entreprise')

