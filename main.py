#!/usr/bin/env python3
"""
Simple static file server for the Galoy Jekyll website with markdown processing
"""
import os
import mimetypes
import markdown
import frontmatter
from flask import Flask, send_from_directory, abort, render_template_string
from pathlib import Path

app = Flask(__name__)

# Set the directory where Jekyll files are located
JEKYLL_DIR = Path(__file__).parent

@app.route('/')
def index():
    """Serve the index.html file with proper header"""
    try:
        # Read the index.html file
        index_file = JEKYLL_DIR / 'index.html'
        if index_file.exists():
            with open(index_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Get the page title
            page_title = post.metadata.get('title', 'Home')
            
            # Generate the full HTML page with navigation
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{page_title} | Galoy</title>
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
                <div class="Header-nav-container">
                    <nav class="Header-nav">
                        <a href="/about">About Us</a>
                        <a href="/products">Products</a>
                        <a href="/faq">FAQ</a>
                    </nav>
                    <nav class="Header-social">
                        <a href="https://github.com/GaloyMoney" target="_blank" rel="noopener nofollow">GitHub</a>
                        <a href="https://docs.galoy.io" target="_blank" rel="noopener nofollow">Documentation</a>
                        <a href="mailto:hello@galoy.io">Contact</a>
                    </nav>
                </div>
            </div>
            <div class="Header-border">
                ==============================================================================================================================================================
            </div>
        </header>
        
        {post.content}
        
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
</html>"""
            return html_content
        else:
            abort(404)
    except Exception:
        abort(404)

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
                # Process markdown files with proper Jekyll-like rendering
                md_file = JEKYLL_DIR / md_files[filename.rstrip('/')]
                if md_file.exists():
                    # Parse the markdown file with frontmatter
                    with open(md_file, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                    
                    # Convert markdown to HTML
                    md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
                    content_html = md.convert(post.content)
                    
                    # Get the page title
                    page_title = post.metadata.get('title', filename.title())
                    
                    # Generate the full HTML page
                    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{page_title} | Galoy</title>
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
                <div class="Header-nav-container">
                    <nav class="Header-nav">
                        <a href="/about">About Us</a>
                        <a href="/products">Products</a>
                        <a href="/faq">FAQ</a>
                    </nav>
                    <nav class="Header-social">
                        <a href="https://github.com/GaloyMoney" target="_blank" rel="noopener nofollow">GitHub</a>
                        <a href="https://docs.galoy.io" target="_blank" rel="noopener nofollow">Documentation</a>
                        <a href="mailto:hello@galoy.io">Contact</a>
                    </nav>
                </div>
            </div>
            <div class="Header-border">
                ==============================================================================================================================================================
            </div>
        </header>
        
        <div class="content">
            {content_html}
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
</html>"""
                    return html_content
        
        # Serve regular files
        return send_from_directory(JEKYLL_DIR, filename)
        
    except Exception:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)