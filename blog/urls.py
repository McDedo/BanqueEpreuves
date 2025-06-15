from django.urls import path, include
from django.contrib import admin
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Page d'accueil
    path('', views.home, name='home'),

    # Authentification
    path('accounts/', include('django.contrib.auth.urls')),
    path('inscription/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('mes-documents/', views.mes_documents, name='mes_documents'), 
    path("logout/", LogoutView.as_view(), name="logout"),


    # Epreuves
    path('epreuves/', views.liste_epreuves, name='epreuves'),
    path('epreuve/<int:epreuve_id>/apercu/', views.apercu_epreuve, name='apercu_epreuve'),
    path('epreuve/<int:epreuve_id>/telecharger/', views.telecharger_epreuve, name='telecharger_epreuve'),

    # Fiches de cours
    path('fiches-cours/', views.fiches_cours, name='fiches_cours'),
    path('fiche/<int:fiche_id>/apercu/', views.apercu_fiche, name='apercu_fiche'),
    path('fiche/<int:fiche_id>/telecharger/', views.telecharger_fiche, name='telecharger_fiche'),

    # Guides de formation
    path('guides-formation/', views.guides_formation, name='guides_formation'),
    path('guide/<int:guide_id>/telecharger/', views.telecharger_guide, name='telecharger_guide'),

    # Arrêtés
    path('arretes/', views.arretes, name='arretes'),
    path('arrete/<int:arrete_id>/telecharger/', views.telecharger_arrete, name='telecharger_arrete'),

    # Matieres
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matiere/<int:matiere_id>/', views.epreuves_par_matiere, name='epreuves_par_matiere'),

    # Recherche
    path('rechercher/', views.rechercher, name='rechercher'),

    # Pages supplémentaires
    path('apropos/', views.apropos, name='apropos'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('aide/', views.aide, name='aide'),
    path('signaler-probleme/', views.signaler_probleme, name='signaler_probleme'),

    # Légal 
    path('conditions/', views.conditions_utilisation, name='conditions_utilisation'),
    path('politique/', views.politique_confidentialite, name='politique_confidentialite'),
    path('mentions/', views.mentions_legales, name='mentions_legales'),
    path('cookies/', views.cookies, name='cookies'),

    # Contenus populaires et récents
    path('contenus-populaires/', views.contenus_populaires, name='populaires'),
    path('epreuves-recentes/', views.epreuves_recentes, name='epreuves_recentes'),
    path('fiches-recentes/', views.fiches_recentes, name='fiches_recentes'),

    # Actualités
    path('actualites/', views.actualites, name='actualites'),
]
