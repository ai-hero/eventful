TAG ?= latest

build:
	docker build . -t eventful:latest

push:
	docker tag eventful:latest 635605213996.dkr.ecr.us-east-2.amazonaws.com/eventful:$(TAG)
	docker push 635605213996.dkr.ecr.us-east-2.amazonaws.com/eventful:$(TAG)
