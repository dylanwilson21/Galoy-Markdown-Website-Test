#!/usr/bin/env python3
"""
Simple static file server for the Galoy Jekyll website
"""
import os
import mimetypes
from flask import Flask, send_from_directory, abort
from pathlib import Path

app = Flask(__name__)

# Set the directory where Jekyll files are located
JEKYLL_DIR = Path(__file__).parent / "bitdev-el-salvador.github.io"

@app.route('/')
def index():
    """Serve the index.html file"""
    return send_from_directory(JEKYLL_DIR, 'index.html')

@app.route('/<path:filename>')
def serve_file(filename):
    """Serve static files"""
    try:
        # Handle common Jekyll URLs
        if filename.endswith('/') or '.' not in filename:
            # Try to serve as .html first
            html_path = JEKYLL_DIR / f"{filename.rstrip('/')}.html"
            if html_path.exists():
                return send_from_directory(JEKYLL_DIR, f"{filename.rstrip('/')}.html")
            
            # Try markdown files converted to HTML paths
            md_files = {
                'about': 'about.md',
                'products': 'products.md', 
                'faq': 'faq.md'
            }
            
            if filename.rstrip('/') in md_files:
                # For development, we'll serve a simple HTML version
                md_file = JEKYLL_DIR / md_files[filename.rstrip('/')]
                if md_file.exists():
                    with open(md_file, 'r') as f:
                        content = f.read()
                    
                    # Basic markdown to HTML conversion for demo
                    html_content = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Galoy - {filename.title()}</title>
                        <meta name="viewport" content="width=device-width, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
                        <link rel="icon" href="/favicon.ico" type="image/x-icon" />
                        <link rel="stylesheet" href="/assets/css/style.css">
                        <link href="https://fonts.googleapis.com/css?family=Source+Code+Pro" rel="stylesheet">
                    </head>
                    <body>
                        <div class="Site">
                            <header class="Header">
                                <div class="Header-inner">
                                    <div class="Header-logo">
                                        <a href="/">Galoy</a>
                                    </div>
                                    <nav class="Header-nav">
                                        <a href="/about">About Us</a>
                                        <a href="/products">Products</a>
                                        <a href="/faq">FAQ</a>
                                    </nav>
                                </div>
                                <div class="Header-border">
                                    ==============================================================================================================================================================
                                </div>
                            </header>
                            
                            <div class="content">
                                <pre style="white-space: pre-wrap; font-family: 'Source Code Pro', monospace; line-height: 1.6;">{content}</pre>
                            </div>
                            
                            <footer class="Footer">
                                <div class="Footer-border">
                                    ==============================================================================================================================================================
                                </div>
                                <div class="Footer-inner">
                                    <div class="Footer-source">
                                        <a href="https://github.com/GaloyMoney" target="_blank" rel="noopener nofollow">Source available on Github</a>
                                    </div>
                                    <div class="Footer-contact">
                                        <a href="mailto:hello@galoy.io">Contact Us</a>
                                    </div>
                                </div>
                            </footer>
                        </div>
                    </body>
                    </html>
                    """
                    return html_content
        
        # Serve regular files
        return send_from_directory(JEKYLL_DIR, filename)
        
    except Exception:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)