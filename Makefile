build:
	docker build . -t eventful:latest

run: build
	docker network create ai-hero-internal || true
	docker-compose up --remove-orphans