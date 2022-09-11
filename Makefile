deps:
	python -m pip install -r requirements.txt

run-dev: setup_db
	python plutus/manage.py runserver 0.0.0.0:8000

setup_db:
	python plutus/manage.py makemigrations && python plutus/manage.py migrate

migrate:
	python plutus/manage.py migrate

clean:
	black plutus

run-prod: setup_db
	cd plutus && gunicorn plutus.wsgi app:app -b 0.0.0.0:8000
