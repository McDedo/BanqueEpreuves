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
        "EPS",
        "Informatique",
        "Économie",
        "Technologie",
        "Anglais",
        "Espagnol",
        "Allemand"
    ]
    for nom in matieres:
        Matiere.objects.get_or_create(nom=nom)

class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20250608_0438'),  
    ]

    operations = [
        migrations.RunPython(add_matieres),
    ]
