default: run

build: 
	docker build -t crossword-helper .

run:
	docker run -d -p 8080:8080 crossword-helper

stop:
	docker stop nifty_wu

ps:
	docker ps

shell:
	docker container exec --interactive --tty nifty_wu sh

lsall:
	docker container ls -a

ls:
	docker container ls

prune:
	docker system prune -f

