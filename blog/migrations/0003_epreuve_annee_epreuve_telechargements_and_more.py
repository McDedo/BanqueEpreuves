# Generated by Django 5.2.1 on 2025-05-23 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_epreuve_matière_delete_matières_epreuve_matiere'),
    ]

    operations = [
        migrations.AddField(
            model_name='epreuve',
            name='annee',
            field=models.CharField(default='2024', max_length=10),
        ),
        migrations.AddField(
            model_name='epreuve',
            name='telechargements',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='epreuve',
            name='niveau',
            field=models.CharField(choices=[('Tle', 'Terminale'), ('1ère', 'Première'), ('2nde', 'Seconde'), ('3e', 'Troisième'), ('4e', 'Quatrième'), ('5e', 'Cinquième'), ('6e', 'Sixième'), ('CP', 'Cours Préparatoire'), ('CE1', 'Cours Élémentaire 1'), ('CE2', 'Cours Élémentaire 2'), ('CM1', 'Cours Moyen 1'), ('CM2', 'Cours Moyen 2'), ('6e', '6e'), ('5e', '5e'), ('4e', '4e'), ('3e', '3e'), ('2nde', '2nde'), ('1ère', '1ère'), ('Tle', 'Terminale'), ('BTS', 'BTS'), ('Licence', 'Licence')], default='Tle', max_length=100),
        ),
    ]
