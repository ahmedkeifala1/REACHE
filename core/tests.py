"""Smoke tests for the REACHE Last-Mile site.

The suite seeds the site once per class with the same management command the
project ships with, then walks the navigation the way a visitor would.
"""

import re

from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape

from .models import (
    ContactMessage,
    FocusArea,
    Location,
    MenuItem,
    NewsletterSignup,
    Page,
    Post,
    Program,
)


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
