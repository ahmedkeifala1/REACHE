# REACHE Last-Mile

Django website for REACHE Last-Mile — an NGO building primary health care that
reaches the hardest-to-reach communities in Sierra Leone.

## Stack

- Django 5.1 (see `requirements.txt`)
- PostgreSQL
- CKEditor 5 for the body fields in the admin
- Server-rendered templates, hand-written CSS in `static/css/style.css`

## Getting started

Create the database first. Any PostgreSQL 13 or newer will do; this is the
database `reache/settings.py` looks for when `DATABASE_URL` is not set.

```bash
createdb -h 127.0.0.1 -U postgres reache
```

Then:

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python manage.py migrate
python manage.py seed_content    # navigation, starter content, section pages
python manage.py seed_images     # placeholder photography (see the warning below)
python manage.py setup_cms       # the Editors group
python manage.py createsuperuser
python manage.py runserver
```

The site runs at http://127.0.0.1:8000/, the admin at `/admin/`.

To use a different server -- a colleague's, or a hosted one -- set `DATABASE_URL`
and nothing else changes:

```bash
DATABASE_URL=postgres://user:password@host:5432/dbname python manage.py migrate
```

## Layout

| Path | Purpose |
| --- | --- |
| `core/models.py` | Content models — pages, focus areas, programs, locations, posts, team, partners, resources, jobs, menu, site settings |
| `core/views.py` | One view per section; `page_detail` serves editor-managed flat pages |
| `core/urls.py` | Fixed routes first, the catch-all flat-page route last |
| `core/section_pages.py` | Joins each fixed route to the `Page` an editor changes it from, and holds the wording it falls back to |
| `core/storage.py` | Sends pictures uploaded inside the editor to `media/uploads/` |
| `core/admin.py` | The CMS itself — thumbnails, draft/publish, grouped fields |
| `core/context_processors.py` | Injects `site` and `main_menu` into every template |
| `core/management/commands/seed_content.py` | Rebuilds the menu and (re)seeds starter content; safe to re-run |
| `core/management/commands/seed_images.py` | Attaches the placeholder photo library to that content; safe to re-run |
| `core/management/commands/setup_cms.py` | Creates the Editors group; safe to re-run |
| `core/seed_assets/` | The placeholder photo library and its `CREDITS.md` |
| `templates/` | `base.html`, `pages/`, and reusable `partials/` |

## Content editing

Everything on the site is editable in the Django admin at `/admin/`.

### Pages

Two kinds of row live in **Pages**, and the list shows which is which.

**Standalone pages** are matched on their `path` (for example
`who-we-are/our-approach`), so a new one needs no code change — add the `Page`,
then a `MenuItem` pointing at it.

**Section landing pages** stand behind a fixed route: "Our Programs", "Meet Our
Team", "Ways to Give" and seven others. Their heading, eyebrow, introduction and
picture used to be written into the template, which made them the only copy on
the site nobody could change. Editing one now changes the live page, its browser
tab and its link preview. Anything typed into the body appears under the heading,
above the list the page exists to show.

Their `path` is what joins them to their route, so the admin will not let you
edit or delete one. `core/section_pages.py` holds the list and the wording each
falls back to when its row is missing.

### Pictures

Every picture field shows a thumbnail in the admin, so it is obvious which rows
still carry placeholder photography.

There are two ways to add one. The toolbar in any body field uploads a picture
into the text itself — those land in `media/uploads/`. Every page also has an
**Extra pictures** section at the bottom of its form, which renders as a gallery
below the body.

### Drafts

Pages and posts have a **Published** tick. Clearing it hides the row from
visitors — off the listings, out of search, 404 on its own URL — while staff who
are signed in still see it, so you can check a page before anyone else can reach
it. The list pages can publish or hide a batch in one action.

### Who can edit what

`python manage.py setup_cms` creates an **Editors** group that can change every
piece of content and nothing else: no user accounts, no deleting the site
settings, no inventing contact messages. Give someone that role in
**Users** — tick *Staff status*, add them to *Editors*, leave *Superuser status*
clear. A superuser can do all of that, so day-to-day editors should not be one.

`seed_content` deletes and rebuilds the menu, so re-running it discards hand-made
menu edits. Section landing pages are created once and never overwritten. All
other content is updated in place by slug.

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
forms. It also covers the CMS: that every section landing page is created and
that editing one changes the page, that drafts are hidden from visitors but not
from staff, that the Editors group cannot reach user accounts, and that an
anonymous picture upload is refused.

It needs a PostgreSQL it can create a test database on, which the local
`postgres` superuser can do.

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

### The deployment needs its own database

The site runs on PostgreSQL, and a PostgreSQL on somebody's laptop is not
reachable from a Vercel function. Until the Vercel project has a `DATABASE_URL`
of its own, `reache/settings.py` falls back to the SQLite copy bundled with the
deployment: Vercel's filesystem is read-only apart from `/tmp`, so that copy is
written to `/tmp` on cold start and **every write is lost when the instance
recycles** — an admin edit, a contact message or a newsletter signup does not
survive. In that state the deployment is a review copy, not a CMS.

To make the live admin durable, create a hosted PostgreSQL (Neon, Supabase and
Vercel Postgres all have a free tier), then set `DATABASE_URL` in the Vercel
environment to its connection string. Nothing in the code changes — that setting
is all `settings.py` is waiting for. Then run the migrations against it once:

```bash
DATABASE_URL=<the hosted connection string> python manage.py migrate
DATABASE_URL=<the hosted connection string> python manage.py setup_cms
DATABASE_URL=<the hosted connection string> python manage.py createsuperuser
```

To carry the local content across, `dumpdata` on this machine and `loaddata`
against the hosted URL.

> [!IMPORTANT]
> Uploads still are not durable. A picture added through the admin or the editor
> is written to the function's filesystem, which is discarded with the instance
> exactly as the SQLite copy is. Fixing that needs `django-storages` pointed at
> S3, R2 or Cloudinary:
>
> ```bash
> pip install django-storages boto3
> ```
>
> Until then, treat the hosted database as the durable half and add photography
> locally, redeploying to publish it.

### Environment variables

Set these in the Vercel project (Settings → Environment Variables):

| Variable | Value |
| --- | --- |
| `DATABASE_URL` | Hosted PostgreSQL connection string. Without it the deployment uses the throwaway SQLite copy described above |
| `DJANGO_SECRET_KEY` | Long random value |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | `.vercel.app` (plus any custom domain) |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://*.vercel.app` (plus any custom domain) |

## Deployment

Development defaults live in `reache/settings.py`. In production set:

| Variable | Notes |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `DJANGO_SECRET_KEY` | Long random value |
| `DJANGO_DEBUG` | `0` |
| `DJANGO_ALLOWED_HOSTS` | Comma-separated hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | Comma-separated origins, e.g. `https://reachelastmile.org` |

With `DJANGO_DEBUG=0` the HTTPS, HSTS and secure-cookie settings switch on
automatically. Then run `python manage.py collectstatic` and serve `staticfiles/`
and `media/` from the web server. `python manage.py check --deploy` should report
no warnings.
