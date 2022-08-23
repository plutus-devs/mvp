run:
	poetry run python plutus/manage.py runserver

setup_db:
	poetry run python plutus/manage.py makemigrations && poetry run python plutus/manage.py migrate

migrate:
	poetry run python plutus/manage.py migrate