from __future__ import annotations

import typer
from src.components.content_sum import ContentSummarizationInput
from src.components.content_sum import ContentSummarizationService
from src.components.convert2post import ConvertPostInput
from src.components.convert2post import ConvertPostService
from src.components.pull_content import PaperInput
from src.components.pull_content import PaperService
from src.settings.settings import load_settings

app = typer.Typer()


@app.command()
def main(
    paper_url: str = typer.Option(
        [], '--url_link', '-u', help='Link to paper',
    ),
    file_path: str = typer.Option(
        'data/paper.pdf', '--file_path', '-f', help='File Input Path',
    ),
    tone: str = typer.Option('Professional', '--tone', '-t', help='Tone'),
    target_platform: str = typer.Option(
        'LinkedIn', '--target_platform', '-p', help='Target Platform',
    ),
) -> str:

    # Load settings
    settings = load_settings()

    # Initialize services
    content_summarization_service = ContentSummarizationService(
        openai_settings=settings.openai,
        llamaparser_settings=settings.llamaparser,
    )

    convert_post_service = ConvertPostService(
        openai_settings=settings.openai,
    )

    paper_service = PaperService()

    # Get Paper
    paper_file = paper_service.process(
        PaperInput(
            paper_url=paper_url,
            file_path=file_path,
        ),
    )

    # Get summary paper
    summary = content_summarization_service.process(
        ContentSummarizationInput(file_path=paper_file.paper_file),
    )

    # Get post
    post = convert_post_service.process(
        ConvertPostInput(
            summary_content=summary.content_sum,
            tone=tone,
            target_platform=target_platform,
        ),
    )

    # Get file_name (split end .pdf)
    file_name = file_path.split('.')[0]

    # Save output to file txt, file name is file_path without txt
    with open(f'{file_name}.txt', 'w', encoding='utf-8') as f:
        f.write(post.post)
    return post.post


if __name__ == '__main__':
    app()
