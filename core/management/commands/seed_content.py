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
STATS = [
    ("6,800", "Professional Connected Community Health Workers across Sierra Leone by 2031."),
    ("16", "districts \u2014 every district in the country \u2014 within the programme by 2031."),
    ("70\u201380%", "of programme costs met from Sierra Leone's own domestic budgets by 2031."),
]

# Stat values carried by the pre-framework placeholder content, removed on seed.
LEGACY_STAT_VALUES = ["2,400,000", "8,500", "640"]

# Wording on the SiteSettings singleton that the Master Document supersedes.
# The document names the organisation iREACHE LASTMILE and expands the *i* as the
# plural "Innovations"; databases seeded before it arrived carry the old wording.
# Each field is only rewritten when it still holds the exact superseded string, so
# anything an editor has changed in the CMS is left alone.
SUPERSEDED_SETTINGS = {
    "organisation_name": (
        "REACHE Last-Mile",
        "iREACHE LASTMILE",
    ),
    "tagline": (
        "Innovation for Rural Empowerment in Access to Community Health and Equity",
        "Innovations for Rural Empowerment in Access to Community Health and Equity",
    ),
    "hero_prefix": (
        "REACHE transforms",
        "iREACHE LASTMILE transforms",
    ),
    "hero_body": (
        "REACHE Last-Mile designs responsive primary health care systems so that "
        "life-saving products and services reach the communities hardest to reach.",
        "iREACHE LASTMILE designs responsive primary health care systems so that "
        "life-saving products and services reach the communities hardest to reach.",
    ),
    "footer_blurb": (
        "REACHE Last-Mile works alongside government, communities and partners "
        "to build primary health care that reaches everyone, everywhere.",
        "iREACHE LASTMILE works alongside government, communities and partners "
        "to build primary health care that reaches everyone, everywhere.",
    ),
    "legal_line": (
        "REACHE Last-Mile is a registered not-for-profit organisation",
        "iREACHE LASTMILE is a registered not-for-profit organisation",
    ),
    "email": (
        "info@reachelastmile.org",
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
        "We are a last-mile health organisation working to make primary health care "
        "reliable for the communities furthest from it.",
        """
        <p>iREACHE LASTMILE exists to close the distance between health systems and the
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
        "Innovations for Rural Empowerment in Access to Community Health and Equity.",
        """
        <h2>Vision</h2>
        <p>A Sierra Leone where every person — in every community, regardless of
        geography, poverty, gender or social circumstance — has equitable access to
        quality community health care delivered by a professional, compensated and
        connected workforce, integrated within a government-owned, domestically financed
        and intelligently supported health system.</p>
        <h2>Mission</h2>
        <p>To strengthen Sierra Leone's community health systems by deploying, training,
        equipping, supervising, compensating and institutionalising a national workforce
        of Professional Connected Community Health Workers — governed by communities,
        integrated into government systems, supported by Intelligent Digital Health
        Systems and sustained through domestic financing — through the
        <a href="/reach-360/">REACH 360° Community Health Systems Strengthening
        Framework</a>.</p>
        <blockquote>Empowerment means doing WITH, not doing FOR.</blockquote>
        <h2>Our values</h2>
        <ul>
          <li><strong>Equity.</strong> Equity is the spine of the REACH 360° Framework,
          not a cross-cutting theme. Every resource allocation, system design and advocacy
          effort is directed first toward the communities most excluded from health
          outcomes. We measure success by narrowing the gap between the best-served and
          worst-served communities — not by improving averages while inequalities
          widen.</li>
          <li><strong>Excellence.</strong> We do not deploy tools, protocols or systems
          that have not been validated in Sierra Leone's specific context. We publish our
          methods and our results — including our failures — so that excellence is
          verifiable rather than claimed.</li>
          <li><strong>Accountability.</strong> We are accountable first to communities,
          then to government, then to donors, in that order. We do not manage
          accountability; we build it into programme architecture.</li>
          <li><strong>Co-ownership.</strong> Doing WITH, not doing FOR is a design
          specification, not a communications aspiration. Communities select their
          ProcCHWs. Traditional Authority Health Governance Councils hold formal
          accountability. Community Health Committees make real decisions with real
          consequences.</li>
          <li><strong>Government primacy.</strong> Every system we build is designed from
          its first day to be owned, financed and operated by the Government of Sierra
          Leone. We build no parallel infrastructure. We measure our success by how little
          Sierra Leone needs us at the end.</li>
          <li><strong>Evidence.</strong> Every programme decision is grounded in data, and
          we treat our own implementation experience as research data to be published.</li>
          <li><strong>Human primacy in digital health.</strong> Digital and AI tools assist
          human care; they do not replace it. The ProcCHW's judgment, the community's
          trust, the traditional authority's endorsement and the government's clinical
          protocol are always the primary governing layer.</li>
          <li><strong>Dignity.</strong> Communities are rights-holders and governing
          partners, not passive beneficiaries. We listen before we design. We ask before
          we assume. We co-create rather than implement.</li>
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
        "We did not found this organisation because we wanted to build an organisation.",
        """
        <blockquote>We did not found iREACHE LASTMILE because we wanted to build an
        organisation. We founded it because we had seen what happens when the systems that
        should protect communities are disconnected — and we could not continue to watch
        it happen.</blockquote>
        <h2>The place where we started</h2>
        <p>Kenema. The word means 'clear water' in Mende — the language of Eastern
        Province, the language of our founders, the language of the communities we serve.
        It is a place of remarkable natural abundance and equally remarkable health
        deprivation. In 2022 the district's maternal mortality rate exceeded Sierra Leone's
        already high national average. In 2024 more than a fifth of children born in its
        most remote chieftaincies received not a single vaccine in their first year.</p>
        <p>Kenema also bore the heaviest concentration of Ebola transmission during the
        2014–2016 outbreak. Communities in remote chieftaincies built their own detection
        systems, their own isolation protocols and their own contact tracing networks,
        because the formal health system could not reach them fast enough. They survived.
        And in surviving they built something no health programme had ever recognised as a
        health system asset: a community epidemiological intelligence infrastructure that
        exists today in the collective memory and social organisation of Eastern Province
        communities.</p>
        <h2>The insight that founded the organisation</h2>
        <p>Our founders had watched the same pattern repeat. Community health workers
        recruited, trained, equipped and deployed. Outcomes improving for the duration of
        the programme cycle. Then the grant ends, the equipment breaks and is not replaced,
        the data systems are abandoned, and communities return to the situation that made
        the programme necessary in the first place.</p>
        <p>The standard diagnosis was that the CHWs were not well enough trained,
        supervised or compensated. The standard solution was to improve all three. The
        standard result was the same collapse at the end of the next cycle.</p>
        <p>So they asked a different question: why does genuinely improved CHW performance
        not produce sustainable health system improvement? The answer that changed
        everything was that CHW performance is a symptom, not the cause. The cause is
        <a href="/reach-360/three-systems/">systems disconnection</a>. A well-performing
        CHW inside three disconnected systems produces better outputs during the programme
        cycle and the same systemic failure when the programme ends.</p>
        <h2>The name and what it means</h2>
        <p><strong>Innovations</strong> — because the REACH 360° Framework is an original
        Sierra Leonean contribution to the global community health field, not an adaptation
        of a global model. <strong>Rural Empowerment</strong> — because empowerment is
        built with communities, not done to them. <strong>Access</strong> — because the
        problem is not quality of care in accessible facilities but access to care in
        inaccessible communities. <strong>Community Health</strong> — because the
        community as a social and governance unit is the level at which we work.
        <strong>Equity</strong> — because equity is the spine of everything we do.</p>
        <p><strong>LASTMILE</strong> is not a communications device. The last mile is the
        segment where the route is hardest, the infrastructure most absent and the cost per
        unit delivered highest — and where delivery matters most, because the communities
        there carry the highest disease burden and have the least access to alternatives.
        It is a programme commitment.</p>
        <h2>The founding commitment</h2>
        <p>We were founded on one commitment: that by 2031 Sierra Leone will
        have a community health system — not a community health programme — that is
        governed by communities, co-led by government, financed domestically and
        continuously strengthened by the intelligence of its own evidence.</p>
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
        <h2>Six architectural levels</h2>
        <ol>
          <li><strong>Global and national foundation.</strong> The WHO Health System
          Building Blocks, primary health care principles from Alma-Ata and Astana, the
          UHC framework and the SDGs; alongside Sierra Leone's NHSSP, National CHW Policy,
          Vision 2030 CHW Programme, Free Healthcare Initiative and IDSR framework.</li>
          <li><strong>Theoretical architecture.</strong> The
          <a href="/reach-360/three-systems/">Three-Systems Connection Theory</a>, the
          <a href="/reach-360/foundations/">Four Constitutional Foundations</a>, equity as
          structural spine, the Connection Quality Index, and
          <a href="/reach-360/idhs/">Intelligent Digital Health Systems Integration</a> as
          a horizontal dimension.</li>
          <li><strong>The <a href="/what-we-do/">seven pillars</a>.</strong> Connected
          Health Workforce; Community Intelligence and Surveillance System; Last-Mile
          Supply Chain and Commodity Access; Sustainable Health Financing and Domestic
          Resource Mobilisation; Three-Authority Community Governance and Accountability;
          Proactive Community Health Service Delivery; and Driving Sustained Impact Through
          Strategic Partnerships.</li>
          <li><strong>The continuous systems cycle.</strong> Listen, map, co-create,
          connect, deliver, measure, learn, strengthen, sustain, scale — a closed loop
          that returns to listening at a higher level of system integration with each
          completed turn.</li>
          <li><strong>Nine programme areas.</strong> Maternal and newborn health; childhood
          disease; immunisation and zero-dose reduction; nutrition systems; sexual and
          reproductive health; community disease surveillance; intelligent digital health
          systems; last-mile supply chain; and emergency response and WASH.</li>
          <li><strong>Measurement architecture.</strong> Output impact through pillar KPIs,
          outcome impact in health status, systems impact through the Connection Quality
          Index, digital impact through the AI Readiness and Responsible Deployment Index,
          and equity impact through the Equity Progress Threshold.</li>
        </ol>
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
            if getattr(settings_obj, field) in ("", superseded):
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
        Stat.objects.filter(value__in=LEGACY_STAT_VALUES).delete()
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
