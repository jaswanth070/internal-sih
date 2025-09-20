# internal-sih (COA Django Starter)

This repository contains a Django project scaffold for a Railway Controller Operations Assistant (COA) UI with JWT authentication (SimpleJWT) and a basic session-based login screen protected by a simple arithmetic captcha.

## Features
- Django 4.x project with custom `accounts.User` model
- JWT auth endpoints via `djangorestframework-simplejwt`
- Session login page with captcha, issues JWT cookies on success
- Minimal dashboard view, logout, and styled UI

## Quickstart
1. Clone and set up environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   ```
2. Generate a secret key and configure `.env`:
   ```bash
   python - << 'PY'
import secrets
print(secrets.token_urlsafe(50))
PY
   ```
   Set `DJANGO_SECRET_KEY` in `.env`.
3. Run migrations and create a superuser:
   ```bash
   python manage.py makemigrations accounts
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Start the server:
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000 to view the login screen.

## JWT Endpoints
- `POST /api/token/` — obtain access/refresh
- `POST /api/token/refresh/` — refresh access

## Notes
- Cookies are set with `secure=False` for local dev. Switch to `True` on HTTPS.
- Consider adding CSRF and HTTPS settings for production.
- This starter does not include frontend build tooling.

## License
MIT
