#!/usr/bin/env python3
import http.server
import socketserver
import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

PORT = 8888

with open("dictionary", "r") as f:
    WORDS = [line.strip().lower() for line in f if line.strip()]


def find_matches(pattern):
    regex = re.compile(f"^{pattern.replace('_', '.')}$")
    return [w for w in WORDS if regex.match(w)]


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Crossword Helper</title>
  <style>
    * { box-sizing: border-box; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      max-width: 800px;
      margin: 0 auto;
      padding: 2rem;
      background: #f5f5f5;
    }
    h1 { text-align: center; color: #333; }
    .input-section { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
    input {
      flex: 1;
      padding: 0.75rem;
      font-size: 1.25rem;
      font-family: monospace;
      border: 2px solid #ddd;
      border-radius: 4px;
      text-transform: lowercase;
    }
    input:focus { outline: none; border-color: #007bff; }
    button {
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
    button:hover { background: #0056b3; }
    .results {
      background: white;
      border-radius: 4px;
      padding: 1rem;
      min-height: 200px;
    }
    .results-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1rem;
      padding-bottom: 0.5rem;
      border-bottom: 1px solid #eee;
    }
    .count { color: #666; font-size: 0.9rem; }
    .word-list { display: flex; flex-wrap: wrap; gap: 0.5rem; }
    .word {
      background: #e9ecef;
      padding: 0.25rem 0.5rem;
      border-radius: 3px;
      font-family: monospace;
      font-size: 1rem;
    }
    .instructions {
      color: #666;
      font-size: 0.9rem;
      margin-bottom: 1.5rem;
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>Crossword Helper</h1>
  <p class="instructions">Enter a word pattern using "." or "_" for unknown letters</p>
  <div class="input-section">
    <input type="text" id="pattern" placeholder="e.g., c...w.rd" autofocus>
    <button onclick="search()">Search</button>
  </div>
  <div class="results">
    <div class="results-header">
      <strong>Matches</strong>
      <span class="count" id="count"></span>
    </div>
    <div class="word-list" id="results"></div>
  </div>
  <script>
    const patternInput = document.getElementById('pattern');
    const resultsDiv = document.getElementById('results');
    const countSpan = document.getElementById('count');
    patternInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') search(); });
    async function search() {
      const pattern = patternInput.value.trim();
      if (!pattern) return;
      const res = await fetch('/api/search?pattern=' + encodeURIComponent(pattern));
      const words = await res.json();
      countSpan.textContent = words.length + ' words found';
      resultsDiv.innerHTML = words.length 
        ? words.map(w => '<span class="word">' + w + '</span>').join('')
        : '<em>No matches found</em>';
    }
  </script>
</body>
</html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/search":
            params = parse_qs(parsed.query)
            pattern = params.get("pattern", [""])[0].lower()
            matches = find_matches(pattern) if pattern else []
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(matches).encode())
        else:
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

    def log_message(self, format, *args):
        print(
            f"{self.address_string()} - [{self.log_date_time_string()}] {format % args}"
        )


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Crossword helper running at http://localhost:{PORT}")
    httpd.serve_forever()
