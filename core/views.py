"""Views for the REACHE Last-Mile site."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from . import section_pages
from .models import (
    ContactMessage,
    FocusArea,
    Job,
    Location,
    NewsletterSignup,
    Page,
    Partner,
    Post,
    PostCategory,
    Program,
    Resource,
    Stat,
    TeamMember,
)


def home(request):
    posts = Post.objects.visible_to(request.user)
    context = {
        "featured_posts": posts.filter(is_featured=True)[:5],
        "focus_areas": FocusArea.objects.all(),
        "stats": Stat.objects.all(),
        "locations": Location.objects.all()[:6],
        "posts": posts[:6],
        "programs": Program.objects.all()[:6],
    }
    return render(request, "pages/home.html", context)


def page_detail(request, path):
    page = get_object_or_404(
        Page.objects.visible_to(request.user).prefetch_related("gallery"),
        path=path.strip("/"),
    )
    return render(request, "pages/page.html", {"page": page})


def what_we_do(request):
    context = {
        "focus_areas": FocusArea.objects.all(),
        "hero": section_pages.hero("what-we-do", request.user),
    }
    return render(request, "pages/what_we_do.html", context)


def focus_area_detail(request, slug):
    area = get_object_or_404(FocusArea, slug=slug)
    return render(
        request,
        "pages/focus_area.html",
        {"area": area, "others": FocusArea.objects.exclude(pk=area.pk)[:3]},
    )


def programs(request):
    return render(
        request,
        "pages/programs.html",
        {
            "programs": Program.objects.all(),
            "hero": section_pages.hero("our-programs", request.user),
        },
    )


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    return render(
        request,
        "pages/program.html",
        {"program": program, "others": Program.objects.exclude(pk=program.pk)[:3]},
    )


def where_we_work(request):
    return render(
        request,
        "pages/where_we_work.html",
        {
            "locations": Location.objects.all(),
            "hero": section_pages.hero("where-we-work", request.user),
        },
    )


def location_detail(request, slug):
    location = get_object_or_404(Location, slug=slug)
    return render(
        request,
        "pages/location.html",
        {
            "location": location,
            "others": Location.objects.exclude(pk=location.pk)[:3],
            "posts": Post.objects.visible_to(request.user)[:3],
        },
    )


def newsroom(request):
    qs = Post.objects.visible_to(request.user)
    category = request.GET.get("category")
    query = request.GET.get("q")
    if category:
        qs = qs.filter(category__slug=category)
    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(excerpt__icontains=query))

    paginator = Paginator(qs, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    context = {
        "page_obj": page_obj,
        "categories": PostCategory.objects.all(),
        "active_category": category,
        "query": query or "",
        "hero": section_pages.hero("our-impact/newsroom", request.user),
    }
    return render(request, "pages/newsroom.html", context)


def post_detail(request, slug):
    visible = Post.objects.visible_to(request.user)
    post = get_object_or_404(visible, slug=slug)
    related = visible.exclude(pk=post.pk)
    if post.category:
        related = related.filter(category=post.category)
    return render(
        request,
        "pages/post.html",
        {"post": post, "related": related[:3]},
    )


def team(request):
    return render(
        request,
        "pages/team.html",
        {
            "leadership": TeamMember.objects.filter(is_leadership=True),
            "staff": TeamMember.objects.filter(is_leadership=False),
            "hero": section_pages.hero("who-we-are/meet-our-team", request.user),
        },
    )


def partners(request):
    return render(
        request,
        "pages/partners.html",
        {
            "partners": Partner.objects.all(),
            "hero": section_pages.hero("who-we-are/our-partners", request.user),
        },
    )


def resources(request):
    return render(
        request,
        "pages/resources.html",
        {
            "resources": Resource.objects.all(),
            "hero": section_pages.hero("our-impact/resources", request.user),
        },
    )


def work_for_us(request):
    return render(
        request,
        "pages/jobs.html",
        {
            "jobs": Job.objects.filter(is_open=True),
            "hero": section_pages.hero("get-involved/work-for-us", request.user),
        },
    )


def donate(request):
    return render(
        request,
        "pages/donate.html",
        {
            "stats": Stat.objects.all(),
            "hero": section_pages.hero("get-involved/donate", request.user),
        },
    )


def search(request):
    query = (request.GET.get("q") or "").strip()
    results = {"posts": [], "pages": [], "programs": [], "locations": []}
    if query:
        results["posts"] = Post.objects.visible_to(request.user).filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query)
        )[:10]
        results["pages"] = Page.objects.visible_to(request.user).filter(
            Q(title__icontains=query) | Q(intro__icontains=query)
        )[:10]
        results["programs"] = Program.objects.filter(
            Q(title__icontains=query) | Q(summary__icontains=query)
        )[:10]
        results["locations"] = Location.objects.filter(name__icontains=query)[:10]
    total = sum(len(v) for v in results.values())
    return render(
        request,
        "pages/search.html",
        {"query": query, "results": results, "total": total},
    )


def contact(request):
    if request.method == "POST":
        name = (request.POST.get("name") or "").strip()
        email = (request.POST.get("email") or "").strip()
        message = (request.POST.get("message") or "").strip()
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=(request.POST.get("subject") or "").strip(),
                message=message,
            )
            messages.success(
                request, "Thank you for reaching out. We will be in touch shortly."
            )
            return redirect("core:contact")
        messages.error(request, "Please complete the name, email and message fields.")
    return render(
        request,
        "pages/contact.html",
        {"hero": section_pages.hero("get-involved/contact-us", request.user)},
    )


def newsletter_signup(request):
    """Handles the newsletter form that appears in several page sections."""
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        if email:
            _, created = NewsletterSignup.objects.get_or_create(email=email)
            if created:
                messages.success(request, "You are subscribed. Thank you!")
            else:
                messages.info(request, "That address is already on our list.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER", "/"))
