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
	python3.8 -m venv env
	python3.8 -m pip install pip --upgrade
	python3.8 -m pip install wheel
	# ставим зависимости
	python3.8 -m pip install -r requirements.txt


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

compose:
	docker-compose build
	docker-compose run app sleep 5 && alembic upgrade head
	docker-compose up

cleandb: clean
	sudo rm -rf pg_data

docker: sdist
	docker build -t $(PROJECT_NAME):$(VERSION) .

upload: docker
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):$(VERSION)
	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):latest
	docker push $(REGISTRY_IMAGE):$(VERSION)
	docker push $(REGISTRY_IMAGE):latest
