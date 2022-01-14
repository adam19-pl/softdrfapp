web: gunicorn drfproject.wsgi
release: python manage.py makemigrations drfapp
release: python manage.py migrate --run-syncdb
release: python manage.py collectstatic --noinput
