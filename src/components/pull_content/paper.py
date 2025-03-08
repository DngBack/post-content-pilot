from __future__ import annotations

import wget

from .base import ContentParserInput
from .base import ContentParserOutput
from .base import ContentParserService


class PaperInput(ContentParserInput):
    paper_url: str
    file_path: str = "data/paper.pdf"

class PaperOutput(ContentParserOutput):
    paper_file: str

class PaperService(ContentParserService):
    def process(self, inputs: PaperInput) -> PaperOutput:
        paper_file = wget.download(
            url=inputs.paper_url, 
            out=inputs.file_path
        )
        return PaperOutput(paper_file=paper_file)
