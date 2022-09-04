deps:
	python -m pip install -r requirements.txt

run:
	python plutus/manage.py runserver

setup_db:
	python plutus/manage.py makemigrations && python plutus/manage.py migrate

migrate:
	python plutus/manage.py migrate

clean:
	black plutus
