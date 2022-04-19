.DEFAULT_GOAL := help
DOCKER_TESTS = src/tests/functional/docker-compose-tests.yml
DOCKER_PROD = docker-compose.yml
#####---PROD---#####
help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---PROD---#####" (build, up, build_up, start, down, destroy, stop, restart, first_start, test_build))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
build:
	docker-compose -f ${DOCKER_PROD} build
up:
	docker-compose -f ${DOCKER_PROD} up -d
build_up: build up
start:
	docker-compose -f ${DOCKER_PROD} start
down:
	docker-compose -f ${DOCKER_PROD} down
destroy:
	docker-compose -f ${DOCKER_PROD} down -v
	docker volume ls -f dangling=true
	docker volume prune --force
	docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)
stop:
	docker-compose -f ${DOCKER_PROD} stop
restart:
	docker-compose -f ${DOCKER_PROD} stop
	docker-compose -f ${DOCKER_PROD} up -d