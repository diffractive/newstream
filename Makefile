.PHONY: jupyter

build: build-django build-jupyter build-tests

build-django:
	docker build . -t diffractive/newstream:latest

build-jupyter:
	docker build . -t diffractive/newstream-jupyter:latest --target jupyter

build-tests:
	cd selenium-tests && make build

clean:
	find . -name '*.pyc' -delete

run:
	docker-compose -f docker-compose.yml up

run-jupyter:
	docker-compose -f docker-compose.yml up jupyter

run-selenium:
	docker-compose -f docker-compose.yml --profile selenium up

down:
	docker-compose -f docker-compose.yml down --remove-orphans

selenium:
	NOTEBOOK_ROOT=$(cwd)/notebooks jupyter notebook
