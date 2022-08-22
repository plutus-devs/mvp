run:
	poetry run python plutus/manage.py runserver

migrate:
	poetry run python plutus/manage.py makemigrations && poetry run python plutus/manage.py migrate