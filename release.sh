#!/bin/bash
set -e

echo "📦 Virtual muhit aktivlashmoqda..."
source venv/bin/activate

echo "🧱 Ma'lumotlar bazasini migratsiya qilinyapti..."
python manage.py migrate

echo "📁 Static fayllar yig‘ilmoqda..."
python manage.py collectstatic --noinput

echo "✅ Release jarayoni yakunlandi."
