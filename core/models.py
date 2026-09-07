"""Content models for the REACHE Last-Mile site.

The site mirrors the information architecture in organogram.jpeg: a small set of
reusable content types drive every page, so editors work from the Django admin
rather than from templates.
"""

from django.db import models
from django.urls import reverse
from django.utils import timezone


def _file_url(field):
    """Return a file's URL, or an empty string when no file is attached.

    Templates pass these straight into `include ... with`, which evaluates
    eagerly, so `.url` on an empty FieldFile would raise ValueError.
    """
    return field.url if field else ""


class TimeStamped(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """Singleton row holding global site chrome."""

    organisation_name = models.CharField(max_length=120, default="REACHE Last-Mile")
    tagline = models.CharField(
        max_length=255,
        default="Innovation for Rural Empowerment in Access to Community Health and Equity",
    )
    hero_prefix = models.CharField(max_length=120, default="REACHE transforms")
    hero_headline = models.CharField(
        max_length=255, default="health care delivery to reach"
    )
    hero_rotating_words = models.CharField(
        max_length=255,
        default="everyone,every mother,every newborn,every village",
        help_text="Comma separated words cycled in the hero headline.",
    )
    hero_body = models.TextField(
        default="REACHE Last-Mile designs responsive primary health care systems so that "
        "life-saving products and services reach the communities hardest to reach."
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
        default="REACHE Last-Mile works alongside government, communities and partners "
        "to build primary health care that reaches everyone, everywhere."
    )
    legal_line = models.CharField(
        max_length=255,
        default="REACHE Last-Mile is a registered not-for-profit organisation",
    )
    email = models.EmailField(default="info@reachelastmile.org")
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


class Page(TimeStamped):
    """A standard content page addressed by its full path."""

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
    intro = models.TextField(blank=True)
    body = models.TextField(blank=True, help_text="HTML content for the page body.")
    hero_image = models.ImageField(upload_to="pages/", blank=True, null=True)
    show_newsletter = models.BooleanField(default=True)

    class Meta:
        ordering = ["path"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:page", kwargs={"path": self.path})

    @property
    def hero_image_url(self):
        return _file_url(self.hero_image)


class FocusArea(TimeStamped):
    """The 'What We Do' pillars shown as icon cards on the home page."""

    title = models.CharField(max_length=160)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.TextField()
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
    body = models.TextField(blank=True)
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
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="locations/", blank=True, null=True)
    is_office = models.BooleanField(
        default=False, help_text="REACHE has an office here."
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
    """Impact counters."""

    value = models.CharField(max_length=40, help_text="e.g. 155,000,000")
    label = models.TextField(help_text="Sentence describing the figure.")
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


class Post(TimeStamped):
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
    body = models.TextField(blank=True)
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
    description = models.TextField(blank=True)
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
