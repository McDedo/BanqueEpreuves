# Banque d'Épreuves

Banque d'Épreuves est une plateforme Django dédiée à l'accès et à la préparation des épreuves académiques. Elle permet aux étudiants de consulter des banques d’épreuves, des corrigés et des ressources pour mieux préparer leurs examens.

---

## 🚀 Fonctionnalités principales

- Consultation des épreuves classées par matières et niveaux  
- Téléchargement des corrigés  
- Interface administrateur pour gérer les ressources  
- Support multi-utilisateurs  
- Responsive design pour une utilisation sur mobile et desktop

---

## 🛠️ Installation et configuration

1. **Cloner le dépôt**

```bash
git clone https://github.com/ton-utilisateur/banque-epreuves.git
cd banque-epreuves

2. **Créer un environnement virtuel (recommandé)**

python -m venv env
source env/bin/activate    # macOS/Linux
env\Scripts\activate       # Windows

pip install -r requirements.txt

python manage.py migrate

