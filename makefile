build: 
	docker-compose -f deploy/docker-compose.yml --project-directory . up --build

run:
	docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up
	
test: 
	docker-compose -f deploy/docker-compose.yml --project-directory . run --rm api pytest -vv .
	docker-compose -f deploy/docker-compose.yml --project-directory . down

run-test-cov:
	docker compose -f ./deploy/docker-compose.yml --project-directory . run --rm -it api pytest -vv . --cov=yummy_pizza

up: 
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ up
