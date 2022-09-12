python plutus/manage.py collectstatic --no-input

if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs -d '\n')
fi

DJANGO_SUPERUSER_PASSWORD=$SUPER_USER_PASSWORD python plutus/manage.py createsuperuser --username "$SUPER_USER_NAME" --email "$SUPER_USER_EMAIL" --noinput

if [ "$ENVIRONMENT" = "production" ]; then
    ./wait-for.sh "$MYSQL_HOST":"$MYSQL_PORT" -- make run-prod
elif [ "$ENVIRONMENT" = "development" ]; then
    ./wait-for.sh "$MYSQL_HOST":"$MYSQL_PORT" -- make run-dev
else
    echo "Invalid environment"
    exit 1
fi
