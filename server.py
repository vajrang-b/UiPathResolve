#!/usr/bin/env python3
"""
Local development server for UiPathResolve Restaurant site.
Automatically attaches required voice calling response headers:
- Permissions-Policy: microphone=(self)
- Content-Security-Policy: connect-src ...; media-src blob:; worker-src blob:;
Supports lightweight Jekyll template rendering for local preview without Ruby/Jekyll installed.
"""

import os
import re
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = int(os.environ.get("PORT", 8080))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CSP_HEADER = (
    "connect-src 'self' wss://voice.uni-stg-svc-eus-01-g.kstg.kubefabric.uipath.systems "
    "https://voice.uni-stg-svc-eus-01-g.kstg.kubefabric.uipath.systems "
    "https://staging.uipath.com wss://staging.uipath.com; "
    "media-src 'self' blob:; "
    "worker-src 'self' blob:;"
)
PERMISSIONS_POLICY_HEADER = "microphone=(self)"


def load_file(rel_path):
    p = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def render_jekyll_page(content, page_title="Savoria Trattoria"):
    # Strip front matter
    front_matter = {}
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            content = parts[2]
            for line in fm_text.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    front_matter[k.strip()] = v.strip()

    layout = load_file("_layouts/default.html")
    if not layout:
        return content

    head = load_file("_includes/head.html")
    navbar = load_file("_includes/navbar.html")
    footer = load_file("_includes/footer.html")
    widget = load_file("_includes/widget.html")

    # Replace includes
    layout = layout.replace("{% include head.html %}", head)
    layout = layout.replace("{% include navbar.html %}", navbar)
    layout = layout.replace("{% include footer.html %}", footer)

    if front_matter.get("has_inline_widget") == "true":
        # Don't add duplicate widget if page already has inline widget
        layout = re.sub(r"\{% unless page\.has_inline_widget %\}.*?\{% endunless %\}", "", layout, flags=re.DOTALL)
    else:
        layout = re.sub(r"\{% unless page\.has_inline_widget %\}(.*?)\{% endunless %\}", widget, layout, flags=re.DOTALL)

    layout = layout.replace("{{ content }}", content)

    # Simple variable replacements
    site_title = "Golden Bites - Fast Food & Drive-Thru"
    site_desc = "Simple McDonald's style fast-food menu with voice drive-thru ordering."
    title = front_matter.get("title", page_title)

    layout = re.sub(r"\{% if page\.title %\}.*?\{% endif %\}", title + " | ", layout)
    layout = layout.replace("{{ site.title }}", site_title)
    layout = layout.replace("{{ page.title }}", title)
    layout = layout.replace("{{ page.description | default: site.description }}", site_desc)
    layout = layout.replace("{{ site.restaurant.name }}", site_title)
    layout = layout.replace("{{ site.restaurant.phone }}", "1-800-555-MACS")
    layout = layout.replace("{{ site.restaurant.email }}", "support@goldenbites.com")
    layout = layout.replace("{{ site.restaurant.address }}", "742 Fast Lane, Drive-Thru Plaza, CA 90210")
    layout = layout.replace("{{ 'now' | date: \"%Y\" }}", "2026")

    # Clean up navigation loops
    nav_links_html = """
      <li class="nav-item"><a href="index.html" class="nav-link">🍔 Full Menu</a></li>
      <li class="nav-item"><a href="deals.html" class="nav-link">🍟 Combos & Deals</a></li>
      <li class="nav-item"><a href="contact.html" class="nav-link">📍 Drive-Thru & Hours</a></li>
    """
    layout = re.sub(r"\{% for item in site\.navigation %\}.*?\{% endfor %\}", nav_links_html, layout, flags=re.DOTALL)
    layout = re.sub(r"\{\{.*?relative_url.*?\}\}", lambda m: m.group(0).split("'")[1].lstrip("/"), layout)

    return layout


class VoiceHeadersHTTPHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Permissions-Policy", PERMISSIONS_POLICY_HEADER)
        self.send_header("Content-Security-Policy", CSP_HEADER)
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()

    def do_GET(self):
        path = self.path.split("?")[0].lstrip("/")
        if not path or path == "":
            path = "index.html"

        target_file = os.path.join(BASE_DIR, path)

        if path.endswith(".html") and os.path.exists(target_file):
            raw = load_file(path)
            rendered = render_jekyll_page(raw, page_title=path.replace(".html", "").title())
            body = rendered.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return

        super().do_GET()


if __name__ == "__main__":
    print(f"🍽️ Starting Savoria Restaurant Server on http://localhost:{PORT}")
    print(f"🔒 Setting Voice Call Response Headers:")
    print(f"   Permissions-Policy: {PERMISSIONS_POLICY_HEADER}")
    print(f"   Content-Security-Policy: {CSP_HEADER}")
    server = HTTPServer(("0.0.0.0", PORT), VoiceHeadersHTTPHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        sys.exit(0)
