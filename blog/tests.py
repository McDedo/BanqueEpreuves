from django.test import TestCase, Client
from django.urls import reverse
from .models import Epreuve, Matiere, FicheCours
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

class ViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.matiere = Matiere.objects.create(nom="Mathématiques")
        self.epreuve = Epreuve.objects.create(
            titre="Epreuve test",
            matiere=self.matiere,
            niveau="Tle",
            fichier=SimpleUploadedFile("test.pdf", b"file_content"),
            telechargements=5
        )
        self.fiche = FicheCours.objects.create(
            titre="Fiche test",
            matiere=self.matiere,
            niveau="Tle",
            fichier=SimpleUploadedFile("fiche.pdf", b"file_content"),
            telechargements=3
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_rechercher_view_with_query(self):
        response = self.client.get(reverse('rechercher') + '?q=test')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Epreuve test")
        self.assertContains(response, "Fiche test")

    @patch('cloudinary.utils.cloudinary_url')
    def test_telecharger_epreuve_view(self, mock_cloudinary_url):
        mock_cloudinary_url.return_value = ("https://cloudinary.com/testfile", {})
        response = self.client.get(reverse('telecharger_epreuve', args=[self.epreuve.id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "https://cloudinary.com/testfile")
        self.epreuve.refresh_from_db()
        self.assertEqual(self.epreuve.telechargements, 6)



