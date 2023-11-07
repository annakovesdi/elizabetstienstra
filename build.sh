set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --noinput
createsuperuser --noinput
python manage.py makemigrations && python manage.py migrate