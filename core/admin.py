"""Admin configuration -- this is the CMS the REACHE team works in.

Three things shape the setup below. Every picture field shows a thumbnail, so an
editor can tell at a glance which rows still carry placeholder photography.
Everything publishable can be saved as a draft and published later, from the list
page as well as the edit form. And the fields on each form are grouped, because a
flat column of twenty inputs gives no hint about which ones matter.
"""

from django.contrib import admin
from django.utils.html import format_html

from .models import (
    ContactMessage,
    FocusArea,
    Job,
    Location,
    MenuItem,
    NewsletterSignup,
    Page,
    PageImage,
    Partner,
    Post,
    PostCategory,
    Program,
    Resource,
    SiteSettings,
    Stat,
    TeamMember,
)

admin.site.site_header = "REACHE Last-Mile"
admin.site.site_title = "REACHE Last-Mile"
admin.site.index_title = "Website content"


def _preview(file, height=48):
    """Render a thumbnail for a file field, or a dash when it is empty."""
    if not file:
        return format_html('<span style="color:#999">&mdash;</span>')
    return format_html(
        '<img src="{}" style="height:{}px;width:auto;max-width:140px;'
        'object-fit:cover;border-radius:4px;border:1px solid #ddd">',
        file.url,
        height,
    )


class ImagePreviewMixin:
    """Adds a thumbnail column and a larger preview for the edit form."""

    preview_field = "image"

    @admin.display(description="Picture")
    def preview(self, obj):
        return _preview(getattr(obj, self.preview_field, None))

    @admin.display(description="Current picture")
    def preview_large(self, obj):
        return _preview(getattr(obj, self.preview_field, None), height=180)


class PublishActionsMixin:
    """Publish and unpublish straight from the changelist."""

    @admin.action(description="Publish selected")
    def publish(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, "{0} published.".format(updated))

    @admin.action(description="Unpublish selected (hide from the public site)")
    def unpublish(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, "{0} hidden from the public site.".format(updated))

    @admin.display(description="Status", ordering="is_published")
    def status(self, obj):
        if obj.is_published:
            return format_html('<b style="color:#1a7f37">Published</b>')
        return format_html('<b style="color:#b35900">Draft</b>')


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """The header, hero, footer and contact details shared by every page."""

    fieldsets = (
        ("Organisation", {"fields": ("organisation_name", "tagline")}),
        (
            "Home page hero",
            {
                "fields": (
                    "hero_prefix",
                    "hero_headline",
                    "hero_rotating_words",
                    "hero_body",
                    "hero_image",
                    "hero_preview",
                ),
            },
        ),
        ("Founding story", {"fields": ("story_image", "story_preview")}),
        ("Footer", {"fields": ("footer_blurb", "legal_line")}),
        ("Contact", {"fields": ("email", "phone", "address")}),
        (
            "Social links",
            {
                "classes": ("collapse",),
                "fields": ("facebook", "linkedin", "youtube", "instagram", "twitter"),
            },
        ),
    )
    readonly_fields = ("hero_preview", "story_preview")

    @admin.display(description="Current hero picture")
    def hero_preview(self, obj):
        return _preview(obj.hero_image, height=180)

    @admin.display(description="Current story picture")
    def story_preview(self, obj):
        return _preview(obj.story_image, height=180)

    def has_add_permission(self, request):
        # Singleton: only ever one settings row.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    fk_name = "parent"
    extra = 0


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("title", "url", "parent", "order", "is_button")
    list_editable = ("order", "is_button")
    list_filter = ("parent",)
    inlines = [MenuItemInline]


class PageImageInline(admin.TabularInline):
    model = PageImage
    extra = 1
    fields = ("preview", "image", "caption", "order")
    readonly_fields = ("preview",)
    verbose_name = "extra picture"
    verbose_name_plural = "Extra pictures (shown as a gallery under the page)"

    @admin.display(description="Preview")
    def preview(self, obj):
        return _preview(obj.image)


@admin.register(Page)
class PageAdmin(PublishActionsMixin, admin.ModelAdmin):
    list_display = ("title", "path", "kind", "status", "updated")
    list_filter = ("is_published", "is_section_page", "show_newsletter")
    search_fields = ("title", "path", "intro", "body")
    actions = ["publish", "unpublish"]
    inlines = [PageImageInline]
    readonly_fields = ("hero_preview", "created", "updated")
    fieldsets = (
        ("Heading", {"fields": ("title", "section", "intro")}),
        ("Content", {"fields": ("body",)}),
        ("Picture", {"fields": ("hero_image", "hero_preview")}),
        (
            "Address and visibility",
            {"fields": ("path", "is_published", "is_section_page", "show_newsletter")},
        ),
        (
            "Search engines and link previews",
            {"classes": ("collapse",), "fields": ("meta_description",)},
        ),
        ("History", {"classes": ("collapse",), "fields": ("created", "updated")}),
    )

    @admin.display(description="Kind", ordering="is_section_page")
    def kind(self, obj):
        return "Section landing page" if obj.is_section_page else "Standalone page"

    @admin.display(description="Current picture")
    def hero_preview(self, obj):
        return _preview(obj.hero_image, height=180)

    def get_readonly_fields(self, request, obj=None):
        fields = list(super().get_readonly_fields(request, obj))
        # A section page is joined to its route by its path, so editing that
        # would quietly detach the page and bring the built-in wording back.
        if obj is not None and obj.is_section_page:
            fields += ["path", "is_section_page"]
        return fields

    def has_delete_permission(self, request, obj=None):
        # Deleting one would not remove the page; it would only reset it.
        if obj is not None and obj.is_section_page:
            return False
        return super().has_delete_permission(request, obj)


