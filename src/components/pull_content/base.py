from __future__ import annotations

from .type import ContentType

from ...base import BaseModel
from ...base import BaseService

class ContentParserInput(BaseModel):
    type: ContentType
    
class ContentParserOutput(BaseModel):
    pass

class ContentParserService(BaseService):
    def process(self, inputs: ContentParserInput) -> ContentParserOutput:
        raise NotImplementedError()