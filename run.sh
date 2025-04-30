#!/bin/bash

set -e

echo "📦 Virtual muhit aktivlashmoqda..."
source venv/bin/activate

echo "🚀 Gunicorn ishga tushmoqda..."
exec gunicorn config.wsgi:application \
  --bind 0.0.0.0:8000 \
  --workers 3 \
  --log-level info \
  --log-file gunicorn.log
