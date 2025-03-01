# Variables for flexibility
DOCKER_COMPOSE_FILE=docker/docker-compose.yml
DOCKERFILE=docker/Dockerfile
IMAGE_NAME=adapp
POSTGRES_CONTAINER=postgres17
POSTGRES_USER=postgres
POSTGRES_PASSWORD=mysecretpassword
PGDATA=/var/lib/postgresql/data/pgdata
MINIO_CONTAINER=minio
REDIS_CONTAINER=redis

.PHONY: build run stop dev_services_run dev_services_start dev_services_stop dev_services_remove logs 

build:
	docker build --file $(DOCKERFILE) --tag $(IMAGE_NAME) .

run:
	docker-compose --file $(DOCKER_COMPOSE_FILE) up -d

stop:
	docker-compose --file $(DOCKER_COMPOSE_FILE) down --volumes

dev_services_run:
	docker run -d --restart unless-stopped \
	    --name $(POSTGRES_CONTAINER) \
		-p 5432:5432 \
		-e POSTGRES_USER=$(POSTGRES_USER) \
		-e POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
		-e PGDATA=$(PGDATA) \
		postgres:latest

	docker run -d \
		--restart unless-stopped --name $(MINIO_CONTAINER) \
		-p 9000:9000 -p 9001:9001 \
		quay.io/minio/minio:RELEASE.2025-02-18T16-25-55Z-cpuv1 \
		server /data --console-address ":9001"

	docker run -d \
		--restart unless-stopped --name $(REDIS_CONTAINER) \
		-p 6379:6379 \
		--restart unless-stopped \
		redis:7.4.2 

dev_services_start:
	docker start $(POSTGRES_CONTAINER) $(MINIO_CONTAINER) $(REDIS_CONTAINER)

dev_services_stop:
	docker stop $(POSTGRES_CONTAINER)
	docker stop $(MINIO_CONTAINER)
	docker stop $(REDIS_CONTAINER)
dev_services_remove:
	docker rm -f $(POSTGRES_CONTAINER) 
	docker rm -f $(MINIO_CONTAINER)
	docker rm -f $(REDIS_CONTAINER)
logs:
	docker-compose --file $(DOCKER_COMPOSE_FILE) logs -f

