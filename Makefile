NAME=crossword-helper

default: run

build: 
	docker build -t crossword-helper .

run:
	docker run -d --rm --name ${NAME} -p 8080:8080 crossword-helper

stop:
	docker stop ${NAME}

ps:
	docker ps

shell:
	docker container exec --interactive --tty ${NAME} sh

lsall:
	docker container ls -a

ls:
	docker container ls

prune:
	docker system prune -f

