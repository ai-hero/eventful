TAG ?= latest

build:
	docker build . -t eventful:latest

run: build
	docker network create ai-hero-internal || true
	docker-compose up --remove-orphans

push: build
	docker tag eventful:latest 635605213996.dkr.ecr.us-east-1.amazonaws.com/eventful:$(TAG)
	docker push 635605213996.dkr.ecr.us-east-1.amazonaws.com/eventful:$(TAG)
