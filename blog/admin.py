from django.contrib import admin
from django.utils.html import format_html
from .models import Epreuve, Matiere, FicheCours, GuideFormation, Arrete, Actualite
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

@admin.register(GuideFormation)
class GuideFormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'annee', 'created_at', 'lien_fichier_cloudinary')

    def lien_fichier_cloudinary(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Voir fichier</a>', obj.fichier.url)
        return "Aucun fichier"
    
    lien_fichier_cloudinary.short_description = 'Fichier Cloudinary'

@admin.register(Arrete)
class ArreteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'created_at', 'lien_fichier_cloudinary')

    def lien_fichier_cloudinary(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Voir fichier</a>', obj.fichier.url)
        return "Aucun fichier"

    lien_fichier_cloudinary.short_description = 'Fichier Cloudinary'

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'apercu_contenu', 'lien_fichier_cloudinary', 'lien_externe_affiche')

    def apercu_contenu(self, obj):
        return (obj.contenu[:75] + '...') if len(obj.contenu) > 75 else obj.contenu
    apercu_contenu.short_description = 'Contenu'

    def lien_fichier_cloudinary(self, obj):
        if obj.fichier:
            return format_html('<a href="{}" target="_blank">Voir fichier</a>', obj.fichier.url)
        return "Aucun fichier"
    lien_fichier_cloudinary.short_description = 'Fichier Cloudinary'

    def lien_externe_affiche(self, obj):
        if obj.lien_externe:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_externe)
        return "Aucun lien"
    lien_externe_affiche.short_description = 'Lien externe'
