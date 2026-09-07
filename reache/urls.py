from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # The rich text editor posts pictures here. It has to be declared before
    # core.urls, whose flat-page catch-all would otherwise match this path and
    # answer the upload with a 404.
    path("ckeditor5/", include("django_ckeditor_5.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
