#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Install Node.js dependencies and build Tailwind CSS
npm ci --omit=optional --no-audit --no-fund || npm install --no-audit --no-fund
npm run build:css

python manage.py collectstatic --no-input
python manage.py migrate
