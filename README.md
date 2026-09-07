# REACHE Last-Mile

Django website for REACHE Last-Mile — an NGO building primary health care that
reaches the hardest-to-reach communities in Sierra Leone.

## Stack

- Django 5.1 (see `requirements.txt`)
- SQLite in development
- Server-rendered templates, hand-written CSS in `static/css/style.css`

## Getting started

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_content    # navigation + starter content
python manage.py seed_images     # placeholder photography (see the warning below)
python manage.py createsuperuser
python manage.py runserver
```

The site runs at http://127.0.0.1:8000/, the admin at `/admin/`.

## Layout

| Path | Purpose |
| --- | --- |
| `core/models.py` | Content models — pages, focus areas, programs, locations, posts, team, partners, resources, jobs, menu, site settings |
| `core/views.py` | One view per section; `page_detail` serves editor-managed flat pages |
| `core/urls.py` | Fixed routes first, the catch-all flat-page route last |
| `core/context_processors.py` | Injects `site` and `main_menu` into every template |
| `core/management/commands/seed_content.py` | Rebuilds the menu and (re)seeds starter content; safe to re-run |
| `core/management/commands/seed_images.py` | Attaches the placeholder photo library to that content; safe to re-run |
| `core/seed_assets/` | The placeholder photo library and its `CREDITS.md` |
| `templates/` | `base.html`, `pages/`, and reusable `partials/` |

## Content editing

Everything on the site is editable in the Django admin. Flat pages are matched on
their `path` field (for example `who-we-are/our-approach`), so new sections can be
added without a code change — add the `Page`, then a `MenuItem` pointing at it.

`seed_content` deletes and rebuilds the menu, so re-running it discards hand-made
menu edits. All other content is updated in place by slug.

## Photography

> [!WARNING]
> The images in `core/seed_assets/` are **placeholders taken from
> villagereach.org**. They are copyright VillageReach and its photographers, they
> show identifiable people in VillageReach's own programmes in Malawi,
> Mozambique and the DRC, and REACHE has no licence to publish them. They exist
> so the layout can be reviewed with real photographs in it. **Replace every one
> of them with REACHE's own licensed photography before this site goes live.**
> `core/seed_assets/CREDITS.md` lists each file and where it came from.

> [!IMPORTANT]
> Because of the above, `core/seed_assets/` and `media/` are **not in this
> repository** — `.gitignore` excludes them. A fresh clone therefore has no
> photography and `seed_images` has nothing to copy; the templates fall back to
> their grey `.placeholder` blocks, which is the intended behaviour until REACHE's
> own pictures arrive. Drop licensed photographs into `core/seed_assets/` (keeping
> the filenames in `CREDITS.md`) and `seed_images` works again.

`seed_images` copies the library into `media/` and attaches it to the site
settings, focus areas, programs, locations, posts and flat pages. It skips any
record that already has an image, so uploading a real photo in the admin is
enough to retire a placeholder — pass `--force` only to reset back to the seeds.

To clear the placeholders wholesale once real photography arrives, delete
`core/seed_assets/`, `core/management/commands/seed_images.py` and the matching
folders under `media/`.

## Tests

```bash
python manage.py test core
```

The suite seeds the site, renders every route and flat page, crawls every internal
link from the home page for 404s, and exercises the search, contact and newsletter
forms.

## Hosting (Vercel)

The site is deployed to Vercel from this directory with the Vercel CLI, which
uploads the working copy rather than the git checkout — that is how the
placeholder photography reaches the deployment without ever entering this public
repository. `.vercelignore` keeps `core/seed_assets/` out of the bundle, since
`media/` already holds the copies the site actually serves.

```bash
python manage.py collectstatic --noinput   # staticfiles/ ships inside the function
vercel deploy                              # protected preview
vercel deploy --prod                       # public production URL
```

> [!CAUTION]
> Deploy with `vercel deploy` (a **protected preview**) for as long as the
> placeholder photography is in `media/`. `--prod` publishes those photographs at a
> public URL, which is the thing the warning above says not to do.

`vercel.json` routes every request to `reache/wsgi.py`. There is no web server in
front of the application, so WhiteNoise serves `staticfiles/` (middleware) and
`media/` (a wrapper in `reache/wsgi.py`, because Django stops serving `MEDIA_ROOT`
once `DEBUG` is off).

### The database is ephemeral

Vercel's filesystem is read-only apart from `/tmp`, so `reache/settings.py` copies
the bundled `db.sqlite3` to `/tmp` on cold start. Reads work and writes succeed,
but **every write is lost when the instance recycles** — an admin edit, a contact
message or a newsletter signup does not survive. The deployment is a review copy,
not a CMS.

To make writes durable, point Django at a managed Postgres (Neon, Supabase or
Vercel Postgres) and put uploads on object storage:

```bash
pip install "psycopg[binary]" dj-database-url django-storages boto3
```

then set `DATABASE_URL` in the Vercel environment and read it in `settings.py`
with `dj_database_url.config()`. Media needs `django-storages` pointed at S3, R2 or
Cloudinary, because uploads written to `/tmp` disappear the same way.

### Environment variables

Set these in the Vercel project (Settings → Environment Variables):

| Variable | Value |
| --- | --- |
| `DJANGO_SECRET_KEY` | Long random value |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` (plus any custom domain) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` (plus any custom domain) |

## Deployment

Development defaults live in `reache/settings.py`. In production set:

| Variable | Notes |
| --- | --- |
| `DJANGO_SECRET_KEY` | Long random value |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated origins, e.g. `https://reachelastmile.org` |

With `DJANGO_DEBUG=0` the HTTPS, HSTS and secure-cookie settings switch on
automatically. Then run `python manage.py collectstatic` and serve `staticfiles/`
and `media/` from the web server. `python manage.py check --deploy` should report
no warnings.
