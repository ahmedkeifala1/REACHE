"""Content models for the iREACHE LASTMILE site.

The site mirrors the information architecture in organogram.jpeg: a small set of
reusable content types drive every page, so editors work from the Django admin
rather than from templates.
"""

from pathlib import Path

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_ckeditor_5.fields import CKEditor5Field


def _file_url(field):
    """Return a file's URL, or an empty string when no file is attached.

    Templates pass these straight into `include ... with`, which evaluates
    eagerly, so `.url` on an empty FieldFile would raise ValueError.
    """
    return field.url if field else ""


class PublishableQuerySet(models.QuerySet):
    """Hides unpublished rows from the public site but not from staff.

    Staff keep seeing drafts while signed in, which is what makes "save it now,
    publish it later" usable: an editor can open the real page and check their
    work before anybody else can reach it.
    """

    def visible_to(self, user):
        if getattr(user, "is_staff", False):
            return self
        return self.filter(is_published=True)


class Publishable(models.Model):
    """Adds the draft/published switch and the shared search-result fields."""

    is_published = models.BooleanField(
        default=True,
        verbose_name="Published",
        help_text="Untick to hide this from the public site. Staff still see it.",
    )
    meta_description = models.CharField(
        max_length=300,
        blank=True,
        help_text=(
            "One or two sentences shown by Google and by Facebook, LinkedIn and "
            "WhatsApp link previews. Falls back to the intro when left empty."
        ),
    )

    objects = PublishableQuerySet.as_manager()

    class Meta:
        abstract = True


