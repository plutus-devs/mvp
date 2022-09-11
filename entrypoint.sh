python plutus/manage.py collectstatic --no-input

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python plutus/manage.py createsuperuser --username "$SUPER_USER_NAME" --email "$SUPER_USER_EMAIL" --noinput

if [ "$ENVIRONMENT" = "production" ]; then
    ./wait-for.sh db:3306 -- make run-prod
elif [ "$ENVIRONMENT" = "development" ]; then
    ./wait-for.sh db:3306 -- make run-dev
else
    echo "Invalid environment"
    exit 1
fi
