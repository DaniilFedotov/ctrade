set -e

echo "&{0}: running migrations."
python manage.py makemigrations
python manage.py migrate

echo "&{0}: running import of settings data."
python manage.py importsettings

echo "&{0}: running server."
python manage.py runserver 0:8000