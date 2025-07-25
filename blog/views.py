from django.shortcuts import render, get_object_or_404, redirect
import os
from .models import Epreuve, Matiere, FicheCours, GuideFormation, Arrete, Actualite
from django.conf import settings
from django.db.models import Q, Count
from django.http import FileResponse, Http404
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter
from django.core.mail import send_mail
from django.contrib import messages
from django.http import Http404
from .utils import get_matiere_icon
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
import requests



def home(request):
    matieres = Matiere.objects.annotate(
        nb_epreuves=Count('epreuve'),
        nb_fiches=Count('fichecours')
    )

    for matiere in matieres:
        if matiere.nom == "Mathématiques":
            matiere.icon = "📐"
        elif matiere.nom == "Physique-Chimie":
            matiere.icon = "⚛️"
        elif matiere.nom == "Français":
            matiere.icon = "📚"
        elif matiere.nom in ["SVT", "Sciences de la Vie et de la Terre"]:
            matiere.icon = "🔬"
        else:
            matiere.icon = "📘"

    epreuves = Epreuve.objects.all().select_related('matiere')
    fiches = FicheCours.objects.all()

    for e in epreuves:
        e.type_contenu = 'epreuve'
        e.icon = get_matiere_icon(e.matiere.nom if e.matiere else "")

    for f in fiches:
        f.type_contenu = 'fiche'
        f.icon = get_matiere_icon(f.matiere.nom if f.matiere else "")

    contenus = sorted(
        chain(epreuves, fiches),
        key=attrgetter('telechargements'),
        reverse=True
    )[:5]  # Limiter aux 5 plus populaires

    return render(request, 'index.html', {
        'matieres': matieres,
        'contenus_populaires': contenus,
    })


#def epreuves_par_matiere(request, matiere_id):
    #matiere = get_object_or_404(Matiere, id=matiere_id)
    #epreuves = Epreuve.objects.filter(matiere=matiere)
    #fiches = FicheCours.objects.filter(matiere=matiere)
    #context = {
     #   'epreuves': epreuves,
      #  'matiere': matiere,
       # 'fiches': fiches,
    #}
    #return render(request, 'epreuves_par_matiere.html', context)

def contenu_par_matiere(request, id):
    matiere = get_object_or_404(Matiere, pk=id)
    epreuves = Epreuve.objects.filter(matiere=matiere)
    fiches = FicheCours.objects.filter(matiere=matiere)
    guides = GuideFormation.objects.filter(matiere=matiere)

    return render(request, "epreuves_par_matieres.html", {
        "matiere": matiere,
        "epreuves": epreuves,
        "fiches": fiches,
        "guides": guides,
    }) 

from .models import Epreuve, FicheCours, Matiere
from django.db.models import Q


from .models import Epreuve, FicheCours, GuideFormation, Matiere

def rechercher(request):
    # Récupérer les paramètres GET
    categorie = request.GET.get('categorie', '')
    niveau = request.GET.get('niveau', '')
    matiere_id = request.GET.get('matiere', '')
    annee = request.GET.get('annee', '')

    # Base QuerySet
    epreuves = Epreuve.objects.all()
    fiches = FicheCours.objects.all()
    guides = GuideFormation.objects.all()

    # Filtrage par niveau
    if niveau:
        epreuves = epreuves.filter(niveau__iexact=niveau)
        fiches = fiches.filter(niveau__iexact=niveau)
        guides = guides.filter(niveau__iexact=niveau)

    # Filtrage par matière (par ID)
    if matiere_id:
        epreuves = epreuves.filter(matiere__id=matiere_id)
        fiches = fiches.filter(matiere__id=matiere_id)
        guides = guides.filter(matiere__id=matiere_id)

    # Filtrage par année
    if annee:
        epreuves = epreuves.filter(annee=annee)
        fiches = fiches.filter(annee=annee)
        guides = guides.filter(annee=annee)

    # Filtrage par type de contenu (catégorie)
    if categorie == 'Epreuve':
        fiches = fiches.none()
        guides = guides.none()
    elif categorie == 'Fiches_cours':
        epreuves = epreuves.none()
        guides = guides.none()
    elif categorie == 'Guide_formation':
        epreuves = epreuves.none()
        fiches = fiches.none()

    # Pour les listes de filtres dynamiques
    matieres = Matiere.objects.all().order_by('nom')
    annees = Epreuve.objects.values_list('annee', flat=True).distinct().order_by('-annee')

    context = {
        'categorie': categorie,
        'niveau': niveau,
        'matiere_id': matiere_id,
        'annee': annee,
        'epreuves': epreuves,
        'fiches': fiches,
        'guides': guides,
        'matieres': matieres,
        'annees': annees,
    }

    return render(request, 'rechercher.html', context)

    

