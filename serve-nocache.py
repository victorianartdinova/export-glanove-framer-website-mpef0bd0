#!/usr/bin/env python3
import http.server, socketserver, os, sys
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 3343
DIR = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.abspath(__file__))
os.chdir(DIR)
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(('', PORT), H) as httpd:
    print(f'no-cache server on :{PORT} → {DIR}')
    httpd.serve_forever()
