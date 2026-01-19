.PHONY: up down logs migrate seed smoke

up:
	docker compose up -d --build

down:
	docker compose down -v

logs:
	docker compose logs -f --tail=200

migrate:
	python infra/db/migrate.py

seed:
	python infra/db/seed.py

smoke:
	python evals/smoke/smoke_test.py
