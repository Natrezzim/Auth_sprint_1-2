.DEFAULT_GOAL := help
DOCKER_TESTS = async_api/src/tests/functional/docker-compose-tests.yml
DOCKER_PROD = async_api/docker-compose.yml
DOCKER_AUTH = auth_api/docker-compose.yml
#####---PROD---#####
help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---PROD---#####" (build, up, build_up, start, down, destroy, stop, restart, first_start, test_build))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---TESTS---#####" (test_build, test_up, test_build_up, test_start, test_down, test_destroy, test_stop, test_restart))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
async_api_build:
	docker-compose -f ${DOCKER_PROD} build
async_api_up:
	docker-compose -f ${DOCKER_PROD} up -d
async_api_build_up: async_api_build async_api_up
async_api_start:
	docker-compose -f ${DOCKER_PROD} start
async_api_down:
	docker-compose -f ${DOCKER_PROD} down
async_api_destroy:
	docker-compose -f ${DOCKER_PROD} down -v
	docker  volume ls -f dangling=true
	docker volume prune --force
	docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)
async_api_stop:
	docker-compose -f ${DOCKER_PROD} stop
async_api_restart:
	docker-compose -f ${DOCKER_PROD} stop
	docker-compose -f ${DOCKER_PROD} up -d
async_api_first_start: async_api_build_up
	docker-compose -f ${DOCKER_PROD} exec service sh /usr/src/app/first_start.sh
	docker-compose -f ${DOCKER_PROD} exec esloader sh /usr/src/create_elastic_schema.sh

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

#####---AUTH---#####
auth_api_help:
	$(info ------------------------------------------------------------------------------------------------------------------------------)
	$(info "#####---AUTH---#####" (build, up, build_up, start, down, destroy, stop, restart, first_start, test_build))
	$(info ------------------------------------------------------------------------------------------------------------------------------)
auth_api_build:
	docker-compose -f ${DOCKER_AUTH} build
auth_api_up:
	docker-compose -f ${DOCKER_AUTH} up -d
auth_api_build_up: auth_api_build auth_api_up
	docker-compose -f ${DOCKER_AUTH} exec service sh -c "python /usr/src/rest/utils/wait_for_pg.py && python /usr/src/rest/utils/wait_for_redis.py"
auth_api_start:
	docker-compose -f ${DOCKER_AUTH} start
auth_api_down:
	docker-compose -f ${DOCKER_AUTH} down
auth_api_destroy:
	docker-compose -f ${DOCKER_AUTH} down -v
	docker volume ls -f dangling=true
	docker volume prune --force
	docker rmi $(shell docker images --filter "dangling=true" -q --no-trunc)
auth_api_stop:
	docker-compose -f ${DOCKER_AUTH} stop
auth_api_restart:
	docker-compose -f ${DOCKER_AUTH} stop
	docker-compose -f ${DOCKER_AUTH} up -d
auth_api_first_start: auth_api_build_up
	docker-compose -f ${DOCKER_AUTH} exec service sh -c "python -m flask db upgrade  && sleep 5"


#####---FIRST_START_ALL---#####
first_start_all: auth_api_first_start async_api_first_start
destroy_all: auth_api_destroy async_api_destroy auth_api_destroy async_api_destroy