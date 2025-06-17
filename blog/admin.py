from django.contrib import admin
from django.utils.html import format_html
from .models import Epreuve, Matiere, FicheCours, GuideFormation, Arrete, Actualite
import re

@admin.register(Epreuve)
class EpreuveAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at', 'lien_drive','lien_drive_corrige' )

    def lien_drive(self, obj):
        if obj.lien_drive:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_drive)
        return "Aucun lien"
    
    def lien_drive_corrige(self, obj):
        if obj.lien_drive_corrige:
            return format_html('<a href="{}" target="_blank">Voir le lien corrigé</a>', obj.lien_drive_corrige)
        return "Aucun lien corrigé"
    
    lien_drive.short_description = 'Lien Drive'
    lien_drive_corrige.short_description = 'Lien Drive Corrigé'

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(FicheCours)
class FicheCoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at', 'lien_drive')

    def lien_drive(self, obj):
        if obj.lien_drive:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_drive)
        return "Aucun lien"
    
    lien_drive.short_description = 'Lien Drive'

@admin.register(GuideFormation)
class GuideFormationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'annee', 'created_at', 'lien_drive')

    def lien_drive(self, obj):
        if obj.lien_drive:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_drive)
        return "Aucun lien"
    
    lien_drive.short_description = 'Lien Drive'

@admin.register(Arrete)
class ArreteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'created_at', 'lien_drive')
    def lien_drive(self, obj):
        if obj.lien_drive:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_drive)
        return "Aucun lien" 
    
    lien_drive.short_description = 'Lien Drive'


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('titre', 'date_publication', 'apercu_contenu', 'lien_drive', 'lien_externe')

    def apercu_contenu(self, obj):
        return (obj.contenu[:75] + '...') if len(obj.contenu) > 75 else obj.contenu
    apercu_contenu.short_description = 'Contenu'

    def lien_drive(self, obj):
        if obj.lien_drive:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_drive)
        return "Aucun lien"

    def lien_externe(self, obj):
        if obj.lien_externe:
            return format_html('<a href="{}" target="_blank">Voir le lien</a>', obj.lien_externe)
        return "Aucun lien"
    lien_externe.short_description = 'Lien externe'
