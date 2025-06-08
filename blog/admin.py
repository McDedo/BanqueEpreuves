from django.contrib import admin
from .models import Epreuve, Matière, FicheCours

@admin.register(Epreuve)
class EpreuveAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at')

@admin.register(Matière)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom',)

@admin.register(FicheCours)
class FicheCoursAdmin(admin.ModelAdmin):
    list_display = ('titre', 'matiere', 'niveau', 'created_at')