def liste_epreuves(request):
    epreuves = Epreuve.objects.all()
    matieres = Matiere.objects.all()
    niveaux = Epreuve.objects.values_list('niveau', flat=True).distinct()

    query = request.GET.get('q')
    niveau = request.GET.get('niveau')
    matiere_id = request.GET.get('matiere')

    if query:
        epreuves = epreuves.filter(
            Q(titre__icontains=query) |
            Q(niveau__icontains=query) |
            Q(annee__icontains=query) |
            Q(matiere__nom__icontains=query) 
        )

    for e in epreuves:
        e.icone = get_matiere_icon(e.matiere.nom)

    if niveau:
        epreuves = epreuves.filter(niveau=niveau)

    if matiere_id:
        epreuves = epreuves.filter(matiere__id=matiere_id)

    paginator = Paginator(epreuves, 10)  # 10 epreuves par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'epreuves': page_obj,
        'matieres': matieres,
        'niveaux': niveaux,
        'page_obj': page_obj,
    }

    return render(request, 'épreuves/liste.html', context)

@login_required
def telecharger_epreuve(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    epreuve.telechargements += 1
    epreuve.save()

    epreuve.utilisateurs_telechargeurs.add(request.user)

    url = epreuve.lien_telechargement()

    if not url:
        raise Http404("Lien de téléchargement introuvable.")

    r = requests.get(url, stream=True)
    if r.status_code != 200:
        raise Http404("Impossible de récupérer le fichier.")
    
    response = HttpResponse(r.raw, content_type=r.headers.get('Content-Type', 'application/octet-stream'))
    response['Content-Disposition'] = f'attachment; filename="{epreuve.titre}.pdf"'
    
    return response
    

def liste_matieres(request):
    matieres = Matiere.objects.all()
    return render(request, 'liste_matieres.html', {'matieres': matieres})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def contact(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f"Message de contact de {nom}",
            message,
            email,
            ['actucoursepreuves@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "Merci pour votre message, nous vous répondrons bientôt.")
        return redirect('contact')

    return render(request, 'contact.html')

def fiches_cours(request):
    fiches = FicheCours.objects.all()
    matieres = Matiere.objects.all()
    niveaux = FicheCours.objects.values_list('niveau', flat=True).distinct()

    query = request.GET.get('q')
    niveau = request.GET.get('niveau')
    matiere_id = request.GET.get('matiere')
    
    if query:
        fiches = fiches.filter(
             titre__icontains=query
        )| fiches.filter(
            annee__icontains=query
        ) | fiches.filter(
            niveau__icontains=query
        ) | fiches.filter(matiere__nom__icontains=query
        )

    for fiche in fiches:
        fiche.icone = get_matiere_icon(fiche.matiere.nom)

    if niveau:
        fiches = fiches.filter(niveau=niveau)

    if matiere_id:
        fiches = fiches.filter(matiere__id=matiere_id)

    context = {
        'fiches': fiches,
        'matieres': matieres,
        'niveaux': niveaux,
    }
    return render(request, 'fiches_cours.html', context)  

def epreuves(request):
    return render(request, 'epreuves.html')

def apropos(request):
    return render(request, 'apropos.html')

@login_required
def telecharger_fiche(request, fiche_id):
    fiche = get_object_or_404(FicheCours, id=fiche_id)

    fiche.telechargements += 1
    fiche.save()

    fiche.utilisateurs_telechargeurs.add(request.user)
    
    url = fiche.lien_telechargement()

    if not url:
        raise Http404("Lien de téléchargement introuvable.")
    
    return redirect(url)
    

def contenus_populaires(request):
    epreuves = Epreuve.objects.all()
    fiches = FicheCours.objects.all()
    guides = Guide.objects.all()

    # Ajouter des attributs dynamiques
    for e in epreuves:
        e.type_contenu = 'epreuve'
        e.icon = get_matiere_icon(e.matiere.nom if e.matiere else "")

    for f in fiches:
        f.type_contenu = 'fiche'
        f.icon = get_matiere_icon(f.matiere.nom if f.matiere else "")

    for g in guides:
        g.type_contenu = 'guide'
        g.icon = get_matiere_icon(g.matiere.nom if g.matiere else "")

    # Fusionner et trier tous les contenus
    tous_les_contenus = sorted(
        chain(epreuves, fiches, guides),
        key=attrgetter('telechargements'),
        reverse=True
    )

    # Pagination
    paginator = Paginator(tous_les_contenus, 8)  # 8 contenus par page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, 'contenus_populaires.html', {'page_obj': page_obj})

def epreuves_recentes(request):
    epreuves = Epreuve.objects.order_by('-created_at')[:10]
    for e in epreuves:
        e.icon = get_matiere_icon(e.matiere.nom if e.matiere else "")

    return render(request, 'epreuves_recentes.html', {'epreuves': epreuves})

def fiches_recentes(request):
    fiches = FicheCours.objects.order_by('-created_at')[:10]
    for f in fiches:
        f.icon = get_matiere_icon(f.matiere.nom if f.matiere else "")

    return render(request, 'fiches_recentes.html', {'fiches': fiches})

def faq(request):
    return render(request, 'faq.html')

def aide(request):
    return render(request, 'aide.html')

def signaler_probleme(request):
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        description = request.POST.get('description')

        messages.success(request, "Merci, votre problème a bien été signalé. Nous allons le traiter rapidement.")
        return redirect('home')  # Rediriger vers la page d'accueil après le signalement

    return render(request, 'signaler_probleme.html')

def conditions_utilisation(request):
    return render(request, 'conditions_utilisation.html')

def politique_confidentialite(request):
    return render(request, 'politique_confidentialite.html')

def cookies(request):
    return render(request, 'cookies.html')

def guides_formation(request):
    guides = GuideFormation.objects.all()
    matieres = Matiere.objects.all()
    niveaux = GuideFormation.objects.values_list('niveau', flat=True).distinct()

    query = request.GET.get('q')
    niveau = request.GET.get('niveau')
    matiere_id = request.GET.get('matiere')
    
    if query:
        guides = guides.filter(
            Q(titre__icontains=query) |
            Q(annee__icontains=query) |
            Q(niveau__icontains=query) |
            Q(matiere__nom__icontains=query)
        )

    for guide in guides:
        guide.icone = get_matiere_icon(guide.matiere.nom)

    if niveau:
        guides = guides.filter(niveau=niveau)

    if matiere_id:
        guides = guides.filter(matiere__id=matiere_id)

    context = {
        'guides': guides,
        'matieres': matieres,
        'niveaux': niveaux,
    }
    return render(request, 'guides_formation.html', context)

@login_required
def telecharger_guide(request, guide_id):
    guide = get_object_or_404(GuideFormation, id=guide_id)
    guide.telechargements += 1
    guide.save()

    guide.utilisateurs_telechargeurs.add(request.user)

    url = guide.lien_telechargement()

    if not url:
        raise Http404("Lien de téléchargement introuvable.")
    
    return redirect(url)

def arretes(request):
    arretes = Arrete.objects.order_by('-date_publication')
    return render(request, 'arretes.html', {'arretes': arretes})

@login_required
def telecharger_arrete(request, arrete_id):
    arrete = get_object_or_404(Arrete, id=arrete_id)

    url = arrete.lien_telechargement()

    arrete.utilisateurs_telechargeurs.add(request.user)

    if not url:
        raise Http404("Lien de téléchargement introuvable.")
    
    return redirect(url)

def actualites(request):
    query = request.GET.get('q')
    actualites = Actualite.objects.all().order_by('-date_publication')

    if query:
        actualites = actualites.filter(
            Q(titre__icontains=query) |
            Q(contenu__icontains=query)
        )

    return render(request, 'actualites.html', {
        'actualites': actualites,
        'query': query,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mes_documents')  
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

@login_required
def mes_documents(request):
    epreuves = Epreuve.objects.filter(utilisateurs_telechargeurs=request.user)
    fiches = FicheCours.objects.filter(utilisateurs_telechargeurs=request.user)
    guides = GuideFormation.objects.filter(utilisateurs_telechargeurs=request.user)

    return render(request, "mes_documents.html", {
        "epreuves": epreuves,
        "fiches": fiches,
        "guides": guides,
    })

@login_required
def telecharger_corrige(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, id=epreuve_id)
    url = epreuve.lien_telechargement_corrige()

    epreuve.utilisateurs_telechargeurs.add(request.user)

    if not url:
        raise Http404("Corrigé non disponible pour cette épreuve.")

    return redirect(url)
