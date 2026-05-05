# Repository Guidelines

## Project Structure & Module Organization
- `xian_tech/xian_tech.py` is the app entrypoint and route registry.
- `xian_tech/pages/` contains route modules; each page should expose a `*_page` factory.
- `xian_tech/components/` holds reusable UI building blocks (shared layout, sections, helpers).
- `xian_tech/state/` contains state logic split by feature (`app.py`, `samples.py`, `tooling.py`).
- `xian_tech/data.py` stores static content, nav metadata, and search data.
- `assets/` serves static files (`assets/css/site.css`, `assets/js/command-palette.js`, images, flow diagrams).
- Root config lives in `pyproject.toml`, `rxconfig.py`, and `README.md`.

## Build, Test, and Development Commands
Use uv for all Python commands:

```bash
uv sync
uv run reflex run
uv run reflex run --env dev
uv run reflex run --env prod --single-port --frontend-port 8001 --backend-port 8001
uv run reflex export --frontend-only
uv run python -m compileall xian_tech
uv run pytest
```

- `reflex run` starts local development.
- `--env dev` uses Vite-style frontend development flow.
- `export --frontend-only` builds static assets and helps debug frontend build issues.

## Coding Style & Naming Conventions
- Target Python 3.14 with 4-space indentation and PEP 8 style.
- Use `snake_case` for modules/functions, `PascalCase` for classes, and descriptive route/page names.
- Keep shared UI in `xian_tech/components/` instead of duplicating page markup.
- Keep content/config data centralized in `xian_tech/data.py` when practical.

## Testing Guidelines
- Place tests under `tests/` using `test_*.py` naming.
- Add focused tests for state logic and API helpers (`fizzy_api.py`, `contact_email.py`).
- Before opening a PR, run syntax and tests, then smoke-test key pages (`/`, `/roadmap`, `/contact`).

## Commit & Pull Request Guidelines
- Recent history favors short, imperative subjects; optional conventional prefixes are used (example: `fix: add Message-ID header to contact form emails`).
- Keep commits scoped to one change and explain non-obvious behavior in the body.
- PRs should include: purpose, affected routes/modules, config/env changes, and screenshots for UI updates.
- Link the related issue/task when available and list local verification commands run.

## Security & Configuration Tips
- Never commit `.env` or credentials (`FIZZY_TOKEN`, SMTP secrets).
- Validate fallback behavior when optional environment variables are missing.

## NO GAMBIARRA POLICY - ASK FOR FEEDBACK INSTEAD
Due to the difficulty of implementing this codebase, we must strive to keep the code high quality, clean, modular, simple and functional - more like an Agda codebase, less like a C codebase. Gambiarras, hacks and duct taping must be COMPLETELY AVOIDED, in favor of robust, simple and general solutions.

In some cases, you will be asked to perform a seemingly impossible task, either because it is (and the user is unaware), or because you don't grasp how to do it properly. In these cases, DO NOT ATTEMPT TO IMPLEMENT A HALF-BAKED SOLUTION JUST TO SATISFY THE USER'S REQUEST. If the task seems too hard, be honest that you couldn't solve it in the proper way, leave the code unchanged, explain the situation to the user and ask for further feedback and clarifications.

The user is a domain expert that will be able to assist you in these cases.
