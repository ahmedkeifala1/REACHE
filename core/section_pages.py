"""Editable headings for the pages behind a fixed route.

Ten pages -- "Our Programs", "Meet Our Team", "Ways to Give" and the rest -- are
served by their own view because they list something the admin cannot express as
prose. Their heading, eyebrow and introduction used to be written into the
template, which meant they were the only copy on the site an editor could not
change.

Each one now looks for a ``Page`` whose ``path`` matches its route. When that
row exists its wording wins; when it does not, the built-in text below is used,
so a database with no section pages in it renders exactly as before.

``seed_content`` creates the rows from this same list, which is why the defaults
live here rather than in the seeder: the seeder and the fallback can never drift
apart.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class SectionPage:
    """A fixed route and the wording it falls back to."""

    path: str
    title: str
    eyebrow: str
    intro: str
    crumbs: str


SECTION_PAGES = (
    SectionPage(
        "what-we-do",
        "What We Do",
        "Our Work",
        "The seven pillars of the REACH 360 Framework. Each addresses one WHO "
        "health system building block, carries a Sierra Leone-original "
        "contribution, and fails without the other six.",
        "What We Do",
    ),
    SectionPage(
        "our-programs",
        "Our Programs",
        "Our Programs",
        "Programmes that carry care across the whole of life, from a healthy "
        "pregnancy to a resilient community.",
        "Our Programs",
    ),
    SectionPage(
        "where-we-work",
        "Locally Driven. Globally Connected.",
        "Where We Work",
        "Our experts live and work where the work happens, combining deep local "
        "knowledge with global perspective.",
        "Where We Work",
    ),
    SectionPage(
        "who-we-are/meet-our-team",
        "Meet Our Team",
        "Who We Are",
        "The people designing, delivering and sustaining last-mile health care.",
        "Who We Are",
    ),
    SectionPage(
        "who-we-are/our-partners",
        "Our Partners & Coalitions",
        "Who We Are",
        "We work through radical collaboration. These are the institutions "
        "building last-mile health care with us.",
        "Who We Are",
    ),
    SectionPage(
        "our-impact/newsroom",
        "Newsroom & Blog",
        "Our Impact",
        "Press, field stories and updates from across our programmes.",
        "Our Impact",
    ),
    SectionPage(
        "our-impact/resources",
        "Resources",
        "Our Impact",
        "Reports, evidence briefs and tools from our programmes and research.",
        "Our Impact",
    ),
    SectionPage(
        "get-involved/work-for-us",
        "Work for Us",
        "Get Involved",
        "Join a team that builds health systems people can rely on.",
        "Get Involved",
    ),
    SectionPage(
        "get-involved/contact-us",
        "Contact Us",
        "Get Involved",
        "Questions, partnership ideas or media enquiries: we would like to hear "
        "from you.",
        "Get Involved",
    ),
    SectionPage(
        "get-involved/donate",
        "Ways to Give",
        "Get Involved",
        "Your contribution helps increase the availability of health care for the "
        "most under-reached communities.",
        "Get Involved",
    ),
)

SECTION_PAGES_BY_PATH = {section.path: section for section in SECTION_PAGES}


def hero(path, user=None):
    """Build the hero context for the fixed route at ``path``.

    Returns a dict the templates hand to ``partials/page_hero.html``, plus the
    ``Page`` itself so a template can render its body and gallery. Every field
    falls back to the built-in wording, so a blank intro in the admin shows the
    original sentence rather than an empty space -- clearing a field is not how
    an editor removes it, and a page with no heading would be a worse outcome
    than one an editor has to overwrite.
    """
    from .models import Page

    default = SECTION_PAGES_BY_PATH[path]
    page = (
        Page.objects.filter(path=path, is_section_page=True)
        .prefetch_related("gallery")
        .first()
    )
    if page is not None and not page.is_published and not getattr(user, "is_staff", False):
        page = None

    return {
        "title": (page.title if page and page.title else default.title),
        "eyebrow": (page.section if page and page.section else default.eyebrow),
        "text": (page.intro if page and page.intro else default.intro),
        "image": (page.hero_image_url if page else ""),
        "crumbs": default.crumbs,
        "page": page,
    }
