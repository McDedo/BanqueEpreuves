# Generated by Django 5.2.1 on 2025-06-01 00:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_epreuve_annee_epreuve_telechargements_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='epreuve',
            name='niveau',
            field=models.CharField(choices=[('Tle', 'Terminale'), ('1ère', 'Première'), ('2nde', 'Seconde'), ('3e', 'Troisième'), ('4e', 'Quatrième'), ('5e', 'Cinquième'), ('6e', 'Sixième'), ('CI', "Cours d'Initiation"), ('CP', 'Cours Préparatoire'), ('CE1', 'Cours Élémentaire 1'), ('CE2', 'Cours Élémentaire 2'), ('CM1', 'Cours Moyen 1'), ('CM2', 'Cours Moyen 2'), ('6e', '6e'), ('5e', '5e'), ('4e', '4e'), ('3e', '3e'), ('2nde', '2nde'), ('1ère', '1ère'), ('Tle', 'Terminale'), ('BTS', 'BTS'), ('Licence', 'Licence')], default='Tle', max_length=100),
        ),
        migrations.CreateModel(
            name='FicheCours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('fichier', models.FileField(upload_to='fiches/')),
                ('niveau', models.CharField(choices=[('Tle', 'Terminale'), ('1ère', 'Première'), ('2nde', 'Seconde'), ('3e', 'Troisième'), ('4e', 'Quatrième'), ('5e', 'Cinquième'), ('6e', 'Sixième'), ('CI', "Cours d'Initiation"), ('CP', 'Cours Préparatoire'), ('CE1', 'Cours Élémentaire 1'), ('CE2', 'Cours Élémentaire 2'), ('CM1', 'Cours Moyen 1'), ('CM2', 'Cours Moyen 2')], default='Tle', max_length=50)),
                ('annee', models.PositiveIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fiches', to='blog.matière')),
            ],
        ),
    ]
