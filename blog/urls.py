from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns=[
    path('',views.home, name='home'),
    path('matiere/<int:matiere_id>/', views.epreuves_par_matiere, name='epreuves_par_matiere'),
    path('rechercher/', views.rechercher, name='rechercher'),
    path('epreuves/', views.liste_epreuves, name='epreuves'),
    path('epreuve/<int:epreuve_id>/apercu/', views.aperçu_epreuve, name='aperçu_epreuve'),
    path('apropos/', views.apropos, name='apropos'),
    path('epreuve/<int:epreuve_id>/telecharger/', views.telecharger_epreuve, name='telecharger_epreuve'),
    path('matieres/<int:matiere_id>/epreuves/', views.epreuves_par_matiere, name='epreuves_par_matiere'),
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('inscription/', views.register, name='register'),
    path('epreuves/', views.liste_epreuves, name='liste_epreuves'),
    path('contact/', views.contact, name='contact'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('fiches-cours/', views.fiches_cours, name='fiches_cours'),
    path('epreuves/', views.liste_epreuves, name='épreuves'),
    path('epreuves/<int:epreuve_id>/apercu/', views.apercu_epreuve, name='apercu_epreuve'),
    path('fiche/<int:fiche_id>/apercu/', views.apercu_fiche, name='aperçu_fiche'),
    path('fiche/<int:fiche_id>/telecharger/', views.telecharger_fiche, name='telecharger_fiche'),
    path('contenus-populaires/', views.contenus_populaires, name='populaires'),
    path('epreuves-recentes/', views.epreuves_recentes, name='epreuves_recentes'),
    path('fiches-recentes/', views.fiches_recentes, name='fiches_recentes'),
    path('faq/', views.faq, name='faq'),
    path('aide/', views.aide, name='aide'),
    path('signaler-probleme/', views.signaler_probleme, name='signaler_probleme'),
    path('conditions/', views.conditions_utilisation, name='conditions_utilisation'),
    path('politique/', views.politique_confidentialite, name='politique_confidentialite'),
    path('mentions/', views.mentions_legales, name='mentions_legales'),
    path('cookies/', views.cookies, name='cookies'),
]
