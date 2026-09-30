include .env
export

init:
	sudo service postgresql start
	sudo -u postgres psql -c "DO \$$\$$ BEGIN IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '$(POSTGRES_USER)') THEN CREATE USER $(POSTGRES_USER) WITH PASSWORD '$(POSTGRES_PASSWORD)'; END IF; END \$$\$$;"
	sudo -iu postgres psql -tAc "SELECT 1 FROM pg_database WHERE datname='$(POSTGRES_DB)'" | grep -q 1 || sudo -iu postgres psql -c "CREATE DATABASE $(POSTGRES_DB) OWNER $(POSTGRES_USER);"
	pg_lsclusters

stop:
	sudo service postgresql stop

migrate:
	python manage.py makemigrations
	python manage.py migrate

delete:
	sudo -iu postgres psql -c "DROP DATABASE IF EXISTS $(POSTGRES_DB) WITH (FORCE);"
	sudo -iu postgres psql -c "DROP USER IF EXISTS $(POSTGRES_USER);"
	find . -path "*/migrations/0*.py" -delete
	find . -path "*/migrations/__pycache__" -type d -exec rm -rf {} +


