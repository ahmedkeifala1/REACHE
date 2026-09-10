"""Smoke tests for the iREACHE LASTMILE site.

The suite seeds the site once per class with the same management command the
project ships with, then walks the navigation the way a visitor would.
"""

import re

from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.html import escape

from .models import (
    ContactMessage,
    FocusArea,
    Location,
    MenuItem,
    NewsletterSignup,
    Page,
    PageImage,
    Post,
    Program,
    SiteSettings,
    Stat,
)
from .section_pages import SECTION_PAGES


class SeededSiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_seed_populates_the_site(self):
        self.assertTrue(MenuItem.objects.exists())
        self.assertTrue(FocusArea.objects.exists())
        self.assertTrue(Program.objects.exists())
        self.assertTrue(Location.objects.exists())
        self.assertTrue(Page.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_named_routes_render(self):
        names = [
            "core:home",
            "core:what_we_do",
            "core:programs",
            "core:where_we_work",
            "core:team",
            "core:partners",
            "core:newsroom",
            "core:resources",
            "core:work_for_us",
            "core:contact",
            "core:donate",
            "core:search",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name)).status_code, 200)

    def test_detail_routes_render(self):
        details = [
            ("core:focus_area", FocusArea.objects.all()),
            ("core:program", Program.objects.all()),
            ("core:location", Location.objects.all()),
            ("core:post", Post.objects.all()),
        ]
        for name, queryset in details:
            for obj in queryset:
                with self.subTest(name=name, slug=obj.slug):
                    url = reverse(name, kwargs={"slug": obj.slug})
                    self.assertEqual(self.client.get(url).status_code, 200)

    def test_flat_pages_render(self):
        for page in Page.objects.all():
            with self.subTest(path=page.path):
                response = self.client.get("/{0}/".format(page.path))
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, escape(page.title))

    def test_unknown_page_returns_404(self):
        self.assertEqual(self.client.get("/no-such-page/").status_code, 404)

    def test_no_broken_internal_links(self):
        """Crawls every in-site link reachable from the home page."""
        seen, queue, broken = set(), ["/"], []
        while queue:
            url = queue.pop(0)
            if url in seen:
                continue
            seen.add(url)
            response = self.client.get(url, follow=True)
            if response.status_code != 200:
                broken.append((url, response.status_code))
                continue
            html = response.content.decode("utf-8", "ignore")
            for href in re.findall(r'href="(/[^"#?]*)"', html):
                if href not in seen and not href.startswith(
                    ("/static", "/media", "/admin")
                ):
                    queue.append(href)
        self.assertEqual(broken, [], "Broken internal links: {0}".format(broken))
        self.assertGreater(len(seen), 20)


