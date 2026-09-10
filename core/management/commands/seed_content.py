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
            ("Connected Health Workforce", "/what-we-do/connected-health-workforce/"),
            (
                "Community Intelligence and Surveillance System",
                "/what-we-do/community-intelligence-and-surveillance-system/",
            ),
            (
                "Last-Mile Supply Chain and Commodity Access",
                "/what-we-do/last-mile-supply-chain-and-commodity-access/",
            ),
            (
                "Sustainable Health Financing and Domestic Resource Mobilisation",
                "/what-we-do/sustainable-health-financing-and-domestic-resource-mobilisation/",
            ),
            (
                "Three-Authority Community Governance and Accountability",
                "/what-we-do/three-authority-community-governance-and-accountability/",
            ),
            (
                "Proactive Community Health Service Delivery",
                "/what-we-do/proactive-community-health-service-delivery/",
            ),
            (
                "Driving Sustained Impact Through Strategic Partnerships",
                "/what-we-do/driving-sustained-impact-through-strategic-partnerships/",
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
            ("BRIDGE 360° LASTMILE CARE", "/our-model/bridge-360/"),
            ("LASTMILE CARE in Sierra Leone", "/our-model/lastmile-care/"),
            ("The ProcCHW Cadre", "/our-model/procchw/"),
        ],
    ),
    (
        "REACH 360°",
        "/reach-360/",
        [
            ("The Framework", "/reach-360/"),
            ("The Three-Systems Connection Theory", "/reach-360/three-systems/"),
            ("The Four Constitutional Foundations", "/reach-360/foundations/"),
            ("Intelligent Digital Health Systems", "/reach-360/idhs/"),
            ("The Connection Quality Index", "/reach-360/connection-quality-index/"),
            ("The Seven Pillars", "/what-we-do/"),
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
        "Connected Health Workforce",
        "workforce",
        "Pillar 1. Building the ProcCHW workforce that is the human infrastructure of the "
        "REACH 360° Framework — 6,800 Professional Connected Community Health Workers "
        "as a nationally connected network, every one of them supervised, compensated and "
        "career-pathed toward government employment.",
        """
        <p><strong>WHO building block:</strong> Health Workforce</p>
        <p>The Connected Health Workforce pillar builds, connects, supports and
        continuously develops the ProcCHW workforce. It draws its primary evidence base
        from Living Goods' 2013 Uganda randomised controlled trial, which showed that
        structured supervision — not training, equipment or compensation alone — drives
        a 27% reduction in under-five mortality. Every design decision in this pillar is
        made against that finding: supervision is the lever.</p>
        <h2>The four-tier supervision hierarchy</h2>
        <ol>
          <li><strong>Senior ProcCHW / Peer Leader</strong> — 1:8–10. Daily dashboard
          monitoring and a weekly mobile check-in; first-line peer support and
          connectivity verification.</li>
          <li><strong>ProcCHW Supervisor</strong> — 1:25–30. A monthly field visit built
          on the seven-step supervisory protocol, with competency assessment, performance
          verification and DHMT liaison.</li>
          <li><strong>District supervision</strong> — co-led with the District Health
          Management Team, which co-signs every ProcCHW appointment.</li>
          <li><strong>National quality assurance</strong> — standards, certification and
          the career pathway toward government payroll absorption.</li>
        </ol>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Predictive attrition modelling, personalised supervision agendas, payment
        integrity detection and career progression analytics — all configured inside the
        government platform, all designed for government operation by 2031.</p>
        """,
    ),
    (
        "Community Intelligence and Surveillance System",
        "data",
        "Pillar 2. Communities as the primary detection instrument — the post-Ebola "
        "epidemiological intelligence that Sierra Leonean communities already hold, "
        "formalised as a standing health system component, government-owned and connected "
        "to national surveillance in real time.",
        """
        <p><strong>WHO building block:</strong> Health Information Systems</p>
        <p>The Community Intelligence and Surveillance System makes the invisible visible.
        Sierra Leone's most current and most proximate health intelligence does not sit in
        DHIS2, in facility records or in any government database. It sits in communities
        — in the awareness of which households have sick children, in the detection of
        unusual illness patterns before they become outbreaks, in the knowledge of which
        families will never reach a facility without support.</p>
        <h2>The three CISS instruments</h2>
        <ul>
          <li><strong>The government CHW digital platform.</strong> All ProcCHW data
          capture happens inside Sierra Leone's national DHIS2 instance. The government
          owns the data from day one; DHMTs reach their district data through the
          dashboards they already use. We hold no exclusive data.</li>
          <li><strong>The Community Epidemiological Intelligence Network (CEIN).</strong>
          Community members trained in event recognition and escalation, governed by
          Community Health Committees, reporting into the national IDSR architecture
          within 48 hours of detection.</li>
          <li><strong>Krio language processing.</strong> Narrative reports in Krio and
          regional languages — intelligence that structured data fields currently lose
          — are read for signals rather than discarded.</li>
        </ul>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Outbreak signal detection inside DHIS2 IDSR, zero-dose prediction, and
        real-time surfacing of equity gaps. The AI layers are configured as DHIS2 program
        rule extensions, so no proprietary infrastructure is left behind when the
        programme ends.</p>
        """,
    ),
    (
        "Last-Mile Supply Chain and Commodity Access",
        "supply",
        "Pillar 3. ProcCHWs as demand signal generators — turning supply-push stockout "
        "cycles into demand-driven, predicted commodity flows that hold through the rainy "
        "season and reach communities the road does not.",
        """
        <p><strong>WHO building block:</strong> Access to Essential Medicines</p>
        <p>A ProcCHW who arrives at a household with an empty kit cannot deliver the care
        model, and community trust erodes faster after a visit that could not treat than
        after no visit at all. This pillar exists so that the commodity is there when the
        visit happens.</p>
        <h2>Optimize — Integrate — Sustain</h2>
        <ol>
          <li><strong>Optimize.</strong> Establish accurate, timely ProcCHW stock
          reporting first. Forecasting built on poor data amplifies errors rather than
          correcting them, so nothing is predicted until completeness passes 95% and
          accuracy 90% for three consecutive months.</li>
          <li><strong>Integrate.</strong> ProcCHW consumption data drives district
          resupply through eLMIS, 21-day demand forecasting comes online, Traditional
          Authority Supply Stewardship is activated in every programme chieftaincy, and
          the Rainy Season Route Optimisation begins.</li>
          <li><strong>Sustain.</strong> ProcCHW demand signals enter the national
          quantification cycle, DHMT supply managers operate the forecasting tools without
          iREACHE intermediation, and district budgets carry the logistics cost.</li>
        </ol>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Stockout prediction 21 days ahead, route optimisation for all 16 districts,
        expiry monitoring across 6,800 ProcCHW kits at once, and alerts to Traditional
        Authority Supply Stewards.</p>
        """,
    ),
    (
        "Sustainable Health Financing and Domestic Resource Mobilisation",
        "financing",
        "Pillar 4. Shared Sovereignty Financing — government, traditional authority and "
        "community as three co-equal financing advocates, working toward 70–80% domestic "
        "government financing by 2031.",
        """
        <p><strong>WHO building block:</strong> Health Financing</p>
        <p>Standard health financing frameworks treat domestic financing as a
        government–donor negotiation: a two-party discussion about reducing donor
        dependency over time. Shared Sovereignty Financing introduces a third sovereign
        party — traditional authority. A Paramount Chief advocating to a District Council
        for a ProcCHW budget line within their own chiefdom carries a political weight in
        that chamber that administrative advocacy does not.</p>
        <h2>Three financing tracks</h2>
        <ul>
          <li><strong>Government track.</strong> Annual cost-effectiveness briefs to
          Ministry of Health planning, costed CHW plans embedded in DHMT annual planning,
          and national budget line advocacy.</li>
          <li><strong>Parliament track.</strong> Engagement with the Parliamentary Health
          Committee and with MPs from the hardest-to-reach districts, showing the health
          consequence of the budget decision in front of them.</li>
          <li><strong>Chieftaincy track.</strong> Paramount Chiefs advocating directly to
          District Councils, using chieftaincy's constitutional standing in local
          government — supported by quarterly, plain-language summaries of what the care
          model achieved in their own chiefdom.</li>
        </ul>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Domestic financing scenario simulation, payment integrity checks, and
        chieftaincy health summaries written for chiefs rather than for health
        economists.</p>
        """,
    ),
    (
        "Three-Authority Community Governance and Accountability",
        "accountability",
        "Pillar 5. Traditional authority, government and community self-governance "
        "co-governing community health — each in the domain where its authority is most "
        "legitimate, each holding formal decision-making power rather than advisory "
        "rights.",
        """
        <p><strong>WHO building block:</strong> Leadership and Governance</p>
        <p>Sierra Leone's community health governance has always been a monologue — the
        government health system speaking at communities while ignoring the traditional
        authority structures that hold actual social legitimacy in them. This pillar
        formalises what Sierra Leone's governance reality requires: three authorities
        governing together, each accountable to the other two.</p>
        <h2>The three authorities</h2>
        <ul>
          <li><strong>Traditional authority</strong> holds social legitimacy, community
          enforcement capacity and embedded knowledge. Its domain: ProcCHW selection
          endorsement, supply stewardship, financing advocacy, and the social norms around
          care-seeking.</li>
          <li><strong>Government health authority</strong> holds legal authority,
          technical capacity and resource access. Its domain: co-leadership of all
          supervision, ownership of the data systems from day one, and the pathway to
          payroll absorption.</li>
          <li><strong>Community self-governance</strong> holds the legitimacy of lived
          experience. Its domain: community scorecards, CEIN governance, ProcCHW
          performance review, and resource allocation accountability.</li>
        </ul>
        <h2>The TRIAD Governance Protocol</h2>
        <p>In every programme district a document signed by the Paramount Chief or their
        representative, the DHMT District Medical Officer and the iREACHE LASTMILE
        District Coordinator specifies which decisions are made by which authority,
        through which process and within which timelines. It is what makes
        three-authority governance operationally real rather than rhetorical.</p>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Every digital tool must pass the TRIAD AI Test: intelligible to traditional
        authority, owned by government, and contestable by the community it affects.
        Community Health Committees receive quarterly plain-language reports and can
        formally contest any classification.</p>
        """,
    ),
    (
        "Proactive Community Health Service Delivery",
        "service",
        "Pillar 6. The monthly proactive rhythm that proves the system is alive — every "
        "registered household visited every month, whether or not anyone has reported "
        "illness, with an integrated seven-area service package at no cost.",
        """
        <p><strong>WHO building block:</strong> Service Delivery</p>
        <p>Muso Health's foundational evidence — that removing barriers to care rather
        than merely reducing them produces dramatically better equity outcomes — is the
        primary evidence base for this pillar. The barriers that stop sick people reaching
        care are always highest for the sickest and most vulnerable households. So the
        health system goes to the community before crises develop, rather than waiting for
        patients to navigate barriers at their most vulnerable.</p>
        <h2>The seven-area integrated service package</h2>
        <ul>
          <li>Maternal and newborn health — early pregnancy identification, ANC 4+
          facilitation, danger sign detection and emergency referral, birth planning, and
          postnatal home visits on days 1, 7 and 28.</li>
          <li>Childhood disease diagnosis and treatment (iCCM).</li>
          <li>Immunisation follow-up and zero-dose reduction.</li>
          <li>Nutrition screening.</li>
          <li>Sexual and reproductive health.</li>
          <li>Community disease surveillance.</li>
          <li>Climate and emergency health.</li>
        </ul>
        <p>All seven areas are delivered in a single visit, at no cost to the household.
        The Agricultural Calendar Alignment Protocol adjusts visit scheduling around each
        district's farming calendar, so that the weeks of peak agricultural labour —
        which women disproportionately carry — never become health access gaps.</p>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Danger sign recognition, MUAC trajectory analysis, obstetric emergency pattern
        detection, and a risk-stratified visit priority list so the highest-risk
        households are reached first — within a commitment that still visits every
        household every month. The ProcCHW's clinical judgment remains primary; alerts are
        suggestions, not prescriptions.</p>
        """,
    ),
    (
        "Driving Sustained Impact Through Strategic Partnerships",
        "partnership",
        "Pillar 7. Collaborating with government, the private sector, stakeholders and "
        "communities to develop the frameworks, strategies and mechanisms through which "
        "health systems change becomes self-reinforcing beyond any single programme.",
        """
        <p><strong>WHO building block:</strong> Cross-cutting — health systems
        strengthening</p>
        <p>This pillar takes its direct inspiration from VillageReach's foundational
        organisational principle, and names what separates a systems-building organisation
        from a programme implementation organisation: sustained investment in the
        ecosystem of partnerships, knowledge, policy influence and technical assistance
        through which change outlives a programme's geographic and temporal
        boundaries.</p>
        <p>It is an explicit recognition that our impact extends beyond our
        6,800 ProcCHWs and its 16 programme districts — through the evidence it
        generates, the capabilities it transfers, the policies it influences, and the
        knowledge it contributes to the global community health field.</p>
        <h2>The Community Health Systems Innovation and Learning Centre</h2>
        <p>Sierra Leone's post-Ebola community health intelligence has something to teach
        the world. The Learning Centre is where that teaching is organised: open-access
        Learning Briefs, peer-reviewed publication of implementation experience including
        its failures, and technical assistance to others adapting the framework.</p>
        <h2>Intelligent Digital Health Systems Integration</h2>
        <p>Knowledge management, policy simulation for advocacy, and literature synthesis
        supporting the Learning Briefs.</p>
        """,
    ),
]

