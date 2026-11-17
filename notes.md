## notes

That's done in the docker run command line, not the Dockerfile.

- docker build -t crossword-helper .
  This names the image crossword-helper.
- docker run --name crossword-helper -p 8080:8080 crossword-helper
  This names the container crossword-helper (the --name flag).

The Dockerfile only defines how the image is built — it has no way to assign a name to a running container.

So the full flow would be:

docker build -t crossword-helper .
docker run --name crossword-helper -p 8080:8080 crossword-helper

Or if you want it to auto-remove when stopped:

docker run --rm --name crossword-helper -p 8080:8080 crossword-helper
