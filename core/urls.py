from django.urls import path, re_path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("search/", views.search, name="search"),
    path("newsletter/", views.newsletter_signup, name="newsletter"),
    # What We Do
    path("what-we-do/", views.what_we_do, name="what_we_do"),
    path("what-we-do/<slug:slug>/", views.focus_area_detail, name="focus_area"),
    # Our Programs
    path("our-programs/", views.programs, name="programs"),
    path("our-programs/<slug:slug>/", views.program_detail, name="program"),
    # Where We Work
    path("where-we-work/", views.where_we_work, name="where_we_work"),
    path("where-we-work/<slug:slug>/", views.location_detail, name="location"),
    # Who We Are
    path("who-we-are/meet-our-team/", views.team, name="team"),
    path("who-we-are/our-partners/", views.partners, name="partners"),
    # Our Impact
    path("our-impact/newsroom/", views.newsroom, name="newsroom"),
    path("our-impact/newsroom/<slug:slug>/", views.post_detail, name="post"),
    path("our-impact/resources/", views.resources, name="resources"),
    # Get Involved
    path("get-involved/work-for-us/", views.work_for_us, name="work_for_us"),
    path("get-involved/contact-us/", views.contact, name="contact"),
    path("get-involved/donate/", views.donate, name="donate"),
    # Flat pages, matched last so the routes above always win.
    re_path(r"^(?P<path>[\w\-/]+)/$", views.page_detail, name="page"),
]
