start:
	docker-compose up

stop:
	docker-compose stop

restart:
	docker-compose stop && sleep 5 && docker-compose up

restart-f:
	docker-compose down && sleep 5 && docker-compose up

ssh-nginx:
	docker exec -it nginx_container bash

ssh-web:
	docker exec -it web_container bash

ssh-db:
	docker exec -it postgres_db_container bash

build-cache:
	docker-compose build

build-no-cache:
	docker-compose build --no-cache --pull

test:
	docker-compose stop web | echo
	docker-compose run web python manage.py test --settings=PulaDemo.settings
	docker-compose stop && docker-compose up