# Focus area slugs superseded when the seven pillars were aligned to the REACH 360
# Master Document. Removed on seed so the old rows do not linger behind the menu.
LEGACY_FOCUS_AREA_SLUGS = [
    "connected-health-workforce-strengthening",
    "community-intelligence-surveillance-systems",
    "last-mile-supply-chain-and-community-access",
    "sustainable-health-financing-and-domestic-resource-mobilization",
    "three-authority-community-government-and-accountability",
    "drive-sustained-impact-through-strategic-partnership",
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
# The four figures printed as cards inside the home page hero: the value, the
# sentence under it, and the short qualifier under that.
HERO_STATS = [
    ("6,800", "ProcCHWs across all 16 districts by 2031", "All districts"),
    ("4.5M", "People in underserved and zero-dose communities", "By 2031"),
    (
        "354",
        "Maternal deaths per 100,000 — the number we are here to change",
        "Target < 300",
    ),
    (
        "$1",
        "The cost to treat the infection that killed Mariama — 14 hours old",
        "Why we exist",
    ),
]

# The compact row across the angled green band: the same figures, fewer words.
BAND_STATS = [
    ("6,800", "ProcCHWs by 2031"),
    ("16", "Districts"),
    ("4.5M", "People reached"),
    ("354→300", "MMR target"),
    ("$1", "Cost of Mariama's cure"),
]

# Stat values carried by earlier content, deleted on seed. The first three are
# the pre-framework placeholders; the last is the domestic financing figure the
# band carried before the document cut it down to the five figures above.
LEGACY_STAT_VALUES = ["2,400,000", "8,500", "640", "70–80%"]

# Wording on the SiteSettings singleton that later documents supersede.
# The Master Document named the organisation iREACHE LASTMILE and expanded the
# *i* as the plural "Innovations"; the REACH 360 website document then replaced
# the home page hero with the headline, standfirst and eyebrow it specifies.
# Each field lists every wording it has carried, oldest first, followed by the
# wording it should carry now. A field is only rewritten when it still holds one
# of those exact strings (or nothing at all), so anything an editor has changed
# in the CMS is left alone.
SUPERSEDED_SETTINGS = {
    "organisation_name": (
        ("REACHE Last-Mile",),
        "iREACHE LASTMILE",
    ),
    "tagline": (
        ("Innovation for Rural Empowerment in Access to Community Health and Equity",),
        "Innovations for Rural Empowerment in Access to Community Health and Equity",
    ),
    "hero_eyebrow": (
        (),
        "Sierra Leone · Eastern Province · 2026",
    ),
    "hero_prefix": (
        ("REACHE transforms", "iREACHE LASTMILE transforms"),
        "Building the health system",
    ),
    "hero_headline": (
        ("health care delivery to reach",),
        "Sierra Leone's communities",
    ),
    "hero_rotating_words": (
        ("everyone,every mother,every newborn,every village",),
        "have always deserved.",
    ),
    "hero_body": (
        (
            "REACHE Last-Mile designs responsive primary health care systems so that "
            "life-saving products and services reach the communities hardest to reach.",
            "iREACHE LASTMILE designs responsive primary health care systems so that "
            "life-saving products and services reach the communities hardest to reach.",
        ),
        "iREACHE LASTMILE connects three systems that have never governed community "
        "health together — traditional authority, government, and community "
        "intelligence — through 6,800 ProcCHWs reaching every last-mile household "
        "every month.",
    ),
    "footer_blurb": (
        (
            "REACHE Last-Mile works alongside government, communities and partners "
            "to build primary health care that reaches everyone, everywhere.",
        ),
        "iREACHE LASTMILE works alongside government, communities and partners "
        "to build primary health care that reaches everyone, everywhere.",
    ),
    "legal_line": (
        ("REACHE Last-Mile is a registered not-for-profit organisation",),
        "iREACHE LASTMILE is a registered not-for-profit organisation",
    ),
    "email": (
        ("info@reachelastmile.org",),
        "info@ireachelastmile.org",
    ),
}

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
        "We are a community health system strengthening organisation working at the "
        "last mile, to make primary health care reliable and accessible for the "
        "communities furthest from it.",
        """
        <blockquote>We are not the Sierra Leonean version of a global model. We are the
        first nationally-rooted community health systems institution Sierra Leone has
        produced — designed, from its founding moment, to build a community health system
        that belongs permanently to this country and to the people who live here.</blockquote>
        <p>iREACHE LASTMILE was founded on a different diagnosis — and a different
        solution.</p>
        <p>We are not a community health delivery organisation. We are a community health
        systems connection organisation. Our model — LASTMILE CARE — puts Professional
        Connected Community Health Workers, ProcCHWs, at the doorstep of every household
        in our programme communities every single month. But a ProcCHW in our model is not
        a service delivery agent. They are a systems connector — the human infrastructure
        through which the Traditional Authority System, the Government Health System and
        the Community Epidemiological System exchange intelligence, align authority, and
        govern community health together.</p>
        <h2>Our vision</h2>
        <p>A Sierra Leone where every person — in every last-mile community, regardless of
        distance or poverty — receives proactive, dignified community health care from a
        professional workforce their own community governs and their own government
        sustains.</p>
        <h2>Our mission</h2>
        <p>iREACHE LASTMILE saves lives at the last mile by deploying Professional
        Connected Community Health Workers who bring proactive, AI-supported care to every
        doorstep — bridging traditional authority, government and community into a health
        system that is community-governed and built to last.</p>
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
        "Innovations for Rural Empowerment in Access to Community Health and Equity.",
        """
        <h2>Vision</h2>
        <p>A Sierra Leone where every person — in every last-mile community, regardless of
        distance or poverty — receives proactive, dignified community health care from a
        professional workforce their own community governs and their own government
        sustains.</p>
        <h2>Mission</h2>
        <p>iREACHE LASTMILE saves lives at the last mile by deploying Professional
        Connected Community Health Workers who bring proactive, AI-supported care to every
        doorstep — bridging traditional authority, government and community into a health
        system that is community-governed and built to last, through the
        <a href="/reach-360/">REACH 360° Community Health Systems Strengthening
        Framework</a>.</p>
        <h2>Organisational values</h2>
        <p>Eight values, and what each one means in practice here rather than in a
        statement of intent.</p>
        <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Value</th>
              <th scope="col">What it means in practice at iREACHE LASTMILE</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">Equity</th>
              <td>Equity is the spine of the REACH 360° Framework — not a cross-cutting
              theme or a compliance requirement. Every resource allocation, system design,
              AI tool deployment and advocacy effort is directed first toward the
              communities most excluded from health outcomes. The communities with the
              highest burden receive the most intensive support. We measure success by
              narrowing the gap between the best-served and worst-served communities — not
              by improving programme averages while inequalities widen.</td>
            </tr>
            <tr>
              <th scope="row">Excellence</th>
              <td>We apply the highest technical and operational standards — modelled on
              Living Goods' supervision rigour, VillageReach's supply chain discipline,
              Muso's proactive care commitment and WHO's Responsible AI Ethics principles.
              We do not deploy tools, protocols or systems that have not been validated in
              Sierra Leone's specific context. We publish our methods and our results —
              including our failures — so that excellence is verifiable rather than
              claimed.</td>
            </tr>
            <tr>
              <th scope="row">Accountability</th>
              <td>We are accountable first to communities, then to government, then to
              donors — in that order. Community Health Committees govern programme
              decisions. DHMTs co-lead all supervision. Toll-free accountability hotlines
              give every community member a direct line to programme leadership. Annual
              Open House meetings make programme results publicly available and publicly
              contestable. We do not manage accountability. We build it into programme
              architecture.</td>
            </tr>
            <tr>
              <th scope="row">Co-ownership</th>
              <td>Doing WITH, not doing FOR is a programme design specification, not a
              communications aspiration. Communities select their ProcCHWs. Traditional
              Authority Health Governance Councils hold formal programme accountability.
              Community Health Committees make real governance decisions with real
              consequences. Co-ownership is the mechanism through which
              <a href="/our-model/bridge-360/">BRIDGE 360° LASTMILE CARE</a> outlasts
              iREACHE LASTMILE's direct involvement. It is what transforms a programme
              into a system.</td>
            </tr>
            <tr>
              <th scope="row">Government primacy</th>
              <td>Every system iREACHE LASTMILE builds is designed from its first day to be
              owned, financed and operated by the Government of Sierra Leone. We build no
              parallel infrastructure. We create no data systems that the government cannot
              access independently. We design no digital health tools that require iREACHE
              LASTMILE's technical team to interpret. We measure our success by how little
              Sierra Leone needs iREACHE LASTMILE at the end of the programme — not by how
              much.</td>
            </tr>
            <tr>
              <th scope="row">Evidence</th>
              <td>Every programme decision is grounded in data. The REACH 360° Crosswalk
              documents the evidence base for every framework element with the precision of
              a scientific citation — naming the specific international inspiration, the
              specific Sierra Leone evidence source and the specific original contribution.
              We treat our implementation experience as research data and publish it
              through peer-reviewed journals, open-access Learning Briefs and the annual
              REACH 360° Crosswalk update.</td>
            </tr>
            <tr>
              <th scope="row">Human primacy in digital health</th>
              <td>Digital and AI tools assist human care; they do not replace it. The
              ProcCHW's judgment, the community's trust, the traditional authority's
              endorsement and the government's clinical protocol are always the primary
              governing layer. Every tool must pass the
              <a href="/reach-360/idhs/">TRIAD AI Test</a> before it is deployed.</td>
            </tr>
            <tr>
              <th scope="row">Dignity</th>
              <td>Communities are rights-holders and governing partners, not passive
              beneficiaries. We listen before we design. We ask before we assume. We
              co-create rather than implement.</td>
            </tr>
          </tbody>
        </table>
        </div>
        <blockquote>Empowerment means doing WITH, not doing FOR.</blockquote>
        """,
    ),
    (
        "who-we-are/our-approach",
        "Our Approach",
        "Who We Are",
        "Three-Systems Connection Theory: Sierra Leone's community health crisis is not "
        "a CHW performance problem. It is a systems disconnection problem.",
        """
        <blockquote>Sierra Leone's community health crisis is not a CHW performance
        problem. It is a systems disconnection problem.</blockquote>
        <p>Three systems that must govern community health together have been operating in
        near-total isolation for decades. Every programme that treated CHW performance as
        the primary problem failed because it addressed a symptom while leaving the
        disconnection — the disease — untreated.</p>
        <h2>Why the standard diagnosis is wrong</h2>
        <p>The standard diagnosis of Sierra Leone's community health crisis runs as
        follows: CHWs are poorly trained, inadequately equipped, insufficiently supervised
        and uncompensated — therefore if we address these four deficiencies, health
        outcomes will improve. This diagnosis is not false. CHWs in Sierra Leone have
        historically been all of these things. But the diagnosis is incomplete in a way
        that has made every previous solution temporary.</p>
        <p>A CHW who is well trained, well equipped, well supervised and appropriately
        compensated but operating inside a disconnected system — where traditional
        authority structures have no role in health governance, where community
        surveillance intelligence never reaches DHMT planning, and where the government
        health system remains institutionally and geographically distant — is a
        high-performing individual inside a failing system. Individual performance
        improvements in a disconnected system produce episodic health gains during the
        programme cycle and systemic collapse when the programme ends. The gains disappear
        because the system that produced the need for those gains has not changed.</p>
        <h2>Three groups of people, none of them talking to each other</h2>
        <p>Sierra Leone has three groups of people who each hold something essential for
        community health. None of them talk to each other.</p>
        <p>That is the problem the <a href="/reach-360/">REACH 360° Framework</a> was
        designed to solve. Not CHW performance. Not supply chains. Not financing. Those are
        real problems. But they are symptoms. The disease underneath all of them is this:
        three groups of people who each hold something the others need — and who have
        never been connected into a single governing system.</p>
        <h2>System one: the Traditional Authority System — social legitimacy</h2>
        <p>Walk into any remote village in Kenema district. You will not find a government
        official. You will not find a DHMT representative. You may not find a health worker
        of any kind. But you will find a chief.</p>
        <p>A Section Chief. A Paramount Chief. A Bondo society leader. A women's group. A
        farmers' cooperative. These are the people who have governed community life in
        Sierra Leone for generations — long before the Republic of Sierra Leone existed as
        a legal entity, long before any Ministry of Health was established, long before any
        donor funded any health programme in any district. These structures are not
        ceremonial and they are not advisory. They are governing. They make decisions that
        communities obey. They settle disputes. They control land. They mobilise community
        members for collective action.</p>
        <h3>What they hold</h3>
        <p>The first thing is <strong>social legitimacy</strong>: the community's
        fundamental belief that the chief has the right to govern. It is not given by law
        and not granted by the government. It is held because the community believes it is
        held. That matters enormously in health care, because community health programmes
        succeed or fail on whether communities trust them. A programme endorsed by a
        paramount chief walks into a community with trust already built. A programme that
        bypasses the chief walks in as a stranger.</p>
        <p>The second is <strong>enforcement capacity</strong>. If a paramount chief tells
        a community that ProcCHW visits are a governance expectation — not optional, not a
        programme activity, but a governance expectation — then households that would
        otherwise close their doors to a female health worker begin to open them. The chief
        does not need police and does not need legal authority. The chief has social
        authority, which is more powerful in a remote chieftaincy than any government
        mandate.</p>
        <p>The third is <strong>embedded knowledge</strong>. A paramount chief knows their
        chieftaincy the way no outsider can. They know which families are most vulnerable,
        which households have pregnant women, which families cannot afford transport to the
        health facility, which households trust each other and which community members
        other people listen to. This knowledge is invisible to any DHMT planning meeting
        and any district database. It lives in the chief.</p>
        <h3>Why every programme ignored this</h3>
        <p>Every health programme that came to Sierra Leone before iREACHE LASTMILE made
        the same mistake. They consulted the chief. They held a community meeting. They
        asked for the chief's blessing. And then they moved on and ran their programme
        through government channels and NGO implementation structures, treating the chief
        as a stakeholder who had been properly engaged.</p>
        <p>They did not give the chief a governing role, formal decision-making authority
        over the programme, or accountability for outcomes in their chieftaincy. They did
        not connect the chief's social enforcement capacity to the health system in any
        structural way. This is like having the most trusted person in the room and asking
        them to stand in the corner while someone else runs the meeting. The REACH 360°
        Framework does not make that mistake.</p>
        <h2>System two: the Government Health System — clinical authority</h2>
        <p>The Government Health System is what most people think of when they hear the
        words <em>health system</em>: the Ministry of Health in Freetown, the District
        Health Management Teams in district capitals, the Peripheral Health Units scattered
        across chieftaincies, and the nurses, doctors, midwives, laboratory technicians and
        health officers who work inside these structures. It was built with international
        support over decades. It has policies, protocols, clinical standards and legal
        authority over health resource allocation. It is the official health system of
        Sierra Leone.</p>
        <h3>What it holds</h3>
        <p>The first thing is <strong>clinical authority</strong>. The government sets the
        clinical standards that determine what counts as quality care. It certifies health
        workers. It approves drug protocols. It operates the health facilities where
        complicated cases go when they are beyond a community health worker's scope.
        Without clinical authority, a community health programme is operating outside the
        law.</p>
        <p>The second is <strong>national resources</strong>. Only the government can put
        ProcCHW salaries into a national budget line. Only the government can integrate CHW
        data into the national health information system. Only the government can ensure
        that community health systems survive donor cycles — because donors come and go,
        but government budgets, in principle, continue. The path to a sustainable community
        health system runs through government financing. There is no other path.</p>
        <h3>The problem with this system</h3>
        <p>The Government Health System has a structural weakness that no amount of
        investment has ever fully solved. It is far away.</p>
        <p>Not just geographically, although that is real: the nearest PHU serving a remote
        Kenema chieftaincy may be fifteen kilometres away on a road that becomes impassable
        in the rainy season, and that distance kills people. But the distance is also
        institutional and social. A DHMT sits in a district town. Its planning meetings
        happen in offices. Its data comes from facilities. Its understanding of what is
        happening in a remote chieftaincy is limited to what gets reported through official
        channels — which, in communities without a functioning community health worker, is
        almost nothing. The Government Health System plans for populations it cannot fully
        see and allocates resources to communities it cannot fully reach, because the most
        marginalised communities are exactly the ones least represented in government data
        systems.</p>
        <p>This is not a failure of intent. It is a structural failure of distance. And you
        cannot solve a distance problem by improving the performance of the institution
        that is far away. You solve it by connecting that institution to the intelligence
        that is close.</p>
        <h2>System three: the Community Epidemiological System — post-Ebola intelligence</h2>
        <p>This is the hardest system to see, because it was never formally named until the
        REACH 360° Framework named it. It is not an organisation. It has no offices and no
        staff. It appears in no government directory and no donor database. It is the
        health knowledge that Sierra Leone's communities hold inside themselves —
        specifically, and this is the part that makes it unique in the world, the health
        knowledge that communities in Eastern Province built by surviving the 2014–2016
        Ebola outbreak.</p>
        <h3>What communities built, and how</h3>
        <p>In 2014 Ebola entered Sierra Leone and spread fast. The formal health system was
        overwhelmed almost immediately. In the communities most severely affected —
        including communities in Kenema district, where iREACHE LASTMILE is headquartered
        today — people were watching their neighbours and family members die, and the
        formal response was not arriving fast enough to stop it. So communities did
        something no health programme had planned for. They started protecting
        themselves.</p>
        <ol>
          <li><strong>They started watching.</strong> People paid attention to specific
          symptoms — fever, extreme weakness, vomiting, bleeding — noticed when a
          neighbour showed these signs, and talked to each other about what they were
          seeing. That is the beginning of community-based disease surveillance: the exact
          function formal epidemiology systems perform, done by ordinary people with no
          training, no equipment and no mandate.</li>
          <li><strong>They built alert chains.</strong> One person tells the Section Chief.
          The Section Chief tells the Paramount Chief. The Paramount Chief sends word to
          the nearest health post or response team. These chains were never written down or
          formalised into any protocol. They were improvised under pressure. But they moved
          information from the community to the formal response faster than official
          reporting channels, because they ran through trusted relationships rather than
          bureaucratic processes.</li>
          <li><strong>They developed isolation understanding.</strong> Communities learned
          by watching the disease move that contact with a sick person was dangerous, and
          developed their own approaches to separating sick people from healthy ones. Chiefs
          enforced those approaches through social authority — which, in a remote
          chieftaincy, moves faster and with less resistance than a government order that
          takes days to arrive.</li>
          <li><strong>They built trust-based reporting.</strong> Families were hiding sick
          members because they were terrified of what reporting would mean, so official
          channels were failing at exactly the moment they needed to work. Communities
          developed what the formal system could not: trusted intermediaries — neighbours
          and community leaders through whom sick households would communicate, and who
          made the connection to the formal response feel less threatening.</li>
          <li><strong>They built a collective memory.</strong> By the time Ebola ended in
          2016, communities in Eastern Province had eighteen months of lived experience
          with disease detection and community response. They knew what early symptoms
          looked like, how fast the disease moved, which contact patterns were risky, and
          how to mobilise community authority for health protection.</li>
        </ol>
        <h3>Why nobody recognised it</h3>
        <p>After Ebola ended, health programmes returned to Eastern Province. They assessed
        community health needs. They designed interventions. They trained community health
        workers in disease surveillance protocols. But they did not ask communities what
        they already knew. Nobody sat down with the survivors of Kenema's Ebola response
        and asked how their detection system had worked, what could be learned from it, or
        how it could be formalised so that it continues to function when the next health
        threat arrives.</p>
        <p>So the knowledge sat dormant: informally present in communities, officially
        invisible to the health system. This is what the REACH 360° Framework calls the
        Community Epidemiological System. It is not something iREACHE LASTMILE invented. It
        is something Sierra Leone's communities built, at tremendous cost, and that no
        health architecture had ever formally recognised and activated until now.</p>
        <h2>How the ProcCHW connects all three systems at once</h2>
        <p>Repositioning the community health worker from service delivery agent to systems
        connector is the theoretical contribution that makes the REACH 360° Framework
        original. The <a href="/our-model/procchw/">ProcCHW</a> is the human infrastructure
        through which the three systems exchange intelligence, align authority, and govern
        community health together. This is not an additional function layered on top of
        service delivery. It is the primary function — from which service delivery
        quality, sustainability and equity all derive.</p>
        <p>She is selected by the traditional authority, so she carries social legitimacy
        into every household she visits. She reports into the government health system, so
        her data flows into national DHIS2, her referrals reach government facilities and
        her work is co-owned by the DHMT. And she activates the community epidemiological
        intelligence — through the CEIN, through the post-Ebola detection knowledge her
        neighbours hold, through the alert networks communities built during Ebola and that
        the Framework formalises as a standing component of Sierra Leone's national
        surveillance system.</p>
        <p>She is not just a health worker delivering services. She is a connection — made
        human — between three systems that each hold something essential and that have
        never, before the REACH 360° Framework, been designed to work together.</p>
        <p>Connection is also what we measure. See
        <a href="/reach-360/connection-quality-index/">the Connection Quality Index</a>.</p>
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
        "Two encounters, one decision, and one name written on a piece of paper.",
        """
        <h2>The first encounter</h2>
        <p>In June 2018, Augustine Alie was working as a community development officer in
        Kenema district. His work took him across the district regularly — to chieftaincy
        meetings, to community health consultations, to the planning meetings where DHMT
        staff and NGO representatives sat together and discussed programme targets.</p>
        <p>One morning he drove three hours on a dirt road to attend a community health
        planning meeting in a remote chieftaincy. He arrived to find forty community
        members waiting. They had been waiting since eight in the morning. It was now
        eleven. The NGO representative had not come; the vehicle had broken down somewhere
        between Kenema town and the chieftaincy, and nobody had sent word.</p>
        <p>Augustine ran the meeting himself. He had not planned to. He did not have the
        programme documents or the agenda. He sat down with the forty community members and
        asked them the only question he could think of.</p>
        <blockquote>Tell me what health care looks like in your community right now. Not
        what you want. What is actually happening.</blockquote>
        <p>They talked for three hours. What Augustine heard that morning — the specific
        texture of community health failure in Eastern Sierra Leone, described not through
        data but through lived experience — stayed with him for years. A grandmother
        describing how her granddaughter had died of a fever because the community health
        worker's medicine kit had been empty for six weeks. A young man describing the
        chief's frustration at being asked to mobilise community members for a programme
        that had collapsed three times in twelve years. A pregnant woman sitting quietly at
        the back of the room who said only one thing when Augustine looked at her
        directly.</p>
        <blockquote>I am afraid of this pregnancy. Not because I am sick, because I don't
        know if anyone will be there when it matters.</blockquote>
        <p>Augustine drove back to Kenema that afternoon with forty testimonies in his
        notebook and one question he could not answer: why does Sierra Leone keep building
        the same programmes and getting the same results?</p>
        <h2>The second encounter</h2>
        <p>Eight months later, Augustine was visiting his grandmother in her village in the
        Niawa chieftaincy of Kenema district. She was seventy-four years old. She had lived
        through the civil war, through the Ebola outbreak, through more health programmes
        than she could count. She was sharp and direct and completely unimpressed by
        official explanations of anything.</p>
        <p>On his second evening there, Augustine told her about the question he had been
        carrying since the community meeting eight months earlier. She listened. She made
        tea. She was quiet for a long time. Then she told him something he had not
        known.</p>
        <p>During the Ebola outbreak in 2014, when the formal health response was slow to
        reach their chieftaincy, the community had organised itself. The paramount chief had
        convened an emergency council. Women's group leaders had gone house to house asking
        specific questions about symptoms. Section chiefs had set up alert chains. Trusted
        community members had become the conduits through which sick households
        communicated with the response teams — because families trusted their neighbours in
        a way they did not yet trust the government teams arriving in unfamiliar protective
        equipment. She described the network in specific detail: who had done what, how the
        alerts had moved, which community decisions had contained transmission in which
        neighbourhoods.</p>
        <blockquote>We did these ourselves, before anyone came to help us. We already knew
        how to protect each other. Nobody ever asked us about it afterward. Nobody wrote it
        down. Nobody used it for anything. The next programme that came just started
        training people as if we knew nothing.</blockquote>
        <p>She looked at Augustine steadily. <em>The knowledge is still here</em>, she said,
        <em>in this community. In every community that survived. Nobody has ever connected
        it to anything.</em></p>
        <p>Augustine sat with his grandmother until late that night. When he drove back to
        Kenema the following morning, he had the answer to the question he had been carrying
        for eight months.</p>
        <p>Sierra Leone was not getting different results because it needed better
        programmes. It was getting the same results because it was ignoring three systems
        that were already present in every community — the traditional authority that held
        social legitimacy, the government health architecture that held clinical authority,
        and the community's own epidemiological intelligence that had been built through
        survival and never activated.</p>
        <p>He pulled over on the road between Niawa chieftaincy and Kenema town. He took
        out his notebook and wrote four words at the top of a blank page.</p>
        <blockquote>What if we connected them?</blockquote>
        <p>Below those four words, he began writing what would eventually become the
        <a href="/reach-360/">REACH 360° Community Health Systems Strengthening
        Framework</a>.</p>
        <h2>The name</h2>
        <p>A week later, Augustine was in a small meeting room in Kenema with four
        colleagues — a public health physician, a community development specialist, a
        former DHMT officer, and a nurse who had worked in rural health posts for fifteen
        years. He walked them through what he had been thinking. They talked for two
        days.</p>
        <p>On the second afternoon, they needed to name what they were building. The nurse
        — a woman named Mariama Koroma, no relation to Augustine — wrote one sentence on
        the whiteboard.</p>
        <blockquote>We are building something for the people the system never reaches: the
        last mile, the forgotten mile.</blockquote>
        <p>Augustine looked at the sentence for a long time. Then he wrote five words
        underneath it — <em>Innovations for Rural Empowerment — iREACHE</em> — and below
        that, three more: <em>Last mile. Always.</em></p>
        <p>The organisation was named in that room in Kenema on a Tuesday afternoon in
        March 2019. Its headquarters have been in Kenema ever since. Not in Freetown. Not in
        a district capital closer to the international airport or the donor offices or the
        government ministries. In Kenema, where the grandmother's knowledge lives, where the
        community meeting happened with forty people and no NGO representative. Where the
        question was first asked and where the answer is being built.</p>
        <h2>What we are building</h2>
        <p>iREACHE LASTMILE exists because two encounters — a community meeting where forty
        people described the texture of health failure in the most honest language Augustine
        had ever heard, and an evening with an elderly woman who described a community
        surveillance network that had saved lives and been forgotten — revealed something
        that ten years of programme evaluations and district health reports had not.</p>
        <p>Sierra Leone does not need another community health programme. Sierra Leone needs
        a community health system: one that connects what already exists — the chief's
        social authority, the government's clinical capacity, the community's
        epidemiological intelligence — into a single governing architecture that is
        community-owned, government-integrated and domestically financed.</p>
        <p>One that, when asked Chief Fofanah's question — <em>when you go, what belongs to
        us?</em> — can answer clearly. Everything. The governance belongs to the community.
        The data belongs to the government. The knowledge belongs to the people who built it
        by surviving Ebola. The financing belongs to Sierra Leone's own budget.</p>
        <p>The only thing that leaves when iREACHE LASTMILE leaves is iREACHE LASTMILE. The
        system stays. That is what we are building. That is why we exist.</p>
        <h2>A vision written in Kenema</h2>
        <blockquote>A Sierra Leone where every person — in every last-mile community,
        regardless of distance or poverty — has equitable access to quality community health
        care delivered by a workforce their own community governs and their own government
        sustains.</blockquote>
        """,
    ),
    (
        "who-we-are/strategy-2030",
        "Strategy 2030",
        "Who We Are",
        "The 2026–2031 programme period, and what has to be true at the end of it.",
        """
        <p>Our strategy runs to 2031 and is set by three forces that converged in 2025 and
        2026. The Government of Sierra Leone's Vision 2030 Community Health Worker
        Programme established a national mandate for 6,800 professional, paid, digital and
        supervised community health workers across all 16 districts — the largest domestic
        community health investment in the country's history. The UNICEF–MasterCard
        Foundation Integrated Community Health Programme launched in January 2026 as the
        financing vehicle for that mandate, seeking national implementing partners able to
        deliver at scale. And the International Rescue Committee closed its Sierra Leone
        operations in September 2025 after 26 years, describing the closure as a handover
        to strong national organisations.</p>
        <p>This window will not remain open indefinitely. Every design decision in the
        <a href="/reach-360/">REACH 360° Framework</a> was made in the knowledge that the
        moment requires not a programme but a system, and not an international organisation
        but a national institution that will still be here after every donor cycle
        ends.</p>
        <h2>Phased systems activation</h2>
        <blockquote>The most important implementation lesson in community health systems
        building: deploy systems before ProcCHWs. Every ProcCHW deployed before governance
        is established, supply chain is integrated and IDHS is validated is a ProcCHW
        deployed into a service delivery role rather than a systems connector role.</blockquote>
        <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Phase</th>
              <th scope="col">Period</th>
              <th scope="col">ProcCHWs</th>
              <th scope="col">Human system milestones</th>
              <th scope="col">IDHS milestones</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">1. Foundation</th>
              <td>Jan–Jun 2026</td>
              <td>0 — systems only</td>
              <td>All legal registrations; Board constituted; core governance documents;
              TACGS governance bodies in Kenema pilot chieftaincies; government platform
              configured; equity baseline completed; MoH recognition secured; UNICEF–MCF
              application submitted.</td>
              <td>IDHS literacy integrated into the ProcCHW training curriculum. AI tool
              design within DHIS2 architecture initiated. TRIAD AI Test documented and
              Board-approved. IDHS Readiness Assessment completed. No AI applications
              deployed.</td>
            </tr>
            <tr>
              <th scope="row">2. Architecture</th>
              <td>Jul–Dec 2026</td>
              <td>0 — architecture only</td>
              <td>TRIAD Governance Protocols and DHMT MoU signed in Kenema; CHCs
              constituted; ProcCHW Supervisors trained; all 32 critical-path documents
              produced; ProcCHW curriculum MoH-accredited; platform fully operational; CEIN
              activation guide completed.</td>
              <td>IDHS clinical decision support configured in DHIS2 as a program rule
              extension; PBI anomaly detection rules written; AI alert feedback protocol
              co-designed with ProcCHW input. No AI applications deployed.</td>
            </tr>
            <tr>
              <th scope="row">3. Activation</th>
              <td>Q1–Q2 2027</td>
              <td>~250, Kenema</td>
              <td>First Kenema ProcCHW cohort trained and deployed. First PBI payment on
              the 1st of the month. First CQI assessment. Adaptive management before
              expanding to other pilot chieftaincies.</td>
              <td>IDHS iCCM decision support activated in Kenema. PBI anomaly detection
              active. Basic stockout alerts active. Community feedback AI classification
              active with CHC contestability. First AI Learning Brief published.</td>
            </tr>
            <tr>
              <th scope="row">4. Scale</th>
              <td>Q3 2027–2028</td>
              <td>800–2,800</td>
              <td>Scale to 4 pilot districts after Kenema CQI &gt; 60. The architecture
              phase is replicated in each new district before any ProcCHW is deployed.
              UNICEF–MCF programme fully activated.</td>
              <td>Phase 2 IDHS tools activated after supply chain optimisation completes:
              21-day demand forecasting; outbreak detection; zero-dose prediction;
              personalised supervision. IDHS validated in Kenema before each new district
              deployment.</td>
            </tr>
            <tr>
              <th scope="row">5. Institutionalisation</th>
              <td>2029–2031</td>
              <td>6,800</td>
              <td>All 16 districts; 70–80% domestic financing; MoH leads all operations;
              iREACHE LASTMILE transitions to a technical assistance role in the earliest
              districts; final evaluation published.</td>
              <td>Phase 3 IDHS tools active: MUAC trajectory; financing simulation; Krio
              NLP. Full IDHS government ownership transfer by 2031. The technical
              assistance role includes IDHS model governance support for government.</td>
            </tr>
          </tbody>
        </table>
        </div>
        <h2>What has to be true by 2031</h2>
        <ul>
          <li>6,800 ProcCHWs deployed across all 16 districts, certified, compensated and
          on a pathway toward government employment.</li>
          <li>70 to 80 per cent of programme costs met from Sierra Leone's domestic
          budgets, with full government ownership of programme systems before donor
          exit.</li>
          <li>District Health Management Teams co-leading all supervision, and accessing
          all programme data directly without our intermediation.</li>
          <li>The Community Epidemiological Intelligence Network operating as a
          government-integrated surveillance system independent of our facilitation.</li>
          <li>Traditional Authority Health Governance Councils advocating directly to
          District Councils for ProcCHW budget lines.</li>
        </ul>
        <h2>The test</h2>
        <p>If we reduce our presence in a community by thirty per cent, do the three
        systems — traditional authority, government health and community epidemiological
        — continue to govern community health together? The answer must be yes. That is
        what it means to have built a system rather than run a programme.</p>
        """,
    ),
    (
        "our-model",
        "Our Model",
        "Our Model",
        "BRIDGE 360° LASTMILE CARE — building resilient integrated delivery gateways for "
        "every community.",
        """
        <p><strong>BRIDGE 360° LASTMILE CARE</strong> is our model for delivering
        responsive, connected and digitally supported community health care in Sierra
        Leone. It is the operational expression of the
        <a href="/reach-360/">REACH 360° Framework</a> — translating the Framework's
        architecture into the lived experience of a household in a remote chieftaincy of
        Kenema district receiving a visit from their ProcCHW on the third Tuesday of every
        month.</p>
        <blockquote>Reaching every household. Connecting every system. Leaving no community
        behind.</blockquote>
        <h2>Explore the model</h2>
        <ul>
          <li><a href="/our-model/the-challenge/">The Challenge</a> — why Sierra Leone's
          community health crisis is a systems problem, not a workforce problem.</li>
          <li><a href="/our-model/bridge-360/">BRIDGE 360° LASTMILE CARE</a> — the five
          delivery mechanisms.</li>
          <li><a href="/our-model/lastmile-care/">LASTMILE CARE in Sierra Leone</a> — what
          makes the model distinctively Sierra Leonean.</li>
          <li><a href="/our-model/procchw/">The ProcCHW Cadre</a> — the human
          infrastructure that makes it real.</li>
        </ul>
        """,
    ),
    (
        "our-model/the-challenge",
        "The Challenge",
        "Our Model",
        "Sierra Leone does not have a community health workforce problem. It has a "
        "community health systems problem.",
        """
        <blockquote>Sierra Leone does not have a community health workforce problem. It has
        a community health systems problem — and the difference is the difference between
        treating a symptom and curing a disease.</blockquote>
        <p>Every community health programme Sierra Leone has hosted over the past four
        decades has begun with the same promise and ended with the same failure. The
        promise: to deploy community health workers who will reach the most marginalised
        communities. The failure: to build the systems that would make those workers
        effective, accountable and sustainable beyond the end of a grant cycle.</p>
        <h2>Why the standard diagnosis is wrong</h2>
        <p>The standard diagnosis runs as follows: CHWs are poorly trained, inadequately
        equipped, insufficiently supervised and uncompensated — so address those four
        deficiencies and outcomes will improve. The diagnosis is not false. But it is
        incomplete in a way that has made every previous solution temporary.</p>
        <p>A CHW who is well trained, well equipped, well supervised and appropriately
        compensated, but operating inside a disconnected system, is a high-performing
        individual inside a failing system. Individual performance improvements in a
        disconnected system produce episodic gains during the programme cycle and systemic
        collapse when the programme ends. The gains disappear because the system that
        produced the need for them has not changed.</p>
        <h2>The disconnection</h2>
        <p>Three systems must govern community health together, and in Sierra Leone they
        have been operating in near-total isolation for decades: the Traditional Authority
        System that holds social legitimacy, the Government Health System that holds
        clinical authority and national resources, and the Community Epidemiological System
        that holds the surveillance intelligence communities built while surviving
        Ebola.</p>
        <p>Read the full argument in
        <a href="/reach-360/three-systems/">the Three-Systems Connection Theory</a>.</p>
        """,
    ),
    (
        "our-model/bridge-360",
        "BRIDGE 360° LASTMILE CARE",
        "Our Model",
        "Building Resilient Integrated Delivery Gateways for Every community — the five "
        "delivery mechanisms.",
        """
        <p>The name carries three meanings at once. A bridge connects what cannot connect
        itself, and this model connects the three systems that have never governed
        community health together in Sierra Leone. A bridge is built to last, built for
        everyone, and built where the crossing is most difficult. And BRIDGE is an
        acronym — <strong>B</strong>uilding <strong>R</strong>esilient
        <strong>I</strong>ntegrated <strong>D</strong>elivery <strong>G</strong>ateways for
        <strong>E</strong>very community — naming what the model actually constructs.</p>
        <p>The five delivery mechanisms are not sequential steps. They operate
        simultaneously and reinforce each other. A ProcCHW making a proactive doorstep
        visit is at the same time activating community governance through their chiefly
        endorsement, removing barriers through services provided at no cost, connecting the
        household to the government health system through the referral system in their
        pocket, and building care infrastructure that will still be operating in 2035.</p>
        <h2>1. Proactive doorstep visits</h2>
        <p>ProcCHWs do not wait for sick people to find them. Every registered household
        receives a monthly visit whether or not anyone has reported illness, and at each
        doorstep receives an integrated seven-area service package in a single visit at no
        cost. The Agricultural Calendar Alignment Protocol adjusts scheduling around each
        district's farming calendar so peak planting and harvesting seasons never become
        health access gaps.</p>
        <h2>2. Community governance access</h2>
        <p>Every ProcCHW is formally nominated by their Paramount or Section Chief with
        mandatory co-endorsement by the community's women's group. This Traditional
        Authority Access Endorsement changes the social permission structure for household
        access: chiefly endorsement transforms a ProcCHW visit from an external programme's
        activity into a community governance expectation. Traditional Authority Health
        Governance Councils meet quarterly with a mandatory minimum of 50% female
        membership. Community Health Committees hold governing power over ProcCHW
        selection, service prioritisation and resource allocation — not advisory rights.
        The model does not give communities a voice in health governance. It gives them
        governing power.</p>
        <h2>3. Care without barriers</h2>
        <p>Four barrier categories are removed rather than reduced. The
        <strong>financial</strong> barrier, through full alignment with Sierra Leone's Free
        Healthcare Initiative. The <strong>transport</strong> barrier, through the Community
        Transport Linkage Fund administered by Community Health Committees. The
        <strong>geographic</strong> barrier, through the Rainy Season Routing Protocol,
        which pre-positions essential medicines in road-inaccessible communities before the
        roads close, and a district motorbike logistics network. The <strong>social and
        gender</strong> barrier, through Traditional Authority Access Endorsement and a
        minimum 60% female ProcCHW workforce in every district.</p>
        <h2>4. Connected government referral</h2>
        <p>When a ProcCHW identifies a patient needing care beyond their scope, a
        closed-loop electronic referral connects that patient to a government Peripheral
        Health Unit immediately. The PHU is notified before the patient arrives, arrival is
        confirmed by facility staff, and the clinical outcome is recorded within fourteen
        days. If the patient does not arrive within the expected window the ProcCHW is
        alerted to follow up and arrange transport. Every referral connects to Sierra
        Leone's government health system — not to our facilities, not to private services
        — and all data flows into the national DHIS2 in real time. We hold no exclusive
        data.</p>
        <h2>5. Care that lasts</h2>
        <p>The model is designed to make itself unnecessary as an externally managed
        programme. By 2031, 70 to 80 per cent of costs will be met from domestic government
        budgets, DHMTs will co-lead all supervision, and Traditional Authority Health
        Governance Councils will advocate directly to District Councils for ProcCHW budget
        lines. The ultimate test: if we reduce our presence in a community by thirty per
        cent, do the three systems continue to govern community health together? The answer
        must be yes.</p>
        """,
    ),
    (
        "our-model/lastmile-care",
        "LASTMILE CARE in Sierra Leone",
        "Our Model",
        "Five elements of the care model that exist nowhere else, because they were built "
        "from Sierra Leone's own history.",
        """
        <p>BRIDGE 360° LASTMILE CARE is not an adaptation of a global community health
        model. Five of its elements were built from conditions specific to this country,
        and could not have been designed anywhere else.</p>
        <h2>Community Epidemiological Intelligence Network</h2>
        <p>Formalises the disease detection, risk communication and community mobilisation
        capabilities that Sierra Leonean communities built during the 2014–2016 Ebola
        outbreak as a standing, community-governed, DHMT-integrated surveillance component.
        No international framework was built from this experience, because no international
        framework was designed here.</p>
        <h2>Traditional Authority Access Endorsement</h2>
        <p>Formal endorsement by Paramount and Section Chiefs changes the social permission
        structure for household access in communities where cultural norms restrict entry.
        Sierra Leone's chieftaincy governance system — with its particular authority
        structures and social enforcement capacity — has no direct equivalent in Uganda,
        Mali, Liberia or Kenya, where comparable CHW models operate.</p>
        <h2>Agricultural Calendar Alignment Protocol</h2>
        <p>Visit scheduling formally adjusted around each district's farming calendar,
        co-developed with Community Health Committees, so that the weeks of peak
        agricultural labour — which women disproportionately carry — do not become
        health access gaps. Smallholder farming seasons determine women's availability more
        decisively than any administrative calendar.</p>
        <h2>Post-Ebola Mental Health Pulse Check</h2>
        <p>Basic psychological health screening integrated into routine household visits in
        communities directly affected by the outbreak, using a tool validated with Sierra
        Leonean clinical psychologists, with positive screens referred to PHU mental health
        officers. No community health model anywhere has operationalised post-Ebola mental
        health screening as a routine primary care component.</p>
        <h2>Shared Sovereignty Financing with a Chieftaincy Track</h2>
        <p>Traditional authority as a third financing sovereignty actor — Paramount Chiefs
        advocating to District Councils for ProcCHW budget lines within their chiefdoms,
        using chieftaincy's constitutional standing in local government. That advocacy
        pathway exists in this specific form nowhere else in West Africa.</p>
        """,
    ),
    (
        "our-model/procchw",
        "The ProcCHW Cadre",
        "Our Model",
        "Professional Connected Community Health Workers — certified, compensated, "
        "triple-connected, government-integrated, community-governed and career-pathed.",
        """
        <p>Professional Connected Community Health Workers are something new in Sierra
        Leone's community health landscape. They are not volunteers. They are not
        government extension workers deployed without training, equipment or support. They
        are not programme-specific CHWs whose mandate disappears when a grant cycle ends.
        They are certified, compensated, government-integrated community health
        professionals who function at once as care deliverers, community intelligence nodes
        and connectors between three previously isolated governance systems.</p>
        <h2>What the name means</h2>
        <p><strong>Professional</strong> names what makes this cadre different from every
        CHW Sierra Leone has previously deployed: compensation through a structured salary
        and performance incentive, a recognised certification co-issued with the Ministry
        of Health, clinical protocols validated to national standards, government-owned
        digital tools, and a defined career pathway toward full government
        employment.</p>
        <p><strong>Connected</strong> names the defining architectural standard. Every
        ProcCHW maintains three simultaneous active connections — upward to their
        supervisor, laterally to their peer network, and downward to their community's
        governance structures. A ProcCHW missing any one of these is not yet fully
        functional within the Framework. One connected to their community but reporting
        into a data system outside government architecture is an isolated worker outside
        the grid.</p>
        <h2>Selection is a governance act</h2>
        <p>ProcCHW selection is a governance act, not a recruitment exercise. A five-stage
        process ensures every appointment carries community legitimacy, government
        recognition and programme accountability at the same time. A ProcCHW selected by
        the programme but not endorsed by their community's traditional authority has a
        fundamentally different accountability relationship. One selected without DHMT
        verification is not recognised within the government health system. Both dimensions
        are non-negotiable.</p>
        <h2>Eight-week certification</h2>
        <ol>
          <li><strong>Sierra Leone foundation</strong> — three weeks residential covering
          district disease burden, the Free Healthcare Initiative, iCCM, maternal and
          newborn danger signs, nutrition screening, the immunisation schedule, community
          surveillance and CEIN protocols, WASH, family planning counselling and the
          Post-Ebola Mental Health Pulse Check. Assessed across seven domains at 75% or
          above before any field work.</li>
          <li><strong>Platform and digital skills</strong> — one week residential on every
          module of the government CHW digital platform, plus how to interpret a clinical
          alert, when to override one, and how to report an error. Assessed at 85% or
          above.</li>
          <li><strong>Supervised field practice</strong> — four weeks in the community
          under direct supervisor observation, ending in competency sign-off, a joint
          Ministry of Health appointment letter and a public appointment ceremony.</li>
          <li><strong>Continuous learning</strong> — quarterly protocol updates, peer case
          review and an annual competency reassessment, logged in the government
          platform.</li>
        </ol>
        <h2>Compensation architecture</h2>
        <p>A fixed monthly stipend makes up 50 to 60 per cent of the package and is paid on
        the first of every month by mobile money, without exception and without
        administrative delay — one missed payment date destroys three months of trust, so
        the payment system is the retention system. A performance-based incentive makes up
        the remainder, weighted across household visit coverage, data reporting quality,
        referral completion, zero-dose child identification and stock reporting
        timeliness.</p>
        <p>Equity safeguards are built into the architecture. Pay is equal for all ProcCHWs
        at the same tier regardless of gender, geography or ethnicity. An adjustment
        mechanism accounts for structural barriers such as rainy season road
        inaccessibility and documented safety incidents. An annual gender pay gap audit
        triggers a mandatory District Coordinator investigation if the gap exceeds 5% within
        comparable community types, and female ProcCHWs' domestic and agricultural
        responsibilities are explicitly excluded as grounds for withholding promotion.</p>
        <h2>Equipment</h2>
        <p>A complete clinical diagnostics kit, protective equipment, job aids, and an
        Android device running the government platform in offline-first mode with solar and
        hand-crank charging. All provided at no cost, and replaced under a 72-hour guarantee
        that applies regardless of how remote the community is — geographic isolation
        cannot disadvantage a ProcCHW in equipment access.</p>
        <h2>Career pathway</h2>
        <p>ProcCHW, then Senior ProcCHW or Peer Leader, then ProcCHW Supervisor — a full
        salaried position co-funded with the District Health Management Team from Year 3.
        Progression criteria are published, accessible to every ProcCHW and applied
        transparently, with promotion rates reviewed annually and disaggregated by
        gender.</p>
        """,
    ),
    (
        "reach-360",
        "The REACH 360° Framework",
        "REACH 360°",
        "The Community Health Systems Strengthening Framework — architecture, equity "
        "spine and seven-pillar integration logic.",
        """
        <blockquote>REACH 360° means complete rotation with no blind spots, full circle
        connection with self-sustaining governance, and full coverage with no person
        outside the circle of care. That is not a communications aspiration. It is a
        programme design specification.</blockquote>
        <p>The REACH 360° Community Health Systems Strengthening Framework is the
        architecture from which every one of our programme documents derives. It is
        published open-access under Creative Commons CC BY 4.0. We invite critique,
        adaptation and replication, and we commit to publishing what we learn — including
        our failures.</p>
        <h2>The framework architecture</h2>
        <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Level</th>
              <th scope="col">Name</th>
              <th scope="col">Content</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">1</th>
              <td>Global and national foundation</td>
              <td>WHO Health System Building Blocks (2007); primary health care from
              Alma-Ata 1978 and Astana 2018; the UHC Framework; SDGs 1, 2, 3, 5, 10, 13 and
              17; WHO AI Ethics 2021; Sierra Leone NHSSP; National CHW Policy 2024; Vision
              2030 CHW Programme; Free Healthcare Initiative 2010; Sierra Leone IDSR
              Framework; National eHealth and Digital Health Policy.</td>
            </tr>
            <tr>
              <th scope="row">2</th>
              <td>Theoretical architecture</td>
              <td><a href="/who-we-are/our-approach/">Three-Systems Connection Theory</a> —
              Sierra Leone's community health crisis is a systems disconnection problem;
              the <a href="/reach-360/foundations/">Four Constitutional Foundations</a>
              specific to Sierra Leone's governance reality; equity as the structural spine
              of all seven pillars; the
              <a href="/reach-360/connection-quality-index/">Connection Quality Index</a> as
              the primary measurement architecture;
              <a href="/reach-360/idhs/">Intelligent Digital Health Systems</a> integration
              as a horizontal design dimension.</td>
            </tr>
            <tr>
              <th scope="row">3</th>
              <td>Seven REACH 360° pillars</td>
              <td><a href="/what-we-do/">Connected Health Workforce</a> | Community
              Intelligence and Surveillance System | Last-Mile Supply Chain and Commodity
              Access | Sustainable Health Financing and Domestic Resource Mobilisation |
              Three-Authority Community Governance and Accountability | Proactive Community
              Health Service Delivery | Driving Sustained Impact Through Strategic
              Partnerships.</td>
            </tr>
            <tr>
              <th scope="row">4</th>
              <td>Continuous systems cycle</td>
              <td>Listen → Map → Co-create → Connect → Deliver → Measure → Learn →
              Strengthen → Sustain → Scale — a closed loop returning to Listen at a higher
              level of system integration with each completed cycle.</td>
            </tr>
            <tr>
              <th scope="row">5</th>
              <td>Nine programme areas</td>
              <td>Maternal and newborn health | Childhood disease (iCCM) | Immunisation and
              zero-dose reduction | Nutrition systems | Sexual and reproductive health |
              Community disease surveillance | Intelligent digital health systems |
              Last-mile health supply chain | Emergency response and WASH.</td>
            </tr>
            <tr>
              <th scope="row">6</th>
              <td>Measurement architecture</td>
              <td>Output impact (pillar KPIs) → Outcome impact (health status) → Systems
              impact (Connection Quality Index) → IDHS impact (AI Readiness and Responsible
              Deployment Index) → Equity impact (Equity Progress Threshold) → stronger
              community health systems, better outcomes, government capacity, health equity
              and universal health coverage.</td>
            </tr>
          </tbody>
        </table>
        </div>
        <h2>Equity as the spine</h2>
        <p>Equity is not a cross-cutting theme in this Framework. It is the structural logic
        that determines why each pillar is designed the way it is. The reason the Framework
        starts from a systems connection theory rather than a CHW performance theory is an
        equity reason: the communities most excluded from health outcomes are not excluded
        because their CHWs perform badly, but because the three governance systems that
        should protect them are disconnected. The most disconnected communities are always
        the most marginalised.</p>
        <p>It operates at four levels at once. <strong>Structural equity</strong> changes
        the systems that produce inequitable outcomes. <strong>Targeting equity</strong>
        weights resources, supervision intensity and commodity priority toward the most
        marginalised communities. <strong>Process equity</strong> makes the governance
        processes themselves equitable. <strong>Outcomes equity</strong> narrows the gap
        between Sierra Leone's best- and worst-served communities, enforced through the
        Equity Accountability Standard.</p>
        <h2>Why the seven pillars are one system</h2>
        <p>The pillars are not parallel programmes. Each is essential to the others, and the
        failure of any one undermines the whole. Without the Connected Health Workforce
        there is no human infrastructure through which the systems can exchange
        intelligence. Without surveillance, community intelligence stays invisible to
        district planning. Without the supply chain, ProcCHWs arrive with empty kits and
        trust erodes. Without sustainable financing, the programme becomes another
        donor-dependent initiative that collapses when the cycle ends. Without
        three-authority governance, the difference between an NGO-run programme and a
        community-governed system disappears. Without proactive delivery, the equity
        commitment exists on paper but not at the doorstep. And without strategic
        partnerships, Sierra Leone's post-Ebola community health intelligence remains a
        local programme story rather than a contribution to global evidence.</p>
        """,
    ),
    (
        "reach-360/three-systems",
        "The Three-Systems Connection Theory",
        "REACH 360°",
        "Sierra Leone's community health crisis is not a CHW performance problem. It is a "
        "systems disconnection problem.",
        """
        <p>Three systems that must govern community health together have been operating in
        near-total isolation for decades. Every programme that treated CHW performance as
        the primary problem failed because it addressed a symptom while leaving the
        disconnection — the disease — untreated.</p>
        <h2>System one — the Traditional Authority System</h2>
        <p>Paramount Chiefs, Section Chiefs, Bondo and Poro societies, women's governance
        networks, farmers' cooperatives, and the full infrastructure of community social
        governance. This system has been present in Sierra Leone's governance architecture
        longer than any other institution, and holds three things no external programme can
        replicate: social legitimacy, social enforcement capacity, and embedded knowledge of
        community dynamics and vulnerability that no external assessment can fully reach
        from outside.</p>
        <p>Every external health programme Sierra Leone has hosted has treated it as a
        community engagement mechanism — a stakeholder to consult before implementation, a
        channel for mobilisation, a formality to observe and move past. That profoundly
        misreads what traditional authority is. It is not a consultation mechanism. It is a
        governing authority, and this Framework is the first community health architecture
        to treat it as one.</p>
        <h2>System two — the Government Health System</h2>
        <p>The Ministry of Health, District Health Management Teams, Peripheral Health
        Units and the national programme directorates. This system holds legal authority
        over resource allocation and clinical standards, technical and epidemiological
        capacity, and access to national and international resources no other system can
        independently reach.</p>
        <p>Its critical structural weakness is distance — institutional, geographic and
        social. DHMTs sit in district towns; PHUs serve catchments limited by staffing and
        road access. The communities with the highest disease burden are exactly those most
        distant from its functional reach. ProcCHWs exist to bridge that distance, but only
        when genuinely integrated into the government's data architecture, supply chain and
        governance structures — not when they create the appearance of reach without the
        reality of connection.</p>
        <h2>System three — the Community Epidemiological System</h2>
        <p>The most original element of the Framework's theory, and the system most
        completely invisible to every previous framework applied here. It is the health
        intelligence communities themselves hold and generate, and in post-Ebola Sierra
        Leone it is the most current and most proximate health intelligence available
        anywhere in the country.</p>
        <p>It has three components. The epidemiological knowledge communities generated
        during the 2014–2016 outbreak — detection capabilities, contact tracing instincts,
        risk communication networks — held not in any database but in the memory of
        survivors and the social networks through which health information travels. The
        informal surveillance every community conducts continuously: seasonal disease
        patterns, which households have sick children, which water sources are contaminated
        in the dry season. And the community-level mapping of vulnerability: which families
        cannot afford transport to the PHU, which mothers have been missed by every previous
        programme, which children have never received a vaccine.</p>
        <h2>The ProcCHW as systems connector</h2>
        <p>Repositioning the community health worker from service delivery agent to systems
        connector is the theoretical contribution that makes this Framework original. The
        <a href="/our-model/procchw/">ProcCHW</a> is the human infrastructure through which
        the three systems exchange intelligence, align authority and govern health together.
        This is not a function layered on top of service delivery. It is the primary
        function, from which service delivery quality, sustainability and equity all
        derive.</p>
        <p>The shift changes what is measured. A service delivery agent is measured on
        households visited, cases treated and referrals made. A systems connector is measured
        on connection quality — are the three systems exchanging intelligence and governing
        health together because this ProcCHW is present? It changes accountability, too:
        from accountability to the programme that trains and pays them, to accountability to
        all three systems at once. And it changes the success criterion, from high output
        metrics sustained through a programme cycle, to three systems that keep governing
        community health together after our presence reduces.</p>
        """,
    ),
    (
        "reach-360/foundations",
        "The Four Constitutional Foundations",
        "REACH 360°",
        "Sierra Leone's starting conditions, which precede every design decision in the "
        "Framework.",
        """
        <p>The Four Constitutional Foundations are the specific starting conditions that
        precede every design decision in the REACH 360° Framework. They are not in any
        international framework, because they are specific to Sierra Leone. They are not
        negotiable design choices. They are constitutional facts of this country's
        governance, policy, history and institutional architecture, which any community
        health framework must account for fully or fail because it did not.</p>
        <h2>One — chieftaincy as legitimate health governance authority</h2>
        <p>Paramount and Section Chiefs are governing authorities, not stakeholders, with
        real power over land, social relationships, community behaviour and resource
        distribution in their chiefdoms. This authority predates the Sierra Leonean state.
        The Framework responds by formalising traditional authority as a co-equal governing
        partner with defined decision-making domains, formal commodity stewardship
        accountability, and a financing advocacy role.</p>
        <h2>Two — the Free Healthcare Initiative as the policy universe</h2>
        <p>Sierra Leone committed in 2010 to free health care for pregnant women, lactating
        mothers and children under five. Communities hold expectations about cost-free care
        that shape every dimension of the ProcCHW–household relationship. All services are
        delivered at no cost within that mandate, and the Community Transport Linkage Fund
        fills the gap between the policy commitment and the household's experience of
        it.</p>
        <h2>Three — post-Ebola community intelligence as a health system asset</h2>
        <p>The 2014–2016 outbreak gave communities — particularly in Eastern Province —
        disease detection, risk communication and emergency response capabilities that no
        training programme produced. Those capabilities exist today. The Framework treats
        them not as a trauma legacy to manage but as an epidemiological intelligence
        infrastructure to activate, govern and integrate into national surveillance.</p>
        <h2>Four — the sixteen-district DHMT architecture</h2>
        <p>Sierra Leone's health system is organised through 16 District Health Management
        Teams with genuine governing authority over resource allocation, staffing and
        programme management. This is not an administrative convenience; it is the actual
        governance architecture through which health decisions are made. So the Framework
        operates within it rather than alongside it: our District Coordinators office inside
        DHMT facilities, all supervision is DHMT co-led, DHMTs co-sign every ProcCHW
        appointment, and they reach all programme data directly without our
        intermediation.</p>
        """,
    ),
    (
        "reach-360/idhs",
        "Intelligent Digital Health Systems",
        "REACH 360°",
        "Digital tools are not the innovation. How they are governed, owned and used in "
        "service of human connection — that is the innovation.",
        """
        <blockquote>Intelligent Digital Health Systems Integration is not a technology
        programme. It is a governance principle implemented through technology.</blockquote>
        <p>IDHS deploys digital tools, including AI-assisted capabilities, inside Sierra
        Leone's national government health information architecture, to strengthen the
        three-systems connection that is the Framework's core purpose. It is not a
        standalone pillar. It is a horizontal dimension running through all
        <a href="/what-we-do/">seven pillars</a>, enhancing what each does without
        substituting for the human systems, governance structures and community
        relationships each is built on.</p>
        <h2>What the three words carry</h2>
        <p><strong>Intelligent</strong> distinguishes AI-enhanced tools from standard
        digital health tools — machine learning, algorithmic decision support and
        predictive analytics that a standard DHIS2 configuration does not possess.
        <strong>Digital</strong> positions these capabilities within the established digital
        health policy frameworks of the WHO, UNICEF, FCDO, GAVI and the Global Fund.
        <strong>Integration</strong> names the design principle: every tool integrates into
        existing government systems rather than creating parallel architecture.</p>
        <h2>The TRIAD AI Test</h2>
        <p>Every AI tool in the Framework must pass three tests before deployment, and the
        standard is non-negotiable.</p>
        <ul>
          <li><strong>Traditional authority intelligibility.</strong> A Paramount Chief must
          be able to understand what the tool does and hold formal authority to query its
          outputs.</li>
          <li><strong>Government ownership.</strong> The tool must be owned by government
          from day one, accessible through DHIS2 instances DHMTs reach independently, and
          designed for government operation by 2031.</li>
          <li><strong>Community contestability.</strong> Communities must be able to
          formally contest any classification affecting them, and receive quarterly
          plain-language reports on how the tools are behaving.</li>
        </ul>
        <h2>Human primacy</h2>
        <p>These tools assist human care; they do not replace it. The ProcCHW's clinical
        judgment, the community's trust, the traditional authority's endorsement and the
        government's clinical protocol are always the primary governing layer. Alerts are
        suggestions, not prescriptions. ProcCHWs are trained from their first day on when to
        override an alert and how to report an error, and cases where a ProcCHW's judgment
        correctly overrode the system are reviewed with the whole cohort.</p>
        <h2>Nothing proprietary left behind</h2>
        <p>The AI layers are configured as DHIS2 program rule extensions — a standard
        platform feature — so they run inside the government's existing architecture
        without new servers, new procurement or new technical staff. Government technical
        staff are trained in model monitoring and retraining from Year 3. When our direct
        role ends, the capability transfers with the platform rather than away from it.</p>
        """,
    ),
    (
        "reach-360/connection-quality-index",
        "The Connection Quality Index",
        "REACH 360°",
        "Not what the programme produced, but what changed in the governance systems "
        "around it because of its presence.",
        """
        <blockquote>The CQI measures what the REACH 360° Framework most cares about — not
        what the programme produced, but what changed in the governance systems around the
        programme because of its presence.</blockquote>
        <h2>Why standard metrics are insufficient</h2>
        <p>Standard programme monitoring measures outputs. The CQI measures systems
        connection: whether the three governance systems are genuinely exchanging
        intelligence, aligning authority and governing community health together. A
        programme with high output metrics and a CQI score below 40 is a service delivery
        programme that will collapse when funding ends. A rising CQI score signals a system
        being built that will outlast the grant cycle.</p>
        <p><a href="/reach-360/idhs/">Intelligent Digital Health Systems</a> support CQI
        measurement by automating data collection and aggregation, freeing assessors to
        focus on the qualitative dimensions that require human judgment — which no AI can
        generate from platform data alone.</p>
        <h2>The three dimensions</h2>
        <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Dimension</th>
              <th scope="col">Indicators (four per dimension)</th>
              <th scope="col">Year 3</th>
              <th scope="col">Year 5</th>
              <th scope="col">IDHS support</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">1. Traditional authority governance integration</th>
              <td>Percentage of chiefs describing chiefdom health indicators without
              prompting; TA governance decisions with measurable programme consequences;
              stockout events escalated through traditional governance; ProcCHW selection
              legitimacy through the TA process.</td>
              <td>&gt; 70%</td>
              <td>&gt; 90%</td>
              <td>TACGS governance event log analysis; automated scoring of TA Health
              Governance Council meeting records.</td>
            </tr>
            <tr>
              <th scope="row">2. Government–community intelligence flow</th>
              <td>Percentage of DHMT decisions citing community data; CEIN
              detection-to-DHMT time; percentage of community members able to state one
              health statistic; percentage of dashboard alerts generating DHMT corrective
              action.</td>
              <td>&gt; 50%</td>
              <td>&gt; 75%</td>
              <td>DHMT dashboard access log analysis; CEIN alert timestamp tracking;
              automated CQI data extraction from DHIS2.</td>
            </tr>
            <tr>
              <th scope="row">3. Community health system navigation capacity</th>
              <td>Percentage of referrals completed without a ProcCHW escort; time
              reduction from danger sign to facility; percentage of maternal deaths
              reported through community channels; percentage of CHC decisions made without
              District Coordinator facilitation.</td>
              <td>&gt; 55%</td>
              <td>&gt; 70%</td>
              <td>Referral completion tracking; transport barrier pattern analysis; CHC
              governance independence scoring from meeting records.</td>
            </tr>
          </tbody>
        </table>
        </div>
        <h2>Reading the score</h2>
        <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th scope="col">Score</th>
              <th scope="col">Interpretation</th>
              <th scope="col">What it means</th>
              <th scope="col">Required action</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <th scope="row">80–100</th>
              <td>Systems deeply connected</td>
              <td>REACH 360° fully working — the systems will sustain without iREACHE
              LASTMILE's direct presence.</td>
              <td>Maintain; document as a model district; begin the transition to a
              technical assistance role; initiate IDHS government ownership transfer.</td>
            </tr>
            <tr>
              <th scope="row">60–79</th>
              <td>Substantially connected, with specific gaps</td>
              <td>The framework is working but one dimension is lagging, and targeted
              intervention is required.</td>
              <td>Targeted intervention in the weak dimension; additional District
              Coordinator support; IDHS tool review for that dimension.</td>
            </tr>
            <tr>
              <th scope="row">40–59</th>
              <td>Partially connected</td>
              <td>Outputs without connections — the service delivery trap.</td>
              <td>Programme design review; TACGS renegotiation; IDHS deployment suspended
              in weak dimensions until the human systems are established.</td>
            </tr>
            <tr>
              <th scope="row">Below 40</th>
              <td>Insufficiently connected</td>
              <td>Structural programme failure — service delivery without systems
              building.</td>
              <td>District pause; root cause analysis; Crosswalk divergence alert; all IDHS
              applications suspended until the human systems are established; Board-level
              reporting.</td>
            </tr>
          </tbody>
        </table>
        </div>
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
        <p>iREACHE LASTMILE is governed by a board that oversees strategy, risk and
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
    help = "Seed the iREACHE LASTMILE site with navigation and starter content."

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
        for field, (superseded, current) in SUPERSEDED_SETTINGS.items():
            if getattr(settings_obj, field) in ("",) + superseded:
                setattr(settings_obj, field, current)
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
        FocusArea.objects.filter(slug__in=LEGACY_FOCUS_AREA_SLUGS).delete()
        for index, (title, icon, summary, body) in enumerate(FOCUS_AREAS):
            FocusArea.objects.update_or_create(
                slug=slugify(title)[:160],
                defaults={
                    "title": title,
                    "icon": icon,
                    "summary": summary,
                    "body": body,
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
        """Write both stat groups.

        A figure is keyed on its value *and* its group: 6,800 appears in the
        hero and again in the band, with different wording in each, so the value
        alone no longer identifies a row. Rows in a group that the document no
        longer lists are deleted, which is how the band was cut from three long
        sentences to five short ones.
        """
        Stat.objects.filter(value__in=LEGACY_STAT_VALUES).delete()
        for index, (value, label, caption) in enumerate(HERO_STATS):
            Stat.objects.update_or_create(
                value=value,
                group=Stat.HERO,
                defaults={"label": label, "caption": caption, "order": index},
            )
        for index, (value, label) in enumerate(BAND_STATS):
            Stat.objects.update_or_create(
                value=value,
                group=Stat.BAND,
                defaults={"label": label, "caption": "", "order": index},
            )
        Stat.objects.filter(group=Stat.HERO).exclude(
            value__in=[value for value, _, _ in HERO_STATS]
        ).delete()
        Stat.objects.filter(group=Stat.BAND).exclude(
            value__in=[value for value, _ in BAND_STATS]
        ).delete()
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
