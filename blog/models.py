from django.db import models

# Create your models here.
class Matière(models.Model):
    nom = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom
    
class Epreuve(models.Model):
    NIVEAUX = [
        ('Tle', 'Terminale'),
        ('1ère', 'Première'),
        ('2nde', 'Seconde'),
        ('3e', 'Troisième'),
        ('4e', 'Quatrième'),
        ('5e', 'Cinquième'),
        ('6e', 'Sixième'),
        ('CI', 'Cours d\'Initiation'),
        ('CP', 'Cours Préparatoire'),
        ('CE1', 'Cours Élémentaire 1'),
        ('CE2', 'Cours Élémentaire 2'),
        ('CM1', 'Cours Moyen 1'),
        ('CM2', 'Cours Moyen 2'),
        ('6e', '6e'),
        ('5e', '5e'),
        ('4e', '4e'),
        ('3e', '3e'),
        ('2nde', '2nde'),
        ('1ère', '1ère'),
        ('Tle', 'Terminale'),
        ('BTS', 'BTS'),
        ('Licence', 'Licence'),
    ]

    titre = models.CharField(max_length=255)
    fichier = models.FileField(upload_to='epreuves/')
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    matiere = models.ForeignKey(Matière, on_delete=models.CASCADE)
    niveau = models.CharField(max_length=100, choices=NIVEAUX, default='Tle')
    annee = models.CharField(max_length=10, default='2024')
    telechargements = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre
    
class FicheCours(models.Model):
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    fichier = models.FileField(upload_to='fiches/')
    matiere = models.ForeignKey(Matière, on_delete=models.CASCADE)
    prix = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    niveau = models.CharField(max_length=50, choices=[
            ('Tle', 'Terminale'),
            ('1ère', 'Première'),
            ('2nde', 'Seconde'),
            ('3e', 'Troisième'),
            ('4e', 'Quatrième'),
            ('5e', 'Cinquième'),
            ('6e', 'Sixième'),
            ('CI', 'Cours d\'Initiation'),
            ('CP', 'Cours Préparatoire'),
            ('CE1', 'Cours Élémentaire 1'),
            ('CE2', 'Cours Élémentaire 2'),
            ('CM1', 'Cours Moyen 1'),
            ('CM2', 'Cours Moyen 2'),
        ], default='Tle')
    annee = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    telechargements = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.titre} ({self.niveau} - {self.annee})"