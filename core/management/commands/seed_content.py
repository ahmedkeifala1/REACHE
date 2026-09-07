"""Populates the site with its navigation and starter content.

Run with:  python manage.py seed_content
The command is idempotent - it updates rather than duplicates on re-run.
"""

import datetime

from django.core.management.base import BaseCommand
from django.utils.text import slugify

from core.models import (
    FocusArea,
    Job,
    Location,
    MenuItem,
    Page,
    Partner,
    Post,
    PostCategory,
    Program,
    Resource,
    SiteSettings,
    Stat,
    TeamMember,
)
from core.section_pages import SECTION_PAGES

# --------------------------------------------------------------- navigation
# Mirrors the structure in organogram.jpeg.
MENU = [
    (
        "Who We Are",
        "/who-we-are/",
        [
            ("Mission, Vision & Values", "/who-we-are/mission-vision-values/"),
            ("Our Approach", "/who-we-are/our-approach/"),
            ("Our Strategy", "/who-we-are/our-strategy/"),
            ("Meet Our Team", "/who-we-are/meet-our-team/"),
            ("Founding Story", "/who-we-are/founding-story/"),
            ("Our Partners & Coalitions", "/who-we-are/our-partners/"),
            ("Strategy 2030", "/who-we-are/strategy-2030/"),
        ],
    ),
    (
        "What We Do",
        "/what-we-do/",
        [
            (
                "Proactive Community Health Service Delivery",
                "/what-we-do/proactive-community-health-service-delivery/",
            ),
            (
                "Connected Health Workforce Strengthening",
                "/what-we-do/connected-health-workforce-strengthening/",
            ),
            (
                "Community Intelligence & Surveillance Systems",
                "/what-we-do/community-intelligence-surveillance-systems/",
            ),
            (
                "Last-Mile Supply Chain and Community Access",
                "/what-we-do/last-mile-supply-chain-and-community-access/",
            ),
            (
                "Sustainable Health Financing and Domestic Resource Mobilization",
                "/what-we-do/sustainable-health-financing-and-domestic-resource-mobilization/",
            ),
            (
                "Three Authority Community Government and Accountability",
                "/what-we-do/three-authority-community-government-and-accountability/",
            ),
            (
                "Drive Sustained Impact Through Strategic Partnership",
                "/what-we-do/drive-sustained-impact-through-strategic-partnership/",
            ),
        ],
    ),
    ("Where We Work", "/where-we-work/", [("Sierra Leone", "/where-we-work/sierra-leone/")]),
    (
        "Our Programs",
        "/our-programs/",
        [
            (
                "Healthy Pregnancies and Newborn Health",
                "/our-programs/healthy-pregnancies-and-newborn-health/",
            ),
            ("Defeating Childhood Diseases", "/our-programs/defeating-childhood-diseases/"),
            ("Sexual and Reproductive Health", "/our-programs/sexual-and-reproductive-health/"),
            (
                "Immunization and Zero Dose Reduction",
                "/our-programs/immunization-and-zero-dose-reduction/",
            ),
            ("Climate and Health Resilience", "/our-programs/climate-and-health-resilience/"),
            (
                "Emergency Preparedness and Outbreak Response",
                "/our-programs/emergency-preparedness-and-outbreak-response/",
            ),
            ("Health and Nutrition", "/our-programs/health-and-nutrition/"),
        ],
    ),
    (
        "Our Model",
        "/our-model/",
        [
            ("The Challenge", "/our-model/the-challenge/"),
            ("BRIDGE 360", "/our-model/bridge-360/"),
            ("LASTMILE CARE", "/our-model/lastmile-care/"),
        ],
    ),
    ("Research", "/research/", []),
    (
        "Our Impact",
        "/our-impact/",
        [
            ("History & Achievements", "/our-impact/history/"),
            ("Governance & Financials", "/our-impact/governance-and-financials/"),
            ("Resources", "/our-impact/resources/"),
            ("Newsroom", "/our-impact/newsroom/"),
        ],
    ),
    (
        "Get Involved",
        "/get-involved/",
        [
            ("Ways to Give", "/get-involved/donate/"),
            ("Work for Us", "/get-involved/work-for-us/"),
            ("Contact Us", "/get-involved/contact-us/"),
        ],
    ),
]

# ------------------------------------------------------------- focus areas
FOCUS_AREAS = [
    (
        "Proactive Community Health Service Delivery",
        "service",
        "Extending services beyond the health facility so that care finds households "
        "before illness becomes an emergency, through routine community outreach and "
        "proactive case finding.",
    ),
    (
        "Connected Health Workforce Strengthening",
        "workforce",
        "Strengthening the health workforce by supporting a paid, professionalised and "
        "digitally connected cadre of community health workers with supervision they can "
        "rely on.",
    ),
    (
        "Community Intelligence & Surveillance Systems",
        "data",
        "Designing and integrating data systems that help governments and health workers "
        "use information from the community level to act early and allocate resources "
        "where they matter.",
    ),
    (
        "Last-Mile Supply Chain and Community Access",
        "supply",
        "Getting health products to people when and where they are needed, in ways that "
        "are convenient, affordable and resilient to the shocks that break conventional "
        "supply chains.",
    ),
    (
        "Sustainable Health Financing and Domestic Resource Mobilization",
        "financing",
        "Working with governments and the private sector to build financing frameworks "
        "and mechanisms that keep primary health care funded beyond the life of any "
        "single grant.",
    ),
    (
        "Three Authority Community Government and Accountability",
        "accountability",
        "Aligning community, government and health system authority around shared targets "
        "so that accountability for last-mile results is mutual, visible and sustained.",
    ),
    (
        "Drive Sustained Impact Through Strategic Partnership",
        "partnership",
        "Collaborating with governments, partners, stakeholders and communities to develop "
        "strategies and innovative mechanisms that strengthen health systems for the long "
        "term.",
    ),
]

# ---------------------------------------------------------------- programs
PROGRAMS = [
    (
        "Healthy Pregnancies and Newborn Health",
        "Accompanying women from first antenatal contact through safe delivery and the "
        "critical first month of a newborn's life.",
    ),
    (
        "Defeating Childhood Diseases",
        "Bringing prevention, diagnosis and treatment for malaria, pneumonia and diarrhoeal "
        "disease within reach of every household.",
    ),
    (
        "Sexual and Reproductive Health",
        "Supporting informed choice, contraceptive access and respectful care for adolescents "
        "and adults alike.",
    ),
    (
        "Immunization and Zero Dose Reduction",
        "Finding and protecting the children who have never received a single vaccine, and "
        "keeping the cold chain that serves them running.",
    ),
    (
        "Climate and Health Resilience",
        "Preparing health facilities and communities for floods, heat and the shifting disease "
        "patterns that follow a changing climate.",
    ),
    (
        "Emergency Preparedness and Outbreak Response",
        "Building the surveillance, stockpiles and trained responders that let communities "
        "detect and contain outbreaks early.",
    ),
    (
        "Health and Nutrition",
        "Screening, treating and preventing malnutrition as an integrated part of routine "
        "primary health care.",
    ),
]

# ---------------------------------------------------------------- content
STATS = [
    ("2,400,000", "people have increased access to quality primary health care."),
    ("8,500", "health workers supported to deliver products and quality health services."),
    ("640", "health facilities received and sent deliveries of health products through our programs."),
]

POSTS = [
    (
        "Reaching the Last Mile: What Changes When Care Comes to the Household",
        "Field Story",
        "Proactive community health service delivery turns a monthly clinic visit into a "
        "continuous relationship between a household and its health system.",
        True,
        "Field Story",
    ),
    (
        "Keeping the Cold Chain Cold: Preventive Maintenance That Actually Happens",
        "Program Update",
        "A vaccine refrigerator that fails quietly can undo a year of outreach. Here is how "
        "routine preventive maintenance changed the picture.",
        True,
        "Program Update",
    ),
    (
        "Community Surveillance in Practice: Acting on Signals Early",
        "Research",
        "When community health workers report what they see, districts can respond in days "
        "rather than weeks.",
        True,
        "Research",
    ),
    (
        "Financing Primary Health Care Beyond the Grant Cycle",
        "Opinion",
        "Domestic resource mobilisation is not a fundraising exercise. It is the difference "
        "between a pilot and a health system.",
        True,
        "Opinion",
    ),
    (
        "Zero-Dose Children Are Not Hard to Reach. They Are Under-Reached.",
        "Opinion",
        "The distinction matters, because it changes where the responsibility for reaching "
        "them sits.",
        True,
        "Perspective",
    ),
    (
        "A Midwife's Patience: One Family Planning Conversation at a Time",
        "Field Story",
        "Informed choice is built through repeated, unhurried conversation, not a single "
        "counselling session.",
        False,
        "",
    ),
    (
        "Training Traditional Healers as Partners, Not Competitors",
        "Field Story",
        "Collaboration with trusted community figures is helping families seek timely care.",
        False,
        "",
    ),
    (
        "When Learning Travels: Turning Peer Exchange Into Action",
        "Program Update",
        "District teams that visit one another adopt improvements faster than those that read "
        "about them.",
        False,
        "",
    ),
    (
        "Nutrition Screening at Every Contact",
        "Program Update",
        "Integrating growth monitoring into routine visits catches malnutrition before it "
        "becomes severe.",
        False,
        "",
    ),
    (
        "Climate Shocks and the Health Facilities That Absorb Them",
        "Research",
        "Flooding does not only damage buildings. It disrupts the supply routes that facilities "
        "depend on.",
        False,
        "",
    ),
    (
        "Building an Outbreak Response That Communities Trust",
        "Opinion",
        "In an outbreak, information needs to move quickly. So does trust.",
        False,
        "",
    ),
    (
        "The Three Authorities: Aligning Community, Government and Health System",
        "Research",
        "Shared targets only work when all three authorities recognise the same numbers.",
        False,
        "",
    ),
]

PAGES = [
    (
        "who-we-are",
        "Who We Are",
        "Who We Are",
        "We are a last-mile health organisation working to make primary health care "
        "reliable for the communities furthest from it.",
        """
        <p>REACHE Last-Mile exists to close the distance between health systems and the
        people they are meant to serve. We work at the point where supply chains end,
        where road networks thin out, and where a missed delivery becomes a missed
        childhood vaccination.</p>
        <h2>What guides us</h2>
        <p>Our work is built with government rather than beside it. We design for the
        systems that will still be running after a programme closes, and we measure
        ourselves on whether local institutions can carry the work forward.</p>
        <blockquote>The distance between a health product and the person who needs it
        should never decide whether they live.</blockquote>
        <h2>Explore</h2>
        <ul>
          <li><a href="/who-we-are/mission-vision-values/">Mission, Vision &amp; Values</a></li>
          <li><a href="/who-we-are/our-approach/">Our Approach</a></li>
          <li><a href="/who-we-are/our-strategy/">Our Strategy</a></li>
          <li><a href="/who-we-are/meet-our-team/">Meet Our Team</a></li>
          <li><a href="/who-we-are/founding-story/">Founding Story</a></li>
          <li><a href="/who-we-are/our-partners/">Our Partners &amp; Coalitions</a></li>
          <li><a href="/who-we-are/strategy-2030/">Strategy 2030</a></li>
        </ul>
        """,
    ),
    (
        "who-we-are/mission-vision-values",
        "Mission, Vision & Values",
        "Who We Are",
        "Innovation for Rural Empowerment in Access to Community Health and Equity.",
        """
        <h2>Our Mission</h2>
        <p>To transform health care delivery so that quality primary health care reaches
        every household, including those the system reaches last.</p>
        <h2>Our Vision</h2>
        <p>A future in which where a person lives no longer determines whether they
        survive a preventable illness.</p>
        <h2>Our Values</h2>
        <ul>
          <li><strong>Equity first.</strong> We start with the communities that are reached last.</li>
          <li><strong>Radical collaboration.</strong> We build with government, communities and partners.</li>
          <li><strong>Evidence in the open.</strong> We publish what works and what does not.</li>
          <li><strong>Local leadership.</strong> Decisions belong closest to the people affected by them.</li>
          <li><strong>Durability.</strong> We design for what remains after we leave.</li>
        </ul>
        """,
    ),
    (
        "who-we-are/our-approach",
        "Our Approach",
        "Who We Are",
        "Designing responsive primary health care around the realities of the last mile.",
        """
        <p>We begin every engagement by mapping the actual conditions of the last mile:
        the roads, the stock-outs, the staffing gaps and the trust deficits. Only then do
        we design.</p>
        <h2>How we work</h2>
        <ul>
          <li><strong>Diagnose with the community.</strong> Local health workers define the problem with us.</li>
          <li><strong>Design with government.</strong> Solutions sit inside national systems from day one.</li>
          <li><strong>Test in the hardest place.</strong> If it works at the last mile, it works everywhere.</li>
          <li><strong>Hand over deliberately.</strong> Capability transfer is a work stream, not an afterthought.</li>
        </ul>
        """,
    ),
    (
        "who-we-are/our-strategy",
        "Our Strategy",
        "Who We Are",
        "Concentrating our effort where the gap between need and access is widest.",
        """
        <p>Our strategy directs resources towards the communities where the distance
        between need and access is greatest, and towards the system changes that close
        that distance permanently.</p>
        <h2>Strategic priorities</h2>
        <ol>
          <li>Make community health service delivery proactive rather than reactive.</li>
          <li>Professionalise and connect the community health workforce.</li>
          <li>Put timely community data in the hands of decision makers.</li>
          <li>Build supply chains that hold under stress.</li>
          <li>Secure domestic financing for primary health care.</li>
        </ol>
        """,
    ),
    (
        "who-we-are/founding-story",
        "Founding Story",
        "Who We Are",
        "How REACHE Last-Mile began, and what has not changed since.",
        """
        <p>REACHE Last-Mile grew out of a simple observation repeated in too many
        villages: the medicine existed, the health worker existed, and still the child
        went untreated. What was missing was the connection between them.</p>
        <p>What began as a bridge between communities and the health system has become a
        model for last-mile care, built on the conviction that reaching the final
        household is a design problem with a solvable answer.</p>
        """,
    ),
    (
        "who-we-are/strategy-2030",
        "Strategy 2030",
        "Who We Are",
        "Our commitments for the decade ahead.",
        """
        <p>By 2030 we intend to have helped establish last-mile primary health care as a
        funded, staffed and measured part of the national health system in every country
        where we work.</p>
        <h2>Our 2030 commitments</h2>
        <ul>
          <li>Every community we serve has a paid, supervised and equipped health worker.</li>
          <li>Community-level data reaches district decision makers within a week.</li>
          <li>Domestic financing covers the majority of recurrent last-mile costs.</li>
          <li>Zero-dose children are identified and reached within a single planning cycle.</li>
        </ul>
        """,
    ),
    (
        "our-model",
        "Our Model",
        "Our Model",
        "The challenge we address, and the two frameworks we use to address it.",
        """
        <p>Our model has three parts: a clear statement of the challenge, the BRIDGE 360
        framework that structures how we engage, and LASTMILE CARE, the delivery model
        that puts it into practice.</p>
        <ul>
          <li><a href="/our-model/the-challenge/">The Challenge</a></li>
          <li><a href="/our-model/bridge-360/">BRIDGE 360</a></li>
          <li><a href="/our-model/lastmile-care/">LASTMILE CARE</a></li>
        </ul>
        """,
    ),
    (
        "our-model/the-challenge",
        "The Challenge",
        "Our Model",
        "Availability is not access. The last mile is where that difference is decided.",
        """
        <p>Health systems are commonly measured on what they stock and staff. Communities
        experience them by what actually arrives. Between those two measures sits the last
        mile, and most system failures are concentrated there.</p>
        <h2>Where systems break</h2>
        <ul>
          <li>Products reach the district store but not the facility.</li>
          <li>Health workers are trained but unpaid, unsupervised or unequipped.</li>
          <li>Data arrives too late to change a decision.</li>
          <li>Communities are consulted after design rather than during it.</li>
        </ul>
        """,
    ),
    (
        "our-model/bridge-360",
        "BRIDGE 360",
        "Our Model",
        "A full-circle framework for connecting community, facility and government.",
        """
        <p>BRIDGE 360 is how we structure an engagement so that no part of the chain is
        strengthened in isolation. It looks at the whole circuit - household, community
        health worker, facility, district and national system - and improves it as one.</p>
        <h2>The circuit</h2>
        <ol>
          <li><strong>Baseline</strong> the real conditions at the last mile.</li>
          <li><strong>Reach</strong> households proactively rather than waiting for them.</li>
          <li><strong>Integrate</strong> community data into district decision making.</li>
          <li><strong>Deliver</strong> products through routes designed for the terrain.</li>
          <li><strong>Govern</strong> through shared accountability across the three authorities.</li>
          <li><strong>Endure</strong> by securing financing and capability that outlast us.</li>
        </ol>
        """,
    ),
    (
        "our-model/lastmile-care",
        "LASTMILE CARE",
        "Our Model",
        "The delivery model that carries BRIDGE 360 into daily practice.",
        """
        <p>LASTMILE CARE is the operational side of our model: the routines, tools and
        supervision structures that a community health worker uses every week.</p>
        <h2>In practice</h2>
        <ul>
          <li>Scheduled household visits rather than opportunistic contact.</li>
          <li>A single register that serves both care and surveillance.</li>
          <li>Supervision visits with a defined checklist and a feedback loop.</li>
          <li>Resupply triggered by consumption data, not by calendar.</li>
        </ul>
        """,
    ),
    (
        "research",
        "Research",
        "Research",
        "Evidence generated with communities, published for everyone.",
        """
        <p>We treat research as part of delivery rather than a parallel activity. Our
        studies are designed with the districts that will use the findings, and we publish
        results whether or not they favour our approach.</p>
        <h2>Current research areas</h2>
        <ul>
          <li>Effectiveness of proactive versus reactive community case finding.</li>
          <li>Cost per zero-dose child reached across delivery models.</li>
          <li>Cold-chain reliability under preventive maintenance regimes.</li>
          <li>Community surveillance signal quality and district response time.</li>
        </ul>
        <p>Published outputs are listed under <a href="/our-impact/resources/">Resources</a>.</p>
        """,
    ),
    (
        "our-impact",
        "Our Impact",
        "Our Impact",
        "What has changed, how we govern, and what we have published.",
        """
        <p>We report on our impact in three ways: the history of what we have achieved, the
        governance and financial record behind it, and the evidence we publish.</p>
        <ul>
          <li><a href="/our-impact/history/">History &amp; Achievements</a></li>
          <li><a href="/our-impact/governance-and-financials/">Governance &amp; Financials</a></li>
          <li><a href="/our-impact/resources/">Resources</a></li>
          <li><a href="/our-impact/newsroom/">Newsroom</a></li>
        </ul>
        """,
    ),
    (
        "our-impact/history",
        "History & Achievements",
        "Our Impact",
        "A record of what we have built, with whom, and what it changed.",
        """
        <p>Our history is best read as a sequence of handovers: each programme designed so
        that a local institution could carry it forward.</p>
        <h2>Milestones</h2>
        <ul>
          <li>Established proactive community health delivery in our first districts.</li>
          <li>Introduced preventive maintenance routines across the vaccine cold chain.</li>
          <li>Connected community-level reporting to district planning cycles.</li>
          <li>Secured the first domestic financing commitments for last-mile delivery.</li>
        </ul>
        """,
    ),
    (
        "our-impact/governance-and-financials",
        "Governance & Financials",
        "Our Impact",
        "How we are governed and how our funds are used.",
        """
        <h2>Governance</h2>
        <p>REACHE Last-Mile is governed by a board that oversees strategy, risk and
        financial stewardship, supported by an audit and finance committee.</p>
        <h2>Financial reporting</h2>
        <p>We publish annual financial statements and an independent audit. Programme
        expenditure, administration and fundraising costs are reported separately.</p>
        <p>Current statements are available under
        <a href="/our-impact/resources/">Resources</a>.</p>
        """,
    ),
    (
        "get-involved",
        "Get Involved",
        "Get Involved",
        "Give, join us, or start a conversation.",
        """
        <p>There is more than one way to support last-mile health care.</p>
        <ul>
          <li><a href="/get-involved/donate/">Ways to Give</a></li>
          <li><a href="/get-involved/work-for-us/">Work for Us</a></li>
          <li><a href="/get-involved/contact-us/">Contact Us</a></li>
        </ul>
        """,
    ),
    (
        "privacy-policy",
        "Privacy Policy",
        "Legal",
        "How we handle the personal information you share with us.",
        """
        <p>We collect personal information only when you choose to give it to us, such as
        when you subscribe to our newsletter or send us a message.</p>
        <h2>What we collect</h2>
        <ul>
          <li>Contact details you submit through forms on this site.</li>
          <li>Basic, non-identifying analytics about how the site is used.</li>
        </ul>
        <h2>How we use it</h2>
        <p>We use your details to respond to you and, where you have opted in, to send
        periodic updates. We do not sell personal information.</p>
        <h2>Your choices</h2>
        <p>You can unsubscribe at any time, or ask us to delete your details by writing to
        the address on our <a href="/get-involved/contact-us/">contact page</a>.</p>
        """,
    ),
    (
        "photo-policy",
        "Photo Policy",
        "Legal",
        "How we photograph, caption and use images of the people we work with.",
        """
        <p>The people in our photographs are partners in our work, not illustrations of
        need. Our practice reflects that.</p>
        <h2>Our commitments</h2>
        <ul>
          <li>We obtain informed consent before photographing anyone.</li>
          <li>We name people where they wish to be named.</li>
          <li>We do not use images that portray people without dignity.</li>
          <li>We honour requests to withdraw an image at any time.</li>
        </ul>
        """,
    ),
]

TEAM = [
    ("Executive Director", True),
    ("Director of Programs", True),
    ("Director of Finance & Operations", True),
    ("Head of Research & Learning", True),
    ("Community Health Systems Lead", False),
    ("Supply Chain Manager", False),
    ("Monitoring & Evaluation Officer", False),
    ("Communications Officer", False),
]


class Command(BaseCommand):
    help = "Seed the REACHE site with navigation and starter content."

    def handle(self, *args, **options):
        self.seed_settings()
        self.seed_menu()
        self.seed_focus_areas()
        self.seed_programs()
        self.seed_locations()
        self.seed_stats()
        self.seed_pages()
        self.seed_section_pages()
        self.seed_posts()
        self.seed_team()
        self.seed_partners()
        self.seed_resources()
        self.seed_jobs()
        self.stdout.write(self.style.SUCCESS("Seed complete."))

    # ------------------------------------------------------------- helpers
    def seed_settings(self):
        settings_obj = SiteSettings.load()
        settings_obj.linkedin = settings_obj.linkedin or "https://www.linkedin.com/"
        settings_obj.facebook = settings_obj.facebook or "https://www.facebook.com/"
        settings_obj.save()
        self.stdout.write("  site settings")

    def seed_menu(self):
        MenuItem.objects.all().delete()
        for index, (title, url, children) in enumerate(MENU):
            parent = MenuItem.objects.create(title=title, url=url, order=index)
            for child_index, (child_title, child_url) in enumerate(children):
                MenuItem.objects.create(
                    title=child_title, url=child_url, parent=parent, order=child_index
                )
        MenuItem.objects.create(
            title="Donate", url="/get-involved/donate/", order=99, is_button=True
        )
        self.stdout.write("  navigation")

    def seed_focus_areas(self):
        for index, (title, icon, summary) in enumerate(FOCUS_AREAS):
            FocusArea.objects.update_or_create(
                slug=slugify(title)[:160],
                defaults={
                    "title": title,
                    "icon": icon,
                    "summary": summary,
                    "order": index,
                },
            )
        self.stdout.write("  focus areas")

    def seed_programs(self):
        for index, (title, summary) in enumerate(PROGRAMS):
            Program.objects.update_or_create(
                slug=slugify(title)[:180],
                defaults={
                    "title": title,
                    "summary": summary,
                    "body": "<p>{0}</p>".format(summary),
                    "order": index,
                },
            )
        self.stdout.write("  programs")

    def seed_locations(self):
        Location.objects.update_or_create(
            slug="sierra-leone",
            defaults={
                "name": "Sierra Leone",
                "summary": "Our home programme, working with district health management "
                "teams to make last-mile primary health care routine.",
                "body": "<p>Sierra Leone is where our model was built and where it is "
                "tested hardest. We work alongside district health management teams to "
                "extend proactive community health service delivery, strengthen the "
                "community health workforce and keep the supply chain running to the "
                "final facility.</p>",
                "is_office": True,
                "order": 0,
            },
        )
        self.stdout.write("  locations")

    def seed_stats(self):
        for index, (value, label) in enumerate(STATS):
            Stat.objects.update_or_create(
                value=value, defaults={"label": label, "order": index}
            )
        self.stdout.write("  stats")

    def seed_pages(self):
        for path, title, section, intro, body in PAGES:
            Page.objects.update_or_create(
                path=path,
                defaults={
                    "title": title,
                    "section": section,
                    "intro": intro,
                    "body": body.strip(),
                },
            )
        self.stdout.write("  pages")

    def seed_section_pages(self):
        """Create the editable rows behind the fixed routes.

        Unlike everything else here this uses get_or_create, not
        update_or_create: these rows exist so an editor can rewrite the heading
        of "Our Programs" or "Ways to Give", and re-running the seeder must not
        undo that. Deleting a row in the admin is what resets one, and even that
        only restores the built-in wording from core/section_pages.py.
        """
        created = 0
        for section in SECTION_PAGES:
            _, was_created = Page.objects.get_or_create(
                path=section.path,
                defaults={
                    "title": section.title,
                    "section": section.eyebrow,
                    "intro": section.intro,
                    "is_section_page": True,
                    "show_newsletter": False,
                },
            )
            created += was_created
        self.stdout.write("  section landing pages ({0} new)".format(created))

    def seed_posts(self):
        today = datetime.date.today()
        for index, (title, category_name, excerpt, featured, kicker) in enumerate(POSTS):
            category, _ = PostCategory.objects.get_or_create(
                slug=slugify(category_name), defaults={"name": category_name}
            )
            Post.objects.update_or_create(
                slug=slugify(title)[:255],
                defaults={
                    "title": title,
                    "category": category,
                    "excerpt": excerpt,
                    "body": "<p>{0}</p><p>Full article content can be edited from the "
                    "Django admin.</p>".format(excerpt),
                    "published": today - datetime.timedelta(days=index * 6),
                    "is_featured": featured,
                    "featured_kicker": kicker,
                },
            )
        self.stdout.write("  posts")

    def seed_team(self):
        for index, (role, is_leadership) in enumerate(TEAM):
            TeamMember.objects.update_or_create(
                name="Team Member {0}".format(index + 1),
                defaults={
                    "role": role,
                    "is_leadership": is_leadership,
                    "order": index,
                    "bio": "Biography to be added from the Django admin.",
                },
            )
        self.stdout.write("  team")

    def seed_partners(self):
        names = [
            "Ministry of Health",
            "District Health Management Teams",
            "Community Health Worker Networks",
            "Gavi, the Vaccine Alliance",
            "World Health Organization",
            "UNICEF",
            "Academic Research Partners",
            "Local Government Councils",
        ]
        for index, name in enumerate(names):
            Partner.objects.update_or_create(name=name, defaults={"order": index})
        self.stdout.write("  partners")

    def seed_resources(self):
        items = [
            ("Annual Impact Report", "Report", "Our yearly account of what changed and what it cost."),
            ("Last-Mile Supply Chain Brief", "Brief", "How we design delivery routes for the final facility."),
            ("Community Surveillance Evidence Note", "Evidence Note", "Signal quality and district response time."),
            ("Financial Statements", "Financials", "Audited statements and expenditure breakdown."),
        ]
        for title, kind, description in items:
            Resource.objects.update_or_create(
                title=title,
                defaults={"resource_type": kind, "description": description},
            )
        self.stdout.write("  resources")

    def seed_jobs(self):
        items = [
            (
                "Community Health Systems Advisor",
                "Support district teams to embed proactive community health service "
                "delivery into routine practice.",
            ),
            (
                "Supply Chain Officer",
                "Plan and monitor last-mile delivery routes and cold-chain performance.",
            ),
            (
                "Monitoring, Evaluation and Learning Officer",
                "Build the data flow from community register to district decision.",
            ),
        ]
        for title, description in items:
            Job.objects.update_or_create(
                slug=slugify(title)[:200],
                defaults={"title": title, "description": description},
            )
        self.stdout.write("  jobs")
