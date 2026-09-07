"""Smoke tests for the REACHE Last-Mile site.

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