@admin.register(FocusArea)
class FocusAreaAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "title", "icon", "order")
    list_display_links = ("title",)
    list_editable = ("order",)
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Focus area", {"fields": ("title", "slug", "icon", "order")}),
        ("Content", {"fields": ("summary", "body")}),
        ("Picture", {"fields": ("image", "preview_large")}),
    )


@admin.register(Program)
class ProgramAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "title", "order")
    list_display_links = ("title",)
    list_editable = ("order",)
    search_fields = ("title", "summary", "body")
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Programme", {"fields": ("title", "slug", "order")}),
        ("Content", {"fields": ("summary", "body")}),
        ("Picture", {"fields": ("image", "preview_large")}),
    )


@admin.register(Location)
class LocationAdmin(ImagePreviewMixin, admin.ModelAdmin):
    list_display = ("preview", "name", "is_office", "order")
    list_display_links = ("name",)
    list_editable = ("is_office", "order")
    search_fields = ("name", "summary", "body")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Location", {"fields": ("name", "slug", "is_office", "order")}),
        ("Content", {"fields": ("summary", "body")}),
        ("Picture", {"fields": ("image", "preview_large")}),
    )


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(PublishActionsMixin, ImagePreviewMixin, admin.ModelAdmin):
    list_display = (
        "preview",
        "title",
        "category",
        "published",
        "status",
        "is_featured",
    )
    list_display_links = ("title",)
    list_filter = ("is_published", "category", "is_featured", "published")
    search_fields = ("title", "excerpt", "body")
    date_hierarchy = "published"
    prepopulated_fields = {"slug": ("title",)}
    actions = ["publish", "unpublish"]
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Story", {"fields": ("title", "slug", "category", "published")}),
        ("Content", {"fields": ("excerpt", "body")}),
        ("Picture", {"fields": ("image", "preview_large")}),
        ("Home page", {"fields": ("is_featured", "featured_kicker")}),
        ("Visibility", {"fields": ("is_published",)}),
        (
            "Search engines and link previews",
            {"classes": ("collapse",), "fields": ("meta_description",)},
        ),
    )


@admin.register(TeamMember)
class TeamMemberAdmin(ImagePreviewMixin, admin.ModelAdmin):
    preview_field = "photo"
    list_display = ("preview", "name", "role", "is_leadership", "order")
    list_display_links = ("name",)
    list_editable = ("order", "is_leadership")
    list_filter = ("is_leadership",)
    search_fields = ("name", "role", "bio")
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Person", {"fields": ("name", "role", "bio")}),
        ("Photo", {"fields": ("photo", "preview_large")}),
        ("Listing", {"fields": ("is_leadership", "order")}),
    )


@admin.register(Partner)
class PartnerAdmin(ImagePreviewMixin, admin.ModelAdmin):
    preview_field = "logo"
    list_display = ("preview", "name", "url", "order")
    list_display_links = ("name",)
    list_editable = ("order",)
    search_fields = ("name",)
    readonly_fields = ("preview_large",)
    fieldsets = (
        ("Partner", {"fields": ("name", "url", "order")}),
        ("Logo", {"fields": ("logo", "preview_large")}),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "published")
    list_filter = ("resource_type",)
    search_fields = ("title", "description")
    date_hierarchy = "published"
    fieldsets = (
        ("Resource", {"fields": ("title", "resource_type", "published")}),
        ("Description", {"fields": ("description",)}),
        (
            "The file itself",
            {
                "description": "Upload a file, or link to one hosted elsewhere.",
                "fields": ("file", "external_url"),
            },
        ),
    )


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "employment_type", "is_open", "closing_date")
    list_filter = ("is_open", "employment_type")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = (
        ("Vacancy", {"fields": ("title", "slug", "location", "employment_type")}),
        ("Description", {"fields": ("description",)}),
        ("Listing", {"fields": ("is_open", "closing_date")}),
    )


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created")
    search_fields = ("email",)

    def has_add_permission(self, request):
        # These arrive from the public form; adding one by hand is a mistake.
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created", "handled")
    list_filter = ("handled",)
    list_editable = ("handled",)
    search_fields = ("name", "email", "message")
    readonly_fields = ("name", "email", "subject", "message", "created")

    def has_add_permission(self, request):
        return False
