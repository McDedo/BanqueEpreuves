from django.shortcuts import render, get_object_or_404, redirect
import os
from .models import Epreuve, Matière, FicheCours
from django.conf import settings
from django.db.models import Q, Count
from django.http import FileResponse, Http404
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator
from itertools import chain
from operator import attrgetter
from django.core.mail import send_mail
from django.contrib import messages


def get_matiere_icon(nom):
    return {
        "Mathématiques": "📐",
        "Physique-Chimie": "⚛️",
        "Français": "📚",
        "SVT": "🔬",
        "Anglais": "🇬🇧",
        "Histoire-Géographie": "🌍",
        "Philosophie": "🤔",
        "EPS": "🏃",
        "Informatique": "💻",
        "Économie": "💰",
        "Technologie": "🔧",
        "Espagnol": "🗣️",
        "Allemand": "🗣️",
        "Arts Appliqués": "🎨",
    }.get(nom, "📘")

def home(request):
    matieres = Matière.objects.annotate(
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

    epreuves = Epreuve.objects.all()
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


def epreuves_par_matiere(request, matiere_id):
    matiere = Matière.objects.get(id=matiere_id)
    epreuves = Epreuve.objects.filter(matiere=matiere)
    fiches = FicheCours.objects.filter(matiere=matiere)
    context = {
        'epreuves': epreuves,
        'matiere': matiere,
        'fiches': fiches,
    }
    return render(request, 'epreuves_par_matiere.html', context)

 

def rechercher(request):
    query = request.GET.get('q', '')
    categorie = request.GET.get('categorie', '')

    epreuves = Epreuve.objects.all()
    fiches = FicheCours.objects.all()
    
    if query:
        epreuves = epreuves.filter(
            Q(titre__icontains=query) |
            Q(matiere__nom__icontains=query) |
            Q(niveau__icontains=query) |
            Q(annee__icontains=query)
        ).distinct()
        
        fiches = fiches.filter(
            Q(titre__icontains=query) |
            Q(matiere__nom__icontains=query) |
            Q(niveau__icontains=query) |
            Q(annee__icontains=query)
        ).distinct()
    
    if categorie:
        epreuves = epreuves.filter(niveau__iexact=categorie)
        fiches = fiches.filter(niveau__iexact=categorie)
            

    context = {
        'query': query,
        'categorie': categorie,
        'epreuves': epreuves,
        'fiches': fiches
    }

    return render(request, 'rechercher.html', context)

def liste_epreuves(request):
    epreuves = Epreuve.objects.all()
    matieres = Matière.objects.all()
    niveaux = Epreuve.objects.values_list('niveau', flat=True).distinct()

    query = request.GET.get('q')
    niveau = request.GET.get('niveau')
    matiere_id = request.GET.get('matiere')

    if query:
        epreuves = epreuves.filter(
            Q(titre__icontains=query) |
            Q(niveau__icontains=query) |
            Q(annee__icontains=query) |
            Q(matière__nom__icontains=query) 
        )

    for e in epreuves:
        e.icone = get_matiere_icon(e.matiere.nom)

    if niveau:
        epreuves = epreuves.filter(niveau=niveau)

    if matiere_id:
        epreuves = epreuves.filter(matière__id=matiere_id)

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

def aperçu_epreuve(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, pk=epreuve_id)
    return render(request, 'aperçu_epreuve.html', {'epreuve': epreuve})

def telecharger_epreuve(request, epreuve_id):
    try:
        epreuve = Epreuve.objects.get(pk=epreuve_id)
        fichier_path = epreuve.fichier.path
        return FileResponse(open(fichier_path, 'rb'), as_attachment=True, filename=os.path.basename(fichier_path))
    except Epreuve.DoesNotExist:
        raise Http404("Épreuve non trouvée.")

def epreuves_par_matiere(request, matiere_id):
    matiere = get_object_or_404(Matière, id=matiere_id)
    epreuves = Epreuve.objects.filter(matiere=matiere)
    fiches = FicheCours.objects.filter(matiere=matiere)
    context = {
        'epreuves': epreuves,
        'matiere': matiere,
        'fiches': fiches,
    }
    return render(request, "epreuves_par_matiere.html", context)

def liste_matieres(request):
    matieres = Matière.objects.all()
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

def liste_epreuves(request):
    epreuves = Epreuve.objects.all()
    return render(request, 'épreuves/liste.html', {'epreuves': epreuves})

def contact(request):
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        send_mail(
            f"Message de contact de {nom}",
            message,
            email,
            ['banqueepreuves@gmail.com'],
            fail_silently=False,
        )
        messages.success(request, "Merci pour votre message, nous vous répondrons bientôt.")
        return redirect('contact')

    return render(request, 'contact.html')

def fiches_cours(request):
    fiches = FicheCours.objects.all()
    matieres = Matière.objects.all()
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

def apercu_epreuve(request, epreuve_id):
    epreuve = get_object_or_404(Epreuve, pk=epreuve_id)
    return render(request, 'épreuves/apercu.html', {'epreuve': epreuve})

def apropos(request):
    return render(request, 'apropos.html')

def apercu_fiche(request, fiche_id):
    fiche = get_object_or_404(FicheCours, pk=fiche_id)
    return render(request, 'apercu_fiche.html', {'fiche': fiche})

def telecharger_fiche(request, fiche_id):
    fiche = get_object_or_404(FicheCours, id=fiche_id)

    fiche.telechargements += 1
    fiche.save()

    if not fiche.fichier:
        raise Http404("Fichier introuvable.")
    
    fichier_path = os.path.join(settings.MEDIA_ROOT, fiche.fichier.name)

    if not os.path.exists(fichier_path):
        raise Http404("Fichier introuvable.")
    return FileResponse(open(fichier_path, 'rb'), as_attachment=True, filename=os.path.basename(fiche.fichier.name)) 

def contenus_populaires(request):
    epreuves = Epreuve.objects.all()
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
    )[:15]  # Limiter aux 15 plus populaires
    
    return render(request, 'contenus_populaires.html', {'contenus': contenus})

    

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

def mentions_legales(request):
    return render(request, 'mentions_legales.html')

def cookies(request):
    return render(request, 'cookies.html')
