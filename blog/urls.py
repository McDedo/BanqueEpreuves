from django.urls import path
from . import views

urlpatterns=[
    path('',views.home, name='home'),
    path('matiere/<int:matiere_id>/', views.epreuves_par_matiere, name='epreuves_par_matiere'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('epreuves/', views.liste_epreuves, name='epreuves'),
    path('epreuve/<int:epreuve_id>/apercu/', views.aperçu_epreuve, name='aperçu_epreuve'),
    path('epreuve/<int:epreuve_id>/telecharger/', views.telecharger_epreuve, name='telecharger_epreuve'),
    path("epreuves/matiere/<int:matiere_id>/", views.epreuves_par_matiere, name="epreuves_par_matiere"),
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('inscription/', views.register, name='register'),
]
