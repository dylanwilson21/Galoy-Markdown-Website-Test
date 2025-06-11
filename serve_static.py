#!/usr/bin/env python3
"""
Simple static file server for the Jekyll site
"""
import os
import http.server
import socketserver
from pathlib import Path

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / "bitdev-el-salvador.github.io"), **kwargs)
    
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHTTPRequestHandler) as httpd:
        print(f"Serving Jekyll site at http://0.0.0.0:{PORT}")
        print("Site directory: bitdev-el-salvador.github.io")
        httpd.serve_forever()