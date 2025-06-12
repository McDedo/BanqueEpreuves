from django.db import models
from cloudinary_storage.storage import MediaCloudinaryStorage
from .constants import NIVEAUX


# Create your models here.
class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
class Epreuve(models.Model):
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    titre = models.CharField(max_length=255)
    fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    annee = models.CharField(max_length=10, default='2024')
    telechargements = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
class FicheCours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    annee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    telechargements = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.titre} ({self.niveau} - {self.annee})"