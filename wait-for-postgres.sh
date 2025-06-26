#!/bin/sh

# Extraire l'URL
echo "⏳ Attente de PostgreSQL..."

until nc -z yamabiko.proxy.rlwy.net 30380; do
  echo "🚫 PostgreSQL pas encore prêt..."
  sleep 2
done

echo "✅ PostgreSQL est prêt !"