class FrameworkContentTests(TestCase):
    """The site's content is the REACH 360 Master Document, not placeholder copy."""

    #  The seven pillars, in the order the Master Document numbers them.
    PILLARS = [
        "connected-health-workforce",
        "community-intelligence-and-surveillance-system",
        "last-mile-supply-chain-and-commodity-access",
        "sustainable-health-financing-and-domestic-resource-mobilisation",
        "three-authority-community-governance-and-accountability",
        "proactive-community-health-service-delivery",
        "driving-sustained-impact-through-strategic-partnerships",
    ]

    FRAMEWORK_PAGES = [
        "our-model",
        "our-model/the-challenge",
        "our-model/bridge-360",
        "our-model/lastmile-care",
        "our-model/procchw",
        "reach-360",
        "reach-360/three-systems",
        "reach-360/foundations",
        "reach-360/idhs",
        "reach-360/connection-quality-index",
    ]

    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_seven_pillars_are_seeded_in_document_order(self):
        seeded = list(
            FocusArea.objects.order_by("order").values_list("slug", flat=True)
        )
        self.assertEqual(seeded, self.PILLARS)

    def test_every_pillar_carries_a_body(self):
        for area in FocusArea.objects.all():
            with self.subTest(pillar=area.slug):
                self.assertIn("WHO building block", area.body)

    def test_pillar_pages_render_their_body(self):
        for area in FocusArea.objects.all():
            with self.subTest(pillar=area.slug):
                response = self.client.get("/what-we-do/{0}/".format(area.slug))
                self.assertContains(response, "WHO building block")

    def test_framework_pages_exist_and_render(self):
        for path in self.FRAMEWORK_PAGES:
            with self.subTest(path=path):
                self.assertTrue(Page.objects.filter(path=path).exists())
                response = self.client.get("/{0}/".format(path))
                self.assertEqual(response.status_code, 200)

    def test_bridge_360_is_the_documents_acronym(self):
        """The pre-document seed invented a different expansion of BRIDGE."""
        response = self.client.get("/our-model/bridge-360/")
        self.assertContains(response, "esilient")
        self.assertNotContains(response, "Baseline")

    def test_superseded_focus_areas_are_removed(self):
        FocusArea.objects.create(
            slug="drive-sustained-impact-through-strategic-partnership",
            title="Superseded",
            summary="",
        )
        call_command("seed_content", verbosity=0)
        self.assertEqual(FocusArea.objects.count(), len(self.PILLARS))

    def test_site_is_named_for_the_document(self):
        """The document names the organisation iREACHE LASTMILE throughout."""
        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.organisation_name, "iREACHE LASTMILE")
        # The *i* stands for the plural "Innovations".
        self.assertTrue(settings_obj.tagline.startswith("Innovations for Rural"))
        self.assertContains(self.client.get("/"), "iREACHE LASTMILE")

    def test_superseded_site_settings_are_rewritten(self):
        settings_obj = SiteSettings.load()
        settings_obj.organisation_name = "REACHE Last-Mile"
        settings_obj.tagline = (
            "Innovation for Rural Empowerment in Access to Community Health and Equity"
        )
        settings_obj.email = "info@reachelastmile.org"
        settings_obj.save()
        call_command("seed_content", verbosity=0)
        settings_obj = SiteSettings.load()
        self.assertEqual(settings_obj.organisation_name, "iREACHE LASTMILE")
        self.assertTrue(settings_obj.tagline.startswith("Innovations for Rural"))
        self.assertEqual(settings_obj.email, "info@ireachelastmile.org")

    def test_settings_an_editor_has_changed_are_left_alone(self):
        settings_obj = SiteSettings.load()
        settings_obj.footer_blurb = "Wording the communications team chose."
        settings_obj.save()
        call_command("seed_content", verbosity=0)
        self.assertEqual(
            SiteSettings.load().footer_blurb, "Wording the communications team chose."
        )

    def test_placeholder_statistics_are_removed(self):
        Stat.objects.create(value="2,400,000", label="Placeholder")
        call_command("seed_content", verbosity=0)
        self.assertFalse(Stat.objects.filter(value="2,400,000").exists())
        self.assertTrue(Stat.objects.filter(value="6,800").exists())


