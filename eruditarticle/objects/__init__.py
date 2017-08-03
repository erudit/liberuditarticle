"""
.. warning::

   Part of the objects interface is deprecated and will be removed or modified in the 0.3.0
   version of ``liberuditarticle``.

   All ``get_html`` and ``get_formatted`` methods will be removed,
   and all ``get_`` methods will support ``formatted`` and ``html`` keyword arguments where
   applicable.

   All ``strip_markup`` keyword arguments will be removed in favour of ``html=False``.

   For example:

   * ``get_formatted_title`` will become ``get_title(formatted=True)``.
   * ``get_html_title`` will become ``get_title(html=True)``.
   * ``get_title(html=True, formatted=True)`` will return a formatted html title

"""
from .publication import EruditPublication  # noqa
from .article import EruditArticle  # noqa
from .journal import EruditJournal  # noqa
from .base import EruditBaseObject  # noqa
