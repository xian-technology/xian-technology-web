# Xian Technology Website

The Xian Technology website is a Reflex app that ships the public site, content
for the Xian stack, and the Fizzy-backed roadmap view.

## Prerequisites

- Python 3.11 (required by `pyproject.toml`).
- Poetry for dependency management.
- Node.js >= 18 or Bun >= 1.1 (Reflex builds the frontend with whichever runtime is on your `PATH`).
- A compiler toolchain for any transitive dependencies (for example `make`, `gcc`, `pkg-config`).

## Configuration

Runtime settings live in `rxconfig.py`:

```python
import os
import reflex as rx

# Disable SSR/prerendered HTML to avoid hydration mismatches behind the proxy.
os.environ.setdefault("REFLEX_SSR", "0")

config = rx.Config(
    app_name="xian_tech",
    deploy_url="https://xian.technology",
    api_url="https://xian.technology",
    frontend_port=3000,
    backend_port=8000,
    show_built_with_reflex=False,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
```

- `REFLEX_SSR=0` disables server-side rendering to prevent hydration mismatches
  behind the reverse proxy. OG/Twitter meta tags are injected via Nginx instead
  (see [Social preview](#social-preview-og--twitter-meta-tags)).
- `deploy_url` / `api_url` should match the public-facing domain.
- Ports can be overridden via CLI arguments (see Running the app).

### Environment variables

Local development loads `.env` from the project root (`dotenv` is imported in
`xian_tech/state.py`). These settings are only needed if you want the roadmap
board to load live data.

```bash
FIZZY_TOKEN=your_read_only_token
FIZZY_ACCOUNT_SLUG=1
FIZZY_BOARD_ID=03fiomkit5oknquymk0ooi26m
FIZZY_BASE_URL=https://tasks.xian.technology
FIZZY_EXCLUDE_TAGS=internal,experimental
CONTACT_EMAIL_TO=info@xian.technology
CONTACT_EMAIL_FROM=no-reply@xian.technology
SMTP_HOST=mail.example.com
SMTP_PORT=587
SMTP_USERNAME=mailer@example.com
SMTP_PASSWORD=super-secret-password
SMTP_USE_TLS=true
SMTP_USE_SSL=false
CONTACT_SUBMISSION_COOLDOWN_SECONDS=30
```

- `FIZZY_TOKEN` is required to call the Fizzy API.
- `FIZZY_ACCOUNT_SLUG` defaults to `1`.
- `FIZZY_BOARD_ID` defaults to `03fiomkit5oknquymk0ooi26m`.
- `FIZZY_BASE_URL` defaults to `https://tasks.xian.technology`.
- `FIZZY_EXCLUDE_TAGS` is a comma-separated list of tags to hide from the roadmap (case-insensitive).
- `CONTACT_EMAIL_TO` sets the recipient for contact form submissions (defaults to `info@xian.technology`).
- `CONTACT_EMAIL_FROM` sets the From address for outgoing contact mail (defaults to `SMTP_USERNAME` or the recipient).
- `SMTP_HOST` is required to send contact form email.
- `SMTP_PORT` defaults to `587`.
- `SMTP_USERNAME`/`SMTP_PASSWORD` authenticate with your SMTP server (password required if username is set).
- `SMTP_USE_TLS` enables STARTTLS (defaults to `true`).
- `SMTP_USE_SSL` enables SMTPS (defaults to `false`).
- `CONTACT_SUBMISSION_COOLDOWN_SECONDS` throttles per-session sends (defaults to `30`).

## Installation

```bash
poetry install
```

## Running the app

### Local development

```bash
poetry run reflex run
```

The terminal prints the URLs it binds to (typically `http://localhost:3000`).

### Production (single-port recommended)

```bash
poetry run reflex run --env prod --single-port --frontend-port 8001 --backend-port 8001
```

- A single Granian process serves both the static bundle and websocket/events on port 8001.
- Keep this process alive with your preferred supervisor (see systemd below).

### Production (split ports)

```bash
poetry run reflex run --env prod
```

- Frontend listens on 3000, backend on 8000.
- Use the split-port Nginx config below so `/` goes to 3000 and only backend
  endpoints hit 8000.

### Development mode

```bash
poetry run reflex run --env dev
```

This launches the Vite dev server with hot reload on whatever open ports Reflex
negotiates.

## Static export

For a frontend-only build:

```bash
poetry run reflex export --frontend-only
```

Reflex prints the output directory during export. Deploy the generated bundle to
your static hosting of choice.

## Reverse proxy / deployment notes

- For single-port deployments, forward every path (including `/_event`) to the chosen backend port and enable websocket headers.
- For split-port deployments, send `/` to port 3000 and proxy only backend endpoints to port 8000 with `proxy_http_version 1.1`, `Upgrade`, and `Connection "upgrade"`.
- If you enforce a CSP, be ready to include `unsafe-eval` in `script-src` if Reflex hydration fails (some components rely on `new Function`).

### Social preview (OG / Twitter meta tags)

Because the app runs in SPA mode (`REFLEX_SSR=0`), the initial HTML shell
contains no `<meta>` tags beyond charset and viewport. Crawlers (Telegram,
Twitter, Facebook, etc.) don't execute JavaScript, so they never see the tags
Reflex injects client-side.

The fix is to use Nginx's `sub_filter` module (`--with-http_sub_module`, included
in the default Ubuntu/Debian package) to inject the OG and Twitter meta tags
into `</head>` before the response reaches the client. See the config examples
below — the `sub_filter` block handles this transparently.

If you change the preview copy or image, update both `xian_tech/data.py` **and**
the corresponding `sub_filter` block in the Nginx config.

### Example Nginx config (single-port mode)

```nginx
server {
    server_name xian.technology;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Inject OG / Twitter meta tags into the SPA shell so crawlers
        # (Telegram, Twitter, Facebook, etc.) can build link previews
        # without executing JavaScript.
        sub_filter '</head>' '
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="Xian Technology"/>
<meta property="og:url" content="https://xian.technology"/>
<meta property="og:title" content="Python-Native Contracting on a CometBFT Backbone"/>
<meta property="og:description" content="Xian is a CometBFT-backed blockchain with a pure Python contracting engine. Write native Python contracts without transpilers."/>
<meta property="og:image" content="https://xian.technology/social-preview.png"/>
<meta property="og:image:secure_url" content="https://xian.technology/social-preview.png"/>
<meta property="og:image:type" content="image/png"/>
<meta property="og:image:width" content="1200"/>
<meta property="og:image:height" content="630"/>
<meta property="og:image:alt" content="Python-Native Contracting on a CometBFT Backbone"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="Python-Native Contracting on a CometBFT Backbone"/>
<meta name="twitter:description" content="Xian is a CometBFT-backed blockchain with a pure Python contracting engine. Write native Python contracts without transpilers."/>
<meta name="twitter:image" content="https://xian.technology/social-preview.png"/>
<meta name="twitter:image:alt" content="Python-Native Contracting on a CometBFT Backbone"/>
<meta name="twitter:site" content="@xian_technology"/>
<meta name="description" content="Xian is a CometBFT-backed blockchain with a pure Python contracting engine. Write native Python contracts without transpilers."/>
</head>';
        sub_filter_once on;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/xian.technology/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xian.technology/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = xian.technology) {
        return 301 https://$host$request_uri;
    }
    listen 80;
    server_name xian.technology;
    return 404;
}
```

Reload Nginx after editing: `sudo nginx -s reload`.

### Example Nginx config (split ports)

Use this when running `poetry run reflex run --env prod` without `--single-port`.

```nginx
server {
    server_name xian.technology;

    location ~ ^/(ping|_upload|_health|_all_routes|auth-codespace)$ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /_event {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    listen 443 ssl;
    ssl_certificate /etc/letsencrypt/live/xian.technology/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xian.technology/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
}

server {
    if ($host = xian.technology) {
        return 301 https://$host$request_uri;
    }
    listen 80;
    server_name xian.technology;
    return 404;
}
```

### systemd unit

To keep the site running after boot, install a service such as
`/etc/systemd/system/xian-tech.service`:

```ini
[Unit]
Description=Xian Technology Website
After=network.target

[Service]
Type=simple
User=endogen
WorkingDirectory=/home/endogen/xian-tech
Environment="PATH=/home/endogen/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/home/endogen/.cache/pypoetry/virtualenvs/xian-tech--py3.11/bin"
ExecStart=/home/endogen/.local/bin/poetry run reflex run --env prod --single-port --frontend-port 8001 --backend-port 8001
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now xian-tech
```

Use `journalctl -u xian-tech -f` to follow logs.
Adjust `User`, `WorkingDirectory`, `PATH`, and ports to match your host.

## Project structure

- `xian_tech/xian_tech.py`: App entry, page wiring, head assets.
- `xian_tech/pages/`: Page factories (`*_page`).
- `xian_tech/components/`: Reusable UI primitives.
- `xian_tech/theme.py`: Design tokens.
- `xian_tech/state.py`: Global interactions and computed data.
- `xian_tech/data.py`: Static copy, nav, and search data.
- `assets/`: Images and brand assets (served from `/filename`).

## Testing

- Syntax check: `poetry run python -m compileall xian_tech`
- Tests: `poetry run pytest`

## Troubleshooting

- Missing Fizzy config: the roadmap loader raises `ValueError` if `FIZZY_TOKEN` is unset or if the account/board is missing. Confirm `.env` and reload.
- Frontend build errors: verify Node.js or Bun are installed and run `poetry run reflex export --frontend-only` to surface raw logs in `.web/`.
- Port already in use: stop the existing process or change the `--frontend-port` and `--backend-port` values.

## Notes

- Do not edit generated `.web/` output directly; regenerate via Reflex commands.
- The Roadmap page relies on Fizzy; without `FIZZY_*` env vars it shows a fallback message.

With the prerequisites satisfied and `.env` configured, the site can be started
locally or deployed on a server by running `poetry run reflex run --env prod` and
fronting it with your preferred process manager and reverse proxy.
