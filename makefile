build: 
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ build

run:
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ run --rm -it -p 8000:8000 api
	
run-test: 
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ run --rm -it -p 8000:8000 api pytest -vv .

run-test-cov:
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ run --rm -it -p 8000:8000 api pytest -vv . --cov=yummy_pizza

up: 
	docker compose -f ./deploy/docker-compose.yml --project-directory ./ up
