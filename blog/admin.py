from django.contrib import admin
from django.utils.html import format_html
from .models import Epreuve, Matiere, FicheCours
import re

@admin.register(Epreuve)
class EpreuveAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at', 'lien_fichier_cloudinary')

    def lien_fichier_cloudinary(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Voir fichier</a>', obj.fichier.url)
        return "Aucun fichier"
    
    lien_fichier_cloudinary.short_description = 'Fichier Cloudinary'

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(FicheCours)
class FicheCoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at', 'lien_fichier_cloudinary')

    def lien_fichier_cloudinary(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Voir fichier</a>', obj.fichier.url)
        return "Aucun fichier"
    
    lien_fichier_cloudinary.short_description = 'Fichier Cloudinary'

