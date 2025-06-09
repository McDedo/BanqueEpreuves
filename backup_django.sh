#!/bin/bash

# === CONFIGURATION ===
PROJECT_DIR="/McDEDO/codage/djangoprojects/banque_epreuves/BanqueEpreuves"         
BACKUP_DIR="/home/ton_utilisateur/sauvegardes"          # 📁 Dossier où stocker les backups
VENV_PATH="$PROJECT_DIR/venv/bin/activate"              # 🔁 Chemin vers ton environnement virtuel

# === SAUVEGARDE ===
cd "$PROJECT_DIR" || exit
source "$VENV_PATH"

# 📦 Sauvegarde avec date/heure dans le nom
BACKUP_FILE="db_backup_$(date +%F_%H-%M).json"
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > "$BACKUP_DIR/$BACKUP_FILE"

# 🧹 Nettoyer les anciens backups (plus de 7 jours)
find "$BACKUP_DIR" -name "*.json" -type f -mtime +7 -delete
