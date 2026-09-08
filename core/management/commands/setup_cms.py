"""Creates the Editors group.

Run with:  python manage.py setup_cms

A superuser can do anything, including delete the staff accounts and empty the
site. Most of the people who write for iREACHE LASTMILE need none of that, so this command
builds a group that can edit every piece of content and nothing else.

It is safe to re-run: permissions are set, not added to, so a group that has
drifted is brought back in line. Membership is untouched -- you add people to the
group in the admin, and this command never removes them.
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from core import models

EDITORS_GROUP = "Editors"

# Full control: these are the models the site is written in.
CONTENT_MODELS = (
    models.FocusArea,
    models.Job,
    models.Location,
    models.MenuItem,
    models.Page,
    models.PageImage,
    models.Partner,
    models.Post,
    models.PostCategory,
    models.Program,
    models.Resource,
    models.Stat,
    models.TeamMember,
)

# Editable but never deletable: one row that the whole site reads from.
SETTINGS_MODELS = (models.SiteSettings,)

# Read and triage only. These are messages from the public, not content, and
# nobody should be able to add one by hand or quietly delete one.
INBOX_MODELS = (models.ContactMessage, models.NewsletterSignup)


class Command(BaseCommand):
    help = "Create or repair the Editors group used by the site's content staff."

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name=EDITORS_GROUP)

        wanted = []
        wanted += self._permissions(CONTENT_MODELS, ("add", "change", "delete", "view"))
        wanted += self._permissions(SETTINGS_MODELS, ("change", "view"))
        wanted += self._permissions(INBOX_MODELS, ("change", "view"))

        group.permissions.set(wanted)

        verb = "Created" if created else "Updated"
        self.stdout.write(
            self.style.SUCCESS(
                "{0} the {1} group with {2} permissions.".format(
                    verb, EDITORS_GROUP, len(wanted)
                )
            )
        )
        self.stdout.write(
            "Give someone this role in the admin under Authentication and "
            "Authorisation > Users: tick 'Staff status' so they can sign in, "
            "add them to Editors, and leave 'Superuser status' unticked."
        )

    def _permissions(self, model_classes, actions):
        found = []
        for model in model_classes:
            content_type = ContentType.objects.get_for_model(model)
            for action in actions:
                codename = "{0}_{1}".format(action, model._meta.model_name)
                try:
                    found.append(
                        Permission.objects.get(
                            content_type=content_type, codename=codename
                        )
                    )
                except Permission.DoesNotExist:
                    # Only reachable if migrations have not finished creating
                    # the permission rows, which would make a silent skip
                    # produce a group that looks right and is not.
                    self.stderr.write(
                        self.style.WARNING("missing permission " + codename)
                    )
        return found
