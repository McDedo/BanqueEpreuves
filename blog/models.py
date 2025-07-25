from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from .constants import NIVEAUX
import re


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
    #fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    #fichier_corrige = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    lien_drive = models.URLField(blank=True, null=True)
    lien_drive_corrige = models.URLField(blank=True, null=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    annee = models.PositiveIntegerField(default='2024')
    telechargements = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    utilisateurs_telechargeurs = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.titre
    
    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)
    
    def lien_telechargement_corrige(self):
        return self._extract_download_url(self.lien_drive_corrige)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url
    
    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])


    
class FicheCours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    #fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    lien_drive = models.URLField(blank=True, null=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    annee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    telechargements = models.PositiveIntegerField(default=0)

    utilisateurs_telechargeurs = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"{self.titre} ({self.niveau} - {self.annee})"
    
    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url

    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])


class GuideFormation(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    #fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    lien_drive = models.URLField(blank=True, null=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    annee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    telechargements = models.PositiveIntegerField(default=0)

    utilisateurs_telechargeurs = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return f"Guide: {self.titre} ({self.niveau} - {self.annee})"
    
    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url
    
    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])


class Arrete(models.Model):
    titre = models.CharField(max_length=200)
    #fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    lien_drive = models.URLField(blank=True, null=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    date_publication = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Arrêté: {self.titre} - {self.date_publication}"
    
    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url
    
    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])


class Actualite(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    #fichier = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    #image = models.ImageField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    lien_drive = models.URLField(blank=True, null=True)
    lien_externe = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titre
    
    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url

    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])


class Document(models.Model):
    user = models.ForeignKey(User, related_name="documents", on_delete=models.CASCADE)
    #file = models.FileField(storage=MediaCloudinaryStorage(), blank=True, null=True)
    lien_drive = models.URLField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Document de {self.user.username} - {self.uploaded_at.strftime('%Y-%m-%d')}"

    def lien_telechargement(self):
        return self._extract_download_url(self.lien_drive)

    def _extract_download_url(self, url):
        match = re.search(r'/d/([a-zA-Z0-9_-]+)', url or "")
        if match:
            file_id = match.group(1)
            return f'https://drive.google.com/uc?export=download&id={file_id}'
        return url
    
    def get_telechargement_url(self):
        return reverse('telecharger_epreuve', args=[self.id])
