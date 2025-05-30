from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


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
    path('epreuves/', views.liste_epreuves, name='liste_epreuves'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('fiches-cours/', views.fiches_cours, name='fiches_cours'),
    path('epreuves/', views.epreuves, name='epreuves'),
]