class WebsiteDocumentTests(TestCase):
    """The home page and Who We Are section follow the REACH 360 website document.

    That document supersedes the Master Document on the wording a visitor reads
    first: the hero headline, the four framing figures beneath it, the origin
    narrative, and the tables the framework, phasing and CQI pages are built
    from.
    """

    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_hero_carries_the_documents_headline(self):
        response = self.client.get("/")
        self.assertContains(response, "Sierra Leone \u00b7 Eastern Province \u00b7 2026")
        self.assertContains(response, "Building the health system")
        self.assertContains(response, escape("Sierra Leone's communities"))
        self.assertContains(response, "have always deserved.")
        self.assertContains(response, "connects three systems that have never governed")

    def test_hero_actions_reach_the_pages_they_name(self):
        for path in ("/our-model/", "/who-we-are/founding-story/", "/our-impact/"):
            with self.subTest(path=path):
                self.assertEqual(self.client.get(path).status_code, 200)

    def test_the_four_framing_figures_are_on_the_home_page(self):
        response = self.client.get("/")
        for value, caption in (
            ("6,800", "All districts"),
            ("4.5M", "By 2031"),
            ("354", "Target &lt; 300"),
            ("$1", "Why we exist"),
        ):
            with self.subTest(value=value):
                self.assertContains(response, value)
                self.assertContains(response, caption)

    def test_the_two_stat_groups_are_kept_apart(self):
        """6,800 is in both groups, with the band's shorter wording of it."""
        self.assertEqual(Stat.objects.filter(group=Stat.HERO).count(), 4)
        self.assertEqual(Stat.objects.filter(group=Stat.BAND).count(), 5)
        band = Stat.objects.get(group=Stat.BAND, value="6,800")
        self.assertEqual(band.label, "ProcCHWs by 2031")
        self.assertEqual(band.caption, "")

    def test_the_superseded_financing_figure_is_removed(self):
        Stat.objects.create(value="70\u201380%", label="Superseded", group=Stat.BAND)
        call_command("seed_content", verbosity=0)
        self.assertFalse(Stat.objects.filter(value="70\u201380%").exists())

    def test_founding_story_is_the_origin_narrative(self):
        response = self.client.get("/who-we-are/founding-story/")
        self.assertContains(response, "Augustine Alie")
        self.assertContains(response, "Niawa")
        self.assertContains(response, "March 2019")
        self.assertContains(response, "What if we connected them?")

    def test_our_approach_walks_all_three_systems(self):
        response = self.client.get("/who-we-are/our-approach/")
        for system in (
            "Traditional Authority System",
            "Government Health System",
            "Community Epidemiological System",
        ):
            with self.subTest(system=system):
                self.assertContains(response, system)

    def test_the_documents_tables_are_rendered_as_tables(self):
        for path, tables in (
            ("who-we-are/mission-vision-values", 1),
            ("who-we-are/strategy-2030", 1),
            ("reach-360", 1),
            ("reach-360/connection-quality-index", 2),
        ):
            with self.subTest(path=path):
                body = self.client.get("/{0}/".format(path)).content.decode()
                self.assertEqual(body.count("<table>"), tables)
                self.assertEqual(body.count('class="table-wrap"'), tables)

    def test_eight_values_are_described_in_practice(self):
        response = self.client.get("/who-we-are/mission-vision-values/")
        for value in (
            "Equity",
            "Excellence",
            "Accountability",
            "Co-ownership",
            "Government primacy",
            "Evidence",
            "Human primacy in digital health",
            "Dignity",
        ):
            with self.subTest(value=value):
                self.assertContains(response, "<th scope=\"row\">{0}</th>".format(value))


class SearchTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_blank_search_reports_nothing(self):
        response = self.client.get(reverse("core:search"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total"], 0)

    def test_search_finds_content(self):
        response = self.client.get(reverse("core:search"), {"q": "health"})
        self.assertEqual(response.status_code, 200)
        self.assertGreater(response.context["total"], 0)

    def test_newsroom_filters_by_category(self):
        post = Post.objects.exclude(category__isnull=True).first()
        self.assertIsNotNone(post)
        response = self.client.get(
            reverse("core:newsroom"), {"category": post.category.slug}
        )
        self.assertEqual(response.status_code, 200)
        for item in response.context["page_obj"]:
            self.assertEqual(item.category, post.category)


class FormTests(TestCase):
    def test_contact_form_stores_message(self):
        response = self.client.post(
            reverse("core:contact"),
            {
                "name": "Aminata Kamara",
                "email": "aminata@example.com",
                "subject": "Partnership",
                "message": "We would like to collaborate.",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertContains(response, "Thank you")

    def test_contact_form_rejects_missing_fields(self):
        response = self.client.post(
            reverse("core:contact"),
            {"name": "", "email": "", "message": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_newsletter_signup_is_idempotent(self):
        for _ in range(2):
            response = self.client.post(
                reverse("core:newsletter"),
                {"email": "reader@example.com", "next": "/"},
                follow=True,
            )
            self.assertEqual(response.status_code, 200)
        self.assertEqual(NewsletterSignup.objects.count(), 1)

    def test_newsletter_rejects_blank_email(self):
        self.client.post(reverse("core:newsletter"), {"email": "", "next": "/"})
        self.assertEqual(NewsletterSignup.objects.count(), 0)


class SectionPageTests(TestCase):
    """The ten pages whose headings used to be written into the template."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_seeder_creates_every_section_page(self):
        for section in SECTION_PAGES:
            page = Page.objects.filter(path=section.path).first()
            self.assertIsNotNone(page, "no Page for " + section.path)
            self.assertTrue(page.is_section_page, section.path)

    def test_built_in_wording_is_used_when_no_page_exists(self):
        Page.objects.filter(is_section_page=True).delete()
        response = self.client.get(reverse("core:programs"))
        self.assertContains(response, escape("Our Programs"))

    def test_editing_the_page_changes_the_heading(self):
        page = Page.objects.get(path="our-programs")
        page.title = "Programmes That Reach"
        page.intro = "Rewritten by an editor."
        page.save()

        response = self.client.get(reverse("core:programs"))
        self.assertContains(response, escape("Programmes That Reach"))
        self.assertContains(response, escape("Rewritten by an editor."))

    def test_body_appears_below_the_heading(self):
        page = Page.objects.get(path="who-we-are/meet-our-team")
        page.body = "<p>An extra paragraph about how we hire.</p>"
        page.save()

        response = self.client.get(reverse("core:team"))
        self.assertContains(response, "An extra paragraph about how we hire.")

    def test_every_section_route_still_renders(self):
        for section in SECTION_PAGES:
            with self.subTest(path=section.path):
                response = self.client.get("/" + section.path + "/")
                self.assertEqual(response.status_code, 200)


class PublishingTests(TestCase):
    """Drafts are hidden from visitors and visible to staff."""

    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_draft_post_is_hidden_from_the_public(self):
        post = Post.objects.first()
        post.is_published = False
        post.save()

        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 404)
        listing = self.client.get(reverse("core:newsroom"))
        self.assertNotContains(listing, escape(post.title))

    def test_staff_can_still_open_a_draft(self):
        post = Post.objects.first()
        post.is_published = False
        post.save()

        User.objects.create_user("editor", password="hunter2-not-a-real-pw", is_staff=True)
        self.client.login(username="editor", password="hunter2-not-a-real-pw")

        self.assertEqual(self.client.get(post.get_absolute_url()).status_code, 200)

    def test_draft_page_is_hidden_from_the_public(self):
        page = Page.objects.filter(is_section_page=False).first()
        page.is_published = False
        page.save()

        self.assertEqual(self.client.get(page.get_absolute_url()).status_code, 404)

    def test_draft_page_is_absent_from_search(self):
        page = Page.objects.filter(is_section_page=False).first()
        page.is_published = False
        page.save()

        response = self.client.get(reverse("core:search"), {"q": page.title})
        # Checked against the result set rather than the rendered HTML: several
        # page titles are also navigation labels, so the words appear in the
        # header and footer of every response whatever the search returns.
        self.assertNotIn(page, response.context["results"]["pages"])


class GalleryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_content", verbosity=0)

    def test_caption_is_shown_for_an_attached_picture(self):
        page = Page.objects.filter(is_section_page=False).first()
        PageImage.objects.create(
            page=page, image="pages/gallery/example.jpg", caption="A clinic in Kono"
        )

        response = self.client.get(page.get_absolute_url())
        self.assertContains(response, "A clinic in Kono")


class EditorGroupTests(TestCase):
    def test_setup_cms_builds_a_group_that_cannot_touch_accounts(self):
        call_command("setup_cms", verbosity=0)
        group = Group.objects.get(name="Editors")

        codenames = set(group.permissions.values_list("codename", flat=True))
        self.assertIn("change_page", codenames)
        self.assertIn("add_post", codenames)
        self.assertIn("change_sitesettings", codenames)

        # The things an editor must not be able to do.
        self.assertNotIn("delete_sitesettings", codenames)
        self.assertNotIn("add_user", codenames)
        self.assertNotIn("change_user", codenames)
        self.assertNotIn("delete_user", codenames)
        self.assertNotIn("add_contactmessage", codenames)

    def test_setup_cms_is_repeatable(self):
        call_command("setup_cms", verbosity=0)
        first = Group.objects.get(name="Editors").permissions.count()
        call_command("setup_cms", verbosity=0)
        second = Group.objects.get(name="Editors").permissions.count()
        self.assertEqual(first, second)


class EditorUploadTests(TestCase):
    """The picture upload behind the rich text editor is staff-only."""

    def test_anonymous_upload_is_refused(self):
        response = self.client.post(reverse("ck_editor_5_upload_file"))
        self.assertEqual(response.status_code, 403)

    def test_upload_url_is_not_swallowed_by_the_flat_page_catch_all(self):
        # core.urls ends in a catch-all that matches "ckeditor5/image_upload/".
        # If it ever wins, uploads answer 404 instead of doing anything.
        match = resolve("/ckeditor5/image_upload/")
        self.assertEqual(match.url_name, "ck_editor_5_upload_file")
