
build:
	docker build . -t diffractive/newstream:latest

clean:
	find . -name '*.pyc' -delete

run:
	docker-compose up
