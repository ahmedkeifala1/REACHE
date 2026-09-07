"""Injects the global site chrome into every template."""

from .models import MenuItem, SiteSettings


def site_context(request):
    menu = (
        MenuItem.objects.filter(parent__isnull=True)
        .prefetch_related("children")
        .order_by("order", "id")
    )
    return {
        "site": SiteSettings.load(),
        "main_menu": menu,
    }
