from django.db import migrations

def add_matieres(apps, schema_editor):
    Matiere = apps.get_model('blog', 'Matière')
    matieres = [
        "Mathématiques",
        "Physique-Chimie",
        "Français",
        "SVT",
        "Histoire-Géographie",
        "Philosophie",
        "EST",
        "Ar",
        "EPS",
        "Informatique",
        "Économie",
        "Technologie",
        "Langues",
        "Arts Appliqués",
        "Mathématiques et Sciences de l'Ingénieur",
        "Sciences de la Vie et de la Terre",
    ]
    for nom in matieres:
        Matiere.objects.get_or_create(nom=nom)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_fichecours_prix'),  
    ]

    operations = [
        migrations.RunPython(add_matieres),
    ]
