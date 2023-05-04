.PHONY: jupyter

build: build-django build-tests

build-django:
	cd django-app && docker build . -t diffractive/newstream:latest

build-tests:
	cd selenium-tests && make build

clean:
	find . -name '*.pyc' -delete

run:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose-dev.yml up

run-selenium:
	docker-compose -f docker/docker-compose.yml -f docker/docker-compose-dev.yml --profile selenium up

down:
	docker-compose -f docker/docker-compose.yml down --remove-orphans

selenium:
	NOTEBOOK_ROOT=$(cwd)/notebooks jupyter notebook