class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton row holding global site chrome."""

    organisation_name = models.CharField(max_length=120, default="iREACHE LASTMILE")
    tagline = models.CharField(
        max_length=255,
        default="Innovations for Rural Empowerment in Access to Community Health and Equity",
    )
    hero_eyebrow = models.CharField(
        max_length=160,
        blank=True,
        default="Sierra Leone · Eastern Province · 2026",
        help_text="Small line printed above the hero headline.",
    )
    hero_prefix = models.CharField(max_length=120, default="Building the health system")
    hero_headline = models.CharField(
        max_length=255, default="Sierra Leone's communities"
    )
    hero_rotating_words = models.CharField(
        max_length=255,
        default="have always deserved.",
        help_text="Closing line of the hero headline. Several comma separated "
        "phrases are cycled; a single one stays put.",
    )
    hero_body = models.TextField(
        default="iREACHE LASTMILE connects three systems that have never governed "
        "community health together — traditional authority, government, and "
        "community intelligence — through 6,800 ProcCHWs reaching every "
        "last-mile household every month."
    )
    hero_image = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Home page hero background. Falls back to img/hero.svg.",
    )
    story_image = models.ImageField(
        upload_to="site/",
        blank=True,
        null=True,
        help_text="Photo beside the founding story block on the home page.",
    )
    footer_blurb = models.TextField(
        default="iREACHE LASTMILE works alongside government, communities and partners "
        "to build primary health care that reaches everyone, everywhere."
    )
    legal_line = models.CharField(
        max_length=255,
        default="iREACHE LASTMILE is a registered not-for-profit organisation",
    )
    email = models.EmailField(default="info@ireachelastmile.org")
    phone = models.CharField(max_length=60, blank=True, default="+232 00 000 000")
    address = models.CharField(
        max_length=255, blank=True, default="Freetown, Sierra Leone"
    )

    facebook = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    twitter = models.URLField(blank=True)

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return self.organisation_name

    @property
    def hero_image_url(self):
        return _file_url(self.hero_image)

    @property
    def story_image_url(self):
        return _file_url(self.story_image)

    @property
    def rotating_words(self):
        return [w.strip() for w in self.hero_rotating_words.split(",") if w.strip()]

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj


class MenuItem(TimeStamped):
    """Top level nav entry plus its dropdown children."""

    title = models.CharField(max_length=120)
    url = models.CharField(max_length=255, help_text="Absolute path, e.g. /who-we-are/")
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    order = models.PositiveIntegerField(default=0)
    is_button = models.BooleanField(
        default=False, help_text="Render as the highlighted Donate style button."
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Page(Publishable, TimeStamped):
    """A standard content page addressed by its full path.

    Two kinds of row live here. Most are standalone pages served by the
    ``page_detail`` catch-all. The rest have ``is_section_page`` set and stand
    behind one of the fixed routes in ``core/urls.py`` -- "Our Programs",
    "Meet Our Team" and the like -- where they supply the heading, intro,
    picture and optional extra copy that used to be hard-coded in the template.
    See ``core.section_pages``.
    """

    title = models.CharField(max_length=200)
    path = models.CharField(
        max_length=255,
        unique=True,
        help_text="Full path without leading/trailing slashes, e.g. who-we-are/our-team",
    )
    section = models.CharField(
        max_length=120,
        blank=True,
        help_text="Eyebrow label shown above the page title.",
    )
    intro = models.TextField(
        blank=True, help_text="Short paragraph under the page heading."
    )
    body = CKEditor5Field(blank=True, help_text="The main content of the page.")
    hero_image = models.ImageField(
        upload_to="pages/",
        blank=True,
        null=True,
        help_text="Wide photograph behind the page heading.",
    )
    show_newsletter = models.BooleanField(default=True)
    is_section_page = models.BooleanField(
        default=False,
        verbose_name="Section landing page",
        help_text=(
            "Set by seed_content for the pages behind a fixed route. Their path "
            "is what links them to that route, so changing it detaches the page "
            "and the built-in wording comes back."
        ),
    )

    class Meta:
        ordering = ["path"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:page", kwargs={"path": self.path})

    @property
    def hero_image_url(self):
        return _file_url(self.hero_image)


class PageImage(models.Model):
    """An extra picture attached to a page, shown in a grid below the body.

    The rich text editor already places pictures inside the prose. This is for
    the other case -- a set of photographs from a field visit, say -- where an
    editor wants a gallery without laying one out by hand.
    """

    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="pages/gallery/")
    caption = models.CharField(max_length=255, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or Path(self.image.name).name

    @property
    def image_url(self):
        return _file_url(self.image)


class FocusArea(TimeStamped):
    """The 'What We Do' pillars shown as icon cards on the home page."""

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.TextField()
    body = CKEditor5Field(
        blank=True, help_text="Full description shown on the focus area page."
    )
    icon = models.CharField(
        max_length=40,
        default="service",
        help_text=(
            "Icon key: service, workforce, data, supply, financing, "
            "accountability, partnership"
        ),
    )
    image = models.ImageField(upload_to="focus/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:focus_area", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        return _file_url(self.image)


class Program(TimeStamped):
    """Entries under 'Our Programs'."""

    title = models.CharField(max_length=180)
    slug = models.SlugField(max_length=180, unique=True)
    summary = models.TextField()
    body = CKEditor5Field(blank=True)
    image = models.ImageField(upload_to="programs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:program", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        return _file_url(self.image)


class Location(TimeStamped):
    """'Where We Work' country cards."""

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=120, unique=True)
    summary = models.TextField(blank=True)
    body = CKEditor5Field(blank=True)
    image = models.ImageField(upload_to="locations/", blank=True, null=True)
    is_office = models.BooleanField(
        default=False, help_text="iREACHE LASTMILE has an office here."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:location", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        return _file_url(self.image)


class Stat(TimeStamped):
    """Impact counters.

    ``group`` decides where a figure is printed. The ``hero`` figures are the
    four cards under the home page headline, each carrying a sentence and a
    short qualifier; the ``band`` figures are the compact row that runs across
    the angled green strip further down the page and across the donate page.
    The same number appears in both groups with different wording, which is why
    a figure is identified by its value *and* its group rather than value alone.
    """

    HERO = "hero"
    BAND = "band"
    GROUP_CHOICES = [(HERO, "Home page hero"), (BAND, "Impact band")]

    value = models.CharField(max_length=40, help_text="e.g. 155,000,000")
    label = models.TextField(help_text="Sentence describing the figure.")
    caption = models.CharField(
        max_length=120,
        blank=True,
        help_text="Short qualifier under a hero figure, e.g. 'Target < 300'.",
    )
    group = models.CharField(max_length=8, choices=GROUP_CHOICES, default=BAND)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return "{0} - {1}".format(self.value, self.label[:40])


class PostCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Post categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Post(Publishable, TimeStamped):
    """Newsroom and blog entries."""

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(
        PostCategory,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="posts",
    )
    excerpt = models.TextField(blank=True)
    body = CKEditor5Field(blank=True)
    image = models.ImageField(upload_to="posts/", blank=True, null=True)
    published = models.DateField(default=timezone.now)
    is_featured = models.BooleanField(
        default=False, help_text="Show in the featured strip under the hero."
    )
    featured_kicker = models.CharField(
        max_length=120, blank=True, help_text="Small label used in the featured strip."
    )

    class Meta:
        ordering = ["-published", "-id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:post", kwargs={"slug": self.slug})

    @property
    def image_url(self):
        return _file_url(self.image)


class TeamMember(TimeStamped):
    name = models.CharField(max_length=160)
    role = models.CharField(max_length=180)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="team/", blank=True, null=True)
    is_leadership = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Partner(TimeStamped):
    name = models.CharField(max_length=180)
    url = models.URLField(blank=True)
    logo = models.ImageField(upload_to="partners/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Resource(TimeStamped):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=80, default="Report")
    file = models.FileField(upload_to="resources/", blank=True, null=True)
    external_url = models.URLField(blank=True)
    published = models.DateField(default=timezone.now)

    class Meta:
        ordering = ["-published"]

    def __str__(self):
        return self.title

    @property
    def link(self):
        if self.file:
            return self.file.url
        return self.external_url or "#"


class Job(TimeStamped):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    location = models.CharField(max_length=120, default="Freetown, Sierra Leone")
    employment_type = models.CharField(max_length=80, default="Full time")
    description = CKEditor5Field(blank=True)
    closing_date = models.DateField(null=True, blank=True)
    is_open = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class NewsletterSignup(models.Model):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.email


class ContactMessage(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return "{0} - {1}".format(self.name, self.subject or "No subject")
