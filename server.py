import http.server
import json
import os
import urllib.parse

PORT = 8000
# Get the directory where the script itself is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Construct the path to DOCS_DIR relative to the script's location and normalize it
DOCS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, os.getenv('DOCS_DIR', '../documents/gemini/documents')))

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/files':
            try:
                files = []
                for root, _, filenames in os.walk(DOCS_DIR):
                    for filename in filenames:
                        if filename.endswith('.md'):
                            # Create a relative path from DOCS_DIR
                            relative_path = os.path.relpath(os.path.join(root, filename), DOCS_DIR)
                            # On Windows, relpath can use backslashes. Ensure forward slashes for URLs.
                            files.append(relative_path.replace("\\", "/"))
                
                files.sort()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(files).encode())
            except Exception as e:
                self.send_error(500, str(e))
        elif self.path.startswith('/api/content/'):
            try:
                filename = urllib.parse.unquote(self.path[len('/api/content/'):])
                filepath = os.path.join(DOCS_DIR, filename)
                # Security check to prevent path traversal
                if not os.path.abspath(filepath).startswith(os.path.abspath(DOCS_DIR)):
                    self.send_error(403, "Forbidden")
                    return
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/markdown')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_error(404, str(e))
        else:
            return super().do_GET()

if __name__ == '__main__':
    print(f"Server started at http://localhost:{PORT}")
    http.server.test(HandlerClass=MyHandler, port=PORT)
