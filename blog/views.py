from django.shortcuts import render, get_object_or_404, redirect
from .models import Epreuve, Matière, FicheCours
from django.db.models import Q, Count
import os
from django.http import FileResponse, Http404
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator


# Create your views here.
def home(request):
    epreuves = Epreuve.objects.all()
    matieres = Matière.objects.all()
    context = {
        'epreuves': epreuves,
        'matieres': matieres
    }
    return render(request, 'index.html', context)

def epreuves_par_matiere(request, matiere_id):
    matiere = Matière.objects.get(id=matiere_id)
    epreuves = Epreuve.objects.filter(matiere=matiere)
    context = {
        'epreuves': epreuves,
        'matiere': matiere
    }
    return render(request, 'epreuves_par_matiere.html', context)

def home(request):
    context = {
        'maths_count': Epreuve.objects.filter(matiere__nom__icontains='Mathématiques').count(),
        'physique_count': Epreuve.objects.filter(matiere__nom__icontains='Physique-Chimie').count(),
        'francais_count': Epreuve.objects.filter(matiere__nom__icontains='Français').count(),
        'svt_count': Epreuve.objects.filter(matiere__nom__icontains='SVT').count(),
        'anglais_count': Epreuve.objects.filter(matiere__nom__icontains='Anglais').count(),
        'histoire_geo_count': Epreuve.objects.filter(matiere__nom__icontains='Histoire-Géographie').count(),
        'philosophie_count': Epreuve.objects.filter(matiere__nom__icontains='Philosophie').count(),
        'est_count': Epreuve.objects.filter(matiere__nom__icontains='EST').count(),
        'es_count': Epreuve.objects.filter(matiere__nom__icontains='Ar').count(),
        'sport_count': Epreuve.objects.filter(matiere__nom__icontains='EPS').count(),
        'info_count': Epreuve.objects.filter(matiere__nom__icontains='Informatique').count(),
        'eco_count': Epreuve.objects.filter(matiere__nom__icontains='Économie').count(),
        'techno_count': Epreuve.objects.filter(matiere__nom__icontains='Technologie').count(),
        'langues_count': Epreuve.objects.filter(matiere__nom__icontains='Langues').count(),
        'arts_appliques_count': Epreuve.objects.filter(matiere__nom__icontains='Arts Appliqués').count(),
        'maths_tech_count': Epreuve.objects.filter(matiere__nom__icontains='Mathématiques et Sciences de l\'Ingénieur').count(),
        'sciences_count': Epreuve.objects.filter(matiere__nom__icontains='Sciences').count(),
    }
    return render(request, 'index.html', context)

def rechercher(request):
    query = request.GET.get('q', '')
    resultats = []

    if query:
        resultats = Epreuve.objects.filter(
            Q(titre__icontains=query) |
            Q(matière__nom__icontains=query) |
            Q(niveau__icontains=query)
        ).distinct()

        context = {
            'query': query,
            'resultats': resultats
        }
        return render(request, 'rechercher.html', context)

def home(request):
    epreuves_populaires = Epreuve.objects.order_by('-telechargements')[:4]
    return render(request, 'index.html', {'epreuves_populaires': epreuves_populaires})

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

    return render(request, 'epreuves/liste.html', context)

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
    return render(request, "epreuves_par_matiere.html", {"matiere": matiere, "epreuves": epreuves})

def liste_matieres(request):
    matieres = Matière.objects.all()
    return render(request, 'liste_matieres.html', {'matieres': matieres})

def register(request):
    return render(request, 'register.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    matieres = Matière.objects.annotate(nb_epreuves=Count('epreuve'))

    for matiere in matieres:
        if matiere.nom == "Mathématiques":
            matiere.icon = "📐"
        elif matiere.nom == "Physique-Chimie":
            matiere.icon = "⚛️"
        elif matiere.nom == "Français":
            matiere.icon = "📚"
        elif matiere.nom == "SVT" or matiere.nom == "Sciences de la Vie et de la Terre":
            matiere.icon = "🔬"
        else:
            matiere.icon = "📘"
            
    return render(request, 'index.html', {'matieres': matieres})

def liste_epreuves(request):
    epreuves = Epreuve.objects.all()
    return render(request, 'epreuves/liste.html', {'epreuves': epreuves})

def contact(request):
    return render(request, 'contact.html')

def fiches_cours(request):
    fiches = FicheCours.objects.all().order_by('created_at')
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
    return render(request, 'epreuves/apercu.html', {'epreuve': epreuve})