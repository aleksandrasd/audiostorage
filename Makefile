build:
	docker build -f docker/Dockerfile -t adapp .
run:
	docker-compose --file docker/docker-compose.yml up
run_wsl:
	docker-compose.exe --file docker/docker-compose.yml up
stop:
	docker-compose  --file docker/docker-compose.yml down --volumes
