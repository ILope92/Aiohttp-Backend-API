PROJECT_NAME ?= backend_api
VERSION = $(shell python3 setup.py --version | tr '+' '-')
PROJECT_NAMESPACE ?= lening
REGISTRY_IMAGE ?= $(PROJECT_NAMESPACE)/$(PROJECT_NAME)

all:
	@echo "make clean		- Remove files created by distutils"
	@echo "make sdist		- Make source distribution"
	@echo "make postgres	- Start postgres container"
	@echo "make docker		- Build a docker image"
	@echo "make upload		- Upload docker image to the registry"
	@echo "make devenv      - install enviroment python3.8"
	@echo "make compose     - install enviroment python3.8"
	@exit 0

clean:
	rm -fr *.egg-info dist

devenv: clean
	rm -rf env
	# создаем новое окружение
	apt-get install python3-venv
	python3.8 -m venv env
	env/bin/python3.8 -m pip install pip --upgrade
	env/bin/python3.8 -m pip install wheel
	# ставим зависимости
	env/bin/python3.8 -m pip install -r requirements.txt


postgres:
	docker stop postgres-dev || true
	docker run --rm --detach --name=postgres-dev\
		--env POSTGRES_USER=admin \
		--env POSTGRES_PASSWORD=admin \
		--env POSTGRES_DB=simalend \
		--publish 5442:5432 postgres

migrate:
	alembic upgrade head

sdist: clean
	python3 setup.py sdist

compose-dev:
	sudo docker-compose -f docker-compose-dev.yaml up --build

compose:
	sudo docker-compose up --build -d

cleandb: clean
	sudo rm -rf pg_data

docker: sdist
	docker build -t $(PROJECT_NAME):$(VERSION) .

upload: docker
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):$(VERSION)
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):latest
	docker push $(REGISTRY_IMAGE):$(VERSION)
	docker push $(REGISTRY_IMAGE):latest
