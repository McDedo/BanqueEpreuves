# Generated by Django 5.2.1 on 2025-06-14 03:01

import cloudinary_storage.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0013_arrete_guideformation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actualite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=200)),
                ('contenu', models.TextField()),
                ('date_publication', models.DateField(auto_now_add=True)),
                ('fichier', models.FileField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='')),
                ('image', models.ImageField(blank=True, null=True, storage=cloudinary_storage.storage.MediaCloudinaryStorage(), upload_to='')),
                ('lien_externe', models.URLField(blank=True, null=True)),
            ],
        ),
    ]
