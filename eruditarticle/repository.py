# -*- coding: utf-8 -*-

from eulfedora.server import Repository

from .conf import settings

print(settings.FEDORA_ROOT)
repo = Repository(
    settings.FEDORA_ROOT, settings.FEDORA_USER, settings.FEDORA_PASSWORD)
