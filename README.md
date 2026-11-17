# Crossword Helper

A lightweight web app that helps you find words matching a crossword puzzle pattern. Use `.` or `_` for unknown letters.

**Example:** enter `c...w.rd` to find `crossword`.

Built with **Flask** and packaged as a **Docker** image.

---

## Quick Start (Docker)

### Option 1: Run the pre-built image

No build needed — just pull and run:

```bash
# Run in foreground (see logs in terminal)
docker run -p 8080:8080 ghcr.io/rabkazoo/crossword-helper:main

# Or run detached in the background
docker run -d -p 8080:8080 ghcr.io/rabkazoo/crossword-helper:main
```

Then open [http://localhost:8080](http://localhost:8080).

> **Detached mode (`-d`)** is useful if you want the container to keep running after you close your terminal. Without it, the container stops when you press `Ctrl+C`.

### Option 2: Build and run locally

```bash
# Clone the repo
git clone https://github.com/rabkazoo/crossword-helper.git
cd crossword-helper

# Build and run with Docker Compose
docker compose up --build

# Or run in the background
docker compose up -d --build
```

### Option 3: Build the image yourself

```bash
docker build -t crossword-helper .
docker run -p 8080:8080 crossword-helper
```

---

## Development (without Docker)

Requires Python 3.10+.

```bash
pip install -r requirements.txt
python app.py
```

The app will be available at [http://localhost:8080](http://localhost:8080).

---

## API

The search endpoint accepts a `pattern` query parameter:

```bash
curl "http://localhost:8080/api/search?pattern=c...w.rd"
# → ["crossword"]
```

Use `.` or `_` as wildcards for unknown letters.

---

## Dictionary

The app ships with a built-in English word list (`dictionary`). Words are matched case-insensitively.

---

## License

[MIT](LICENSE)
