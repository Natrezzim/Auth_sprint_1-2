.DEFAULT_GOAL := help
DOCKER_TESTS = src/tests/functional/docker-compose-tests.yml
DOCKER_PROD = docker-compose.yml
#####---PROD---#####
help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---PROD---#####" (build, up, build_up, start, down, destroy, stop, restart, first_start, test_build))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---TESTS---#####" (test_build, test_up, test_build_up, test_start, test_down, test_destroy, test_stop, test_restart))
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
first_start: build_up
	docker-compose exec service sh /usr/src/app/first_start.sh
	docker-compose exec esloader sh /usr/src/create_elastic_schema.sh

#####---TESTS---#####
test_build:
	docker-compose -f ${DOCKER_TESTS} build
test_up:
	docker-compose -f ${DOCKER_TESTS} up -d
test_build_up: test_build test_up
test_start:
	docker-compose -f ${DOCKER_TESTS} start
test_down:
	docker-compose -f ${DOCKER_TESTS} down
test_destroy:
	docker-compose -f ${DOCKER_TESTS} down -v
	docker volume ls -f dangling=true
	docker volume prune --force
	docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)
test_stop:
	docker-compose -f ${DOCKER_TESTS} stop
test_restart:
	docker-compose -f ${DOCKER_TESTS} stop
	docker-compose -f ${DOCKER_TESTS} up -d