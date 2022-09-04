python plutus/manage.py makemigrations
python plutus/manage.py migrate --no-input
python plutus/manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python plutus/manage.py createsuperuser --username $SUPER_USER_NAME --email $SUPER_USER_EMAIL --noinput

./wait-for.sh db:3306 -- python plutus/manage.py runserver 0.0.0.0:8000
