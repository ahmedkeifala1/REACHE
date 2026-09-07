"""Attaches the placeholder photo library in `core/seed_assets/` to content.

Run with:  python manage.py seed_images

The command copies each file into MEDIA_ROOT under the field's own `upload_to`
directory and points the record at it, so it is idempotent - re-running does not
create `image_XyZ123.jpg` duplicates the way `FileField.save()` would.

Records that already carry an image are left alone unless `--force` is passed,
so an editor's upload is never overwritten by a re-run.

The photographs are third-party placeholders. See `core/seed_assets/CREDITS.md`
before this site goes anywhere near production.
"""

import shutil
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import FocusArea, Location, Page, Post, Program, SiteSettings

SEED_DIR = Path(__file__).resolve().parents[2] / "seed_assets"

# ------------------------------------------------------------------ mapping
# Each map is {lookup value: seed file}. A file may appear more than once - the
# library is smaller than the number of slots, so related sections share a photo.

SITE_IMAGES = {
    "hero_image": "hero-home.jpg",
    "story_image": "founding-story.jpg",
}

FOCUS_IMAGES = {
    "proactive-community-health-service-delivery": "community-health-visit.jpg",
    "connected-health-workforce-strengthening": "health-education.jpg",
    "community-intelligence-surveillance-systems": "data-review.jpg",
    "last-mile-supply-chain-and-community-access": "cold-chain.jpg",
    "sustainable-health-financing-and-domestic-resource-mobilization": "pharmacy-stock.jpg",
    "three-authority-community-government-and-accountability": "partnership-meeting.jpg",
    "drive-sustained-impact-through-strategic-partnership": "partnership-hands.jpg",
}

PROGRAM_IMAGES = {
    "healthy-pregnancies-and-newborn-health": "newborn-care.jpg",
    "defeating-childhood-diseases": "child-vaccination.jpg",
    "sexual-and-reproductive-health": "family-planning.jpg",
    "immunization-and-zero-dose-reduction": "school-outreach.jpg",
    "climate-and-health-resilience": "flood-delivery.jpg",
    "emergency-preparedness-and-outbreak-response": "community-meeting.jpg",
    "health-and-nutrition": "mothers-and-infants.jpg",
}

LOCATION_IMAGES = {
    "sierra-leone": "health-facility.jpg",
}

POST_IMAGES = {
    "reaching-the-last-mile-what-changes-when-care-comes-to-the-household": "community-health-visit.jpg",
    "keeping-the-cold-chain-cold-preventive-maintenance-that-actually-happens": "cold-chain.jpg",
    "community-surveillance-in-practice-acting-on-signals-early": "data-review.jpg",
    "financing-primary-health-care-beyond-the-grant-cycle": "pharmacy-window.jpg",
    "zero-dose-children-are-not-hard-to-reach-they-are-under-reached": "immunization-campaign.jpg",
    "a-midwifes-patience-one-family-planning-conversation-at-a-time": "family-planning.jpg",
    "training-traditional-healers-as-partners-not-competitors": "community-outreach.jpg",
    "when-learning-travels-turning-peer-exchange-into-action": "health-workers-group.jpg",
    "nutrition-screening-at-every-contact": "mothers-and-infants.jpg",
    "climate-shocks-and-the-health-facilities-that-absorb-them": "flood-delivery.jpg",
    "building-an-outbreak-response-that-communities-trust": "community-meeting.jpg",
    "the-three-authorities-aligning-community-government-and-health-system": "partnership-meeting.jpg",
}

PAGE_IMAGES = {
    "who-we-are": "field-visit.jpg",
    "who-we-are/founding-story": "founding-story.jpg",
    "who-we-are/mission-vision-values": "health-worker-portrait.jpg",
    "who-we-are/our-approach": "community-health-visit.jpg",
    "who-we-are/our-strategy": "partnership-meeting.jpg",
    "who-we-are/strategy-2030": "walking-the-trail.jpg",
    "our-model": "last-mile-road.jpg",
    "our-model/bridge-360": "partnership-hands.jpg",
    "our-model/lastmile-care": "mother-and-baby.jpg",
    "our-model/the-challenge": "vaccine-delivery.jpg",
    "our-impact": "immunization-campaign.jpg",
    "our-impact/governance-and-financials": "data-review.jpg",
    "our-impact/history": "milestone.jpg",
    "research": "health-education.jpg",
    "get-involved": "health-workers-group.jpg",
    "photo-policy": "health-facility.jpg",
    "privacy-policy": "cold-chain-transport.jpg",
}


class Command(BaseCommand):
    help = "Attach the seed photo library to pages, programs, posts and locations."

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Replace images that are already set instead of skipping them.",
        )

    def handle(self, *args, **options):
        if not SEED_DIR.is_dir():
            self.stderr.write(f"Seed image directory missing: {SEED_DIR}")
            return

        self.force = options["force"]
        self.attached = 0
        self.skipped = 0
        self.missing = set()

        site = SiteSettings.load()
        for field, filename in SITE_IMAGES.items():
            self._attach(site, field, filename)
        site.save()

        self._attach_many(FocusArea, "slug", "image", FOCUS_IMAGES)
        self._attach_many(Program, "slug", "image", PROGRAM_IMAGES)
        self._attach_many(Location, "slug", "image", LOCATION_IMAGES)
        self._attach_many(Post, "slug", "image", POST_IMAGES)
        self._attach_many(Page, "path", "hero_image", PAGE_IMAGES)

        for name in sorted(self.missing):
            self.stderr.write(f"Seed file not found: {name}")
        self.stdout.write(
            self.style.SUCCESS(
                f"Images attached: {self.attached}, left as-is: {self.skipped}"
            )
        )

    # ------------------------------------------------------------- internals
    def _attach_many(self, model, lookup, field, mapping):
        for value, filename in mapping.items():
            obj = model.objects.filter(**{lookup: value}).first()
            if obj is None:
                self.stderr.write(f"{model.__name__} not found: {value}")
                continue
            if self._attach(obj, field, filename):
                obj.save(update_fields=[field])

    def _attach(self, obj, field, filename):
        """Copy one seed file into MEDIA_ROOT and point `field` at it."""
        source = SEED_DIR / filename
        if not source.is_file():
            self.missing.add(filename)
            return False

        current = getattr(obj, field)
        if current and not self.force:
            self.skipped += 1
            return False

        folder = obj._meta.get_field(field).upload_to
        target = Path(settings.MEDIA_ROOT) / folder / filename
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or target.stat().st_size != source.stat().st_size:
            shutil.copyfile(source, target)

        setattr(obj, field, f"{folder}{filename}")
        self.attached += 1
        return True
