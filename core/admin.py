from django.contrib import admin

from .models import (
    ContactMessage,
    FocusArea,
    Job,
    Location,
    MenuItem,
    NewsletterSignup,
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


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
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


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "path", "section", "updated")
    search_fields = ("title", "path", "intro", "body")


@admin.register(FocusArea)
class FocusAreaAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_office", "order")
    list_editable = ("is_office", "order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ("value", "label", "order")
    list_editable = ("order",)


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published", "is_featured")
    list_filter = ("category", "is_featured", "published")
    search_fields = ("title", "excerpt", "body")
    date_hierarchy = "published"
    prepopulated_fields = {"slug": ("title",)}


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "is_leadership", "order")
    list_editable = ("order", "is_leadership")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "order")
    list_editable = ("order",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "published")
    list_filter = ("resource_type",)


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "location", "employment_type", "is_open", "closing_date")
    list_filter = ("is_open",)
    prepopulated_fields = {"slug": ("title",)}


@admin.register(NewsletterSignup)
class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("email", "created")
    search_fields = ("email",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created", "handled")
    list_filter = ("handled",)
    list_editable = ("handled",)
    search_fields = ("name", "email", "message")
