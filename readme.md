# Note command

- To enter in web container run: `docker exec -it mvp_web_1 /bin/bash`

  - Create superuser: `python plutus/manage.py createsuperuser`

  - Set up db: `python plutus/manage.py makemigrations`

  - Migrate db: `python plutus/manage.py migrate`
