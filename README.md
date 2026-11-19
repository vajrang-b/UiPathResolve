# 🍷 Savoria Trattoria & Bar — UiPath Resolve Voice AI Restaurant

A modern, multi-page restaurant website built for **Savoria Trattoria & Bar**, integrated with the **UiPath Resolve Conversational Voice AI Concierge** widget for automated 24/7 table reservations, dietary recommendations, and voice calls.

Designed with a **Jekyll theme** for **GitHub Pages** deployment with full responsiveness and microphone permissions support.

---

## 🚀 Live Site & Multi-Page Structure

The site is organized into 5 pages:

| Page | File | Description |
|---|---|---|
| **Home** | [`index.html`](index.html) | Hero banner, Chef's signature selections, voice assistant showcase, diner reviews, and the embedded UiPath Resolve voice widget. |
| **Menu** | [`menu.html`](menu.html) | Interactive categorized dining menu (Antipasti, Primi Pasta, Secondi, Pizza, Dolci, Wine & Cocktails) with real-time category filtering. |
| **Reservations** | [`reservations.html`](reservations.html) | Online table reservation form (guests, date, time, seating zone) with direct voice reservation instructions. |
| **Our Story** | [`about.html`](about.html) | Executive Chef Matteo Moretti's culinary journey, farm-to-table sourcing, and awards. |
| **Contact & Hours** | [`contact.html`](contact.html) | Service hours, directions, parking & valet info, map card, and private events inquiry form. |

---

## 🎙️ UiPath Resolve Voice Calling Integration

### 1. Widget Script in `index.html`
```html
<script src="https://staging.uipath.com/vajrang/DefaultTenant/cx_/widget/v1/loader.js"
  data-agent-id="08aa5a00-ffe1-f111-91f2-7c1e52021864"
  data-api-url="https://staging.uipath.com/vajrang/DefaultTenant/cx_/api"
  data-title="Restaurant"
  data-color="#6366f1"
  data-position="bottom-right"
  data-theme="dark">
</script>
```

### 2. Voice Calling Response Headers
For browsers to allow microphone access and WebRTC voice calls with the UiPath voice backend, the following response headers are required:

```http
Permissions-Policy: microphone=(self)
Content-Security-Policy:
  connect-src 'self' wss://voice.uni-stg-svc-eus-01-g.kstg.kubefabric.uipath.systems https://voice.uni-stg-svc-eus-01-g.kstg.kubefabric.uipath.systems https://staging.uipath.com wss://staging.uipath.com;
  media-src 'self' blob:;
  worker-src 'self' blob:;
```

We provide out-of-the-box configurations for all hosting environments:

- **`<meta http-equiv="Content-Security-Policy">`** in `_includes/head.html` on all pages.
- **`_headers`** file for **Cloudflare Pages** and **Netlify**.
- **`vercel.json`** for **Vercel** serverless hosting.
- **`.htaccess`** for **Apache** web servers.
- **`server.py`** for local testing with Python 3.

### 3. Microphone Permissions for iFrames
A dynamic `MutationObserver` script automatically monitors and applies `allow="microphone"` to any iframe inserted by the UiPath loader/widget runtime:

```javascript
iframe.setAttribute('allow', 'microphone');
```

---

## 🎨 Jekyll Theme Configuration (GitHub Pages)

As documented in [GitHub Pages Jekyll Themes Guide](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll/adding-a-theme-to-your-github-pages-site-using-jekyll), the site utilizes `_config.yml` with the Cayman theme:

```yaml
theme: jekyll-theme-cayman
title: "Savoria Trattoria & Bar"
description: "Authentic Italian Gastronomy & Modern Hospitality"
```

Theme styling is extended via [`assets/css/style.scss`](assets/css/style.scss):
```scss
---
---
@import "{{ site.theme }}";
/* Custom Restaurant Styles */
```

---

## 💻 Running Locally

### Option 1: Python Development Server (with exact voice response headers)
Run the bundled development server:
```bash
python3 server.py
```
Open **[http://localhost:8080](http://localhost:8080)** in your browser.

The server automatically sets `Permissions-Policy: microphone=(self)` and `Content-Security-Policy` headers on every response.

### Option 2: Jekyll / Bundler
If Ruby and Bundler are installed:
```bash
bundle install
bundle exec jekyll serve
```
Open **[http://localhost:4000](http://localhost:4000)**.

---

## 🌐 Deploying to GitHub Pages

1. Push your changes to the `main` branch:
   ```bash
   git add .
   git commit -m "Add multi-page restaurant site with UiPath voice widget and Jekyll theme"
   git push origin main
   ```
2. In your GitHub repository, go to **Settings** > **Pages**.
3. Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
4. Select `main` branch and `/ (root)` folder, then click **Save**.
5. GitHub Actions will build and deploy your Jekyll site automatically!

> **Note on Permissions-Policy on `*.github.io`:** Standard GitHub Pages does not support custom HTTP response headers. For full browser microphone voice calling in production, point a custom domain through **Cloudflare** (which automatically reads `_headers` or uses Transform Rules) or host on **Cloudflare Pages** / **Netlify** / **Vercel** using the included configuration files.
