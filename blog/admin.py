from django.contrib import admin
from .models import Epreuve, Matière, FicheCours

# Register your models here.
admin.site.register(Epreuve)
admin.site.register(Matière)
admin.site.register(FicheCours)
