# Copilot Instructions for NSCPL Django Project

## Project Overview
- This is a Django 5.x web application for NSCPL PRIVATE LIMITED, featuring sports/event management, team/player profiles, news, gallery, and contact forms.
- Major apps: `core`, `events`, `sports`, `teams`, `news`, `gallery`, `contact`, `registration`.
- Static assets are in `static/`, user uploads in `media/`, templates in `templates/`.

## Architecture & Patterns
- Each app follows Django conventions: models, views, admin, urls, migrations.
- Shared context processors in `core/context_processors.py` provide theme/footer data to templates.
- Custom color palettes and CKEditor config are set in `nscpl_project/settings.py`.
- Admin UI is customized via Jazzmin (`JAZZMIN_SETTINGS`, `JAZZMIN_UI_TWEAKS`).
- CKEditor 5 is used for rich text editing; config in `settings.py` under `CKEDITOR_5_CONFIGS`.
- Email/contact forms use environment-based config from `.env` (see `env.example`).

## Developer Workflows
- **Setup**: Use `python -m venv venv` and `pip install -r requirements.txt`.
- **Environment**: Copy `env.example` to `.env` and configure secrets/keys.
- **Database**: Use `python manage.py makemigrations` and `python manage.py migrate`.
- **Superuser**: Create with `python manage.py createsuperuser`.
- **Run Server**: `python manage.py runserver`.
- **Testing**: Run tests with `python manage.py test` (tests in each app's `tests.py`).
- **Static/Media**: Collect static files with `python manage.py collectstatic` for production.

## Conventions & Integration
- Use Bootstrap 5 for frontend, with custom theme colors (see README and `settings.py`).
- Admin panel is accessed at `/admin/` and is heavily customized.
- External dependencies: CKEditor 5, Jazzmin, crispy-forms, django-extensions.
- Database: SQLite3 for dev, PostgreSQL for production (set via `DATABASE_URL` in `.env`).
- Email: Console backend for dev, SMTP for production (set in `.env`).

## Key Files & Directories
- `nscpl_project/settings.py`: All major config, including CKEditor, Jazzmin, color palettes, static/media paths.
- `core/context_processors.py`: Custom context for templates.
- `requirements.txt`: Python dependencies.
- `env.example`: Environment variable template.
- `README.md`: Project overview and setup.

## Example Patterns
- To add a new model, create it in the relevant app's `models.py`, register in `admin.py`, and add migrations.
- For new template pages, add HTML to `templates/` and update views/urls in the relevant app.
- For custom admin UI, update Jazzmin settings in `settings.py`.

## Notes
- Do not hardcode secrets; always use environment variables.
- Follow Django app structure for new features.
- Use the color palette and CKEditor config from `settings.py` for UI consistency.

---

If any section is unclear or missing, please provide feedback to improve these instructions.