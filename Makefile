up:
	docker compose up --build
down:
	docker compose down -v
bash:
	docker compose exec api bash
test:
	pytest -q
