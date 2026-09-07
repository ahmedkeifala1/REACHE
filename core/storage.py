"""File storage for pictures uploaded from inside the rich text editor.

django-ckeditor-5 saves uploads with the plain default storage, which puts them
at the top of MEDIA_ROOT next to the ``site/``, ``posts/`` and ``pages/``
folders that ``seed_images`` manages. Giving the editor its own subfolder keeps
the two apart, so a bulk reset of the seed photography can never sweep up a
picture someone placed in a page by hand.
"""

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class EditorUploadStorage(FileSystemStorage):
    """FileSystemStorage rooted at ``media/uploads/``."""

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("location", settings.MEDIA_ROOT / "uploads")
        kwargs.setdefault("base_url", settings.MEDIA_URL + "uploads/")
        super().__init__(*args, **kwargs)
