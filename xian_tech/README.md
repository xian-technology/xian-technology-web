# xian_tech

## Purpose

This package is the Reflex application behind the public Xian Technology
website: page definitions, shared components, site state, and the contact /
roadmap integrations.

## Contents

- `xian_tech.py` — app assembly and routing.
- `pages/` — one module per public page (home, about, developers, contact,
  faq, and the stack-explainer pages such as abci, consensus, contracting,
  api).
- `components/common.py` — shared layout and UI building blocks.
- `state/` — Reflex state classes for interactive parts of the site.
- `fizzy_api.py` — Fizzy roadmap client behind the public roadmap view.
- `contact_email.py` — SMTP contact-form delivery.
- `data.py`, `search.py`, `theme.py` — page content data, site search, and
  theming.

## Notes

- This is the brand site; developer documentation belongs in
  `xian-docs-web`, not in these pages.
- The app runs with SSR disabled (see the root README); OG meta tags are
  injected by the reverse proxy.

## Next

- Start with `xian_tech.py`, then the page you care about under `pages/`.
