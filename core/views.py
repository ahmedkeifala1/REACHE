"""Views for the REACHE Last-Mile site."""

from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

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
    featured = Post.objects.filter(is_featured=True)[:5]
    context = {
        "featured_posts": featured,
        "focus_areas": FocusArea.objects.all(),
        "stats": Stat.objects.all(),
        "locations": Location.objects.all()[:6],
        "posts": Post.objects.all()[:6],
        "programs": Program.objects.all()[:6],
    }
    return render(request, "pages/home.html", context)


def page_detail(request, path):
    page = get_object_or_404(Page, path=path.strip("/"))
    return render(request, "pages/page.html", {"page": page})


def what_we_do(request):
    context = {
        "focus_areas": FocusArea.objects.all(),
        "page_title": "What We Do",
        "page_intro": (
            "We design responsive primary health care systems that improve the "
            "accessibility of health products and services for the hardest-to-reach "
            "communities."
        ),
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
        {"programs": Program.objects.all()},
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
        {"locations": Location.objects.all()},
    )


def location_detail(request, slug):
    location = get_object_or_404(Location, slug=slug)
    return render(
        request,
        "pages/location.html",
        {
            "location": location,
            "others": Location.objects.exclude(pk=location.pk)[:3],
            "posts": Post.objects.all()[:3],
        },
    )


def newsroom(request):
    qs = Post.objects.all()
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
    }
    return render(request, "pages/newsroom.html", context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    related = Post.objects.exclude(pk=post.pk)
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
        },
    )


def partners(request):
    return render(request, "pages/partners.html", {"partners": Partner.objects.all()})


def resources(request):
    return render(request, "pages/resources.html", {"resources": Resource.objects.all()})


def work_for_us(request):
    return render(
        request, "pages/jobs.html", {"jobs": Job.objects.filter(is_open=True)}
    )


def donate(request):
    return render(request, "pages/donate.html", {"stats": Stat.objects.all()})


def search(request):
    query = (request.GET.get("q") or "").strip()
    results = {"posts": [], "pages": [], "programs": [], "locations": []}
    if query:
        results["posts"] = Post.objects.filter(
            Q(title__icontains=query) | Q(excerpt__icontains=query)
        )[:10]
        results["pages"] = Page.objects.filter(
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
    return render(request, "pages/contact.html")


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
