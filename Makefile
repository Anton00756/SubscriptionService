IMAGE_LIST = ssta_service autotests

shared = true
image = ssta_service

build:
	@docker build -t ssta/$(image)_image:latest -f docker/$(image)/Dockerfile .

full_build:
	@$(foreach image_name, $(IMAGE_LIST), \
		docker build -t ssta/$(image_name)_image:latest -f docker/$(image_name)/Dockerfile .;)

up: down
    ifeq ($(shared), true)
		@docker-compose --env-file .env -f=docker/docker-compose-shared.yaml -p ssta up -d
    else
		@docker-compose --env-file .env -f=docker/docker-compose.yaml -p ssta up -d
    endif

down:
	@docker-compose -p ssta down -v