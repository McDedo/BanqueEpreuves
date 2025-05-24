from django.shortcuts import render, get_object_or_404, redirect
from .models import Epreuve, Matière
from django.db.models import Q
import os
from django.http import FileResponse, Http404
from .forms import CustomUserCreationForm


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
    return render(request, 'epreuves.html', {'epreuves': epreuves})

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