from __future__ import annotations

from .base import ContentParserInput
from .base import ContentParserOutput
from .base import ContentParserService
from .news import NewsInput
from .news import NewsOutput
from .news import NewsService
from .paper import PaperInput
from .paper import PaperOutput
from .paper import PaperService
from .type import ContentType

__all__ = [
    'PaperInput',
    'PaperOutput',
    'PaperService',
    'NewsInput',
    'NewsOutput',
    'NewsService',
    'ContentType',
    'ContentParserInput',
    'ContentParserOutput',
    'ContentParserService',
]
