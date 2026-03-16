PHONY: dev deploy collectstatic

dev:
	echo "http://localhost:8080"
	uv run manage.py runserver

deploy:
	git push dokku main

collectstatic:
	uv run manage.py collectstatic